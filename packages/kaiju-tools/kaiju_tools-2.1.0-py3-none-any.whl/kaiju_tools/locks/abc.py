import abc
import asyncio
from time import time
from typing import Optional, Union

from kaiju_tools.services import ContextableService, Service
from kaiju_tools.scheduler import Scheduler

from .etc import StatusCodes
from .exceptions import *

__all__ = ['BaseLocksService']


class BaseLocksService(ContextableService, abc.ABC):
    """Base class for managing shared locks (in redis or other external store).

    It stores the TTL of a lock locally, sets a short-lived key in an external storage
    and periodically renews it until the TTL is reached. Thus it prevents apps from
    deadlocking if a service acquired the lock is unexpectedly terminated.

    You should inherit from this class if you want to program a custom
    backend specific lock service.
    """

    service_name = 'locks'
    WAIT_RELEASE_REFRESH_INTERVAL = 1  #: (s) interval between tries to acquire a used lock
    MIN_REFRESH_INTERVAL = 1  #: (s) minimal allowed refresh interval for the daemon
    REFRESH_INTERVAL = 60  #: (s) how often locks will be renewed by the daemon
    BASE_TTL = 3 * REFRESH_INTERVAL  #: (s) lifetime of a lock after each renewal
    PREFIX = 'lock'  #: default lock key prefix
    DELIMITER = ':'
    transport_cls = None

    def __init__(
        self,
        app,
        transport: Service = None,
        namespace: str = None,
        refresh_interval: int = REFRESH_INTERVAL,
        scheduler: str = None,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param transport: transport service (may be Redis, DB or similar)
        :param namespace: optional custom namespace (None == app.name)
        :param refresh_interval:  how often locks will be renewed
        :param logger:
        """
        super().__init__(app=app, logger=logger)
        self._namespace = namespace if namespace else app['name']
        self._transport_name = transport
        self._refresh_interval = max(self.MIN_REFRESH_INTERVAL, int(refresh_interval))
        self._scheduler: Union[Scheduler, None] = scheduler
        self._keys = {}
        self._closing = False
        self._transport = None
        self._task = None

    async def init(self):
        """Initialize."""
        self._transport = self.discover_service(self._transport_name, cls=self.transport_cls)
        self._scheduler = self.discover_service(self._scheduler, cls=Scheduler)
        self._closing = False
        self._task = self._scheduler.schedule_task(
            self._renew_keys,
            self._refresh_interval,
            name=f'scheduled:{self.service_name}._renew_keys',
            policy=self._scheduler.ExecPolicy.WAIT,
        )
        self._keys = {}

    async def close(self):
        """Close."""
        self._closing = True
        self._task.enabled = False

    async def wait(self, key: str, timeout: float = None):
        """Wait for a lock and return when it's released.

        :param key: lock key name
        :param timeout: optional max wait time in seconds

        :raises LockAcquireTimeout: when timeout reached
        :raises LockError: any internal error
        """
        t, _key = 0, self._create_key(key)
        while 1:
            if key in self._keys or _key in (await self._check_exists([_key])):
                self.logger.debug('wait', key=_key)
                await asyncio.sleep(self.WAIT_RELEASE_REFRESH_INTERVAL)
                t += self.WAIT_RELEASE_REFRESH_INTERVAL
                if timeout and t > timeout:
                    raise LockAcquireTimeout(StatusCodes.LOCK_ACQUIRE_TIMEOUT, code=StatusCodes.LOCK_ACQUIRE_TIMEOUT)
            else:
                break

    async def acquire(self, key: str, identifier: str = None, ttl: int = None, wait=True, timeout: float = None):
        """Wait for lock and acquire it.

        :param key: lock name
        :param identifier: service/owner identifier, if id is None then the app['id'] will be used
        :param ttl: optional ttl in seconds, None for eternal (until app exists)
        :param wait: wait for a lock to release (if False then it will raise a `LockError`
            if lock with such key already exists
        :param timeout: optional max wait time in seconds

        :raises LockExistsError:
        :raises LockAcquireTimeout: when timeout's reached
        :raises LockError: any internal error
        """

        def _wait():
            if wait:
                return asyncio.sleep(self.WAIT_RELEASE_REFRESH_INTERVAL)
            raise LockExistsError('Lock exists.', code=StatusCodes.LOCK_EXISTS)

        if identifier is None:
            identifier = self.app['id']

        t0, _key = 0, self._create_key(key)

        while 1:
            if ttl is None:
                new_ttl = self.BASE_TTL
            else:
                new_ttl = min(self.BASE_TTL, int(ttl))

            t = int(time()) + 1

            if timeout and t0 > timeout:
                raise LockAcquireTimeout(StatusCodes.LOCK_ACQUIRE_TIMEOUT, code=StatusCodes.LOCK_ACQUIRE_TIMEOUT)

            t0 += self.WAIT_RELEASE_REFRESH_INTERVAL

            if self._closing:
                await _wait()
                continue

            if key in self._keys:
                _deadline = self._keys[key]
                if _deadline is None or _deadline > t:
                    await _wait()
                    continue
                else:
                    del self._keys[key]

            try:
                await self._acquire([_key], identifier, new_ttl)
            except LockExistsError:
                await _wait()
            except Exception as exc:
                raise LockError(
                    'An unexpected error acquiring a lock.', code=StatusCodes.RUNTIME_ERROR, base_exc=exc
                ) from exc
            else:
                self.logger.info('locked', key=_key)
                self._keys[key] = t + new_ttl if ttl else None
                break

    async def release(self, key: str, identifier: str):
        """Release a lock.

        :param key: lock name
        :param identifier: service/owner identifier
        :raises LockError: if the lock can't be released by this service
        """
        _key = self._create_key(key)
        self.logger.debug('releasing', key=_key)
        try:
            await self._release([_key], identifier)
        except NotALockOwnerError as exc:
            raise exc
        except Exception as exc:
            raise LockError(
                'An unexpected error releasing a lock.', code=StatusCodes.RUNTIME_ERROR, base_exc=exc
            ) from exc
        self.logger.info('released', key=_key)
        if key in self._keys:
            del self._keys[key]

    async def owner(self, key: str) -> Optional[str]:
        """Return a current lock owner identifier or None if not found / has no owner."""
        key = self._create_key(key)
        owner = await self._owner(key)
        return owner

    async def is_owner(self, key: str) -> bool:
        """Return `True` if the current instance is an owner of this lock."""
        owner = await self._owner(key)
        return str(owner) == str(self.app['id'])

    @abc.abstractmethod
    async def _check_exists(self, keys: list) -> frozenset:
        """Check if locks with such keys exist. Return a set of existing keys."""

    @abc.abstractmethod
    async def _acquire(self, keys: list, identifier: str, ttl: int):
        """Set a list of specified keys. Also keep in mind that the operation must be atomic or transactional.

        :param keys: a list of keys
        :param identifier: key value
        :param ttl: key ttl in sec
        :raises `LockExistsError` if lock exists
        """

    @abc.abstractmethod
    async def _release(self, keys: list, identifier: str):
        """Release lock.

        Must raise `NotALockOwnerError` if identifier doesn't match the stored one.
        Also keep in mind that the operation must be atomic or transactional.
        """

    @abc.abstractmethod
    async def _renew(self, keys: list, values: list):
        """Renew keys TTLs with the new provided values (in sec)."""

    @abc.abstractmethod
    async def _owner(self, key: str):
        """Return a key owner or None if there's no key or owner."""

    def _create_key(self, key: str):
        keys = (self.app.env, self._namespace, self.PREFIX, key)
        return self.DELIMITER.join((k for k in keys if k))

    async def _renew_keys(self):
        """Renews existing locks."""
        t = int(time()) + 1
        keys, values, to_remove = [], [], []

        for key, deadline in self._keys.items():
            if deadline is None:
                keys.append(self._create_key(key))
                values.append(self.BASE_TTL)
            elif deadline <= t:
                to_remove.append(key)
            else:
                keys.append(self._create_key(key))
                ttl = min(deadline - t, self.BASE_TTL)
                values.append(ttl)

        for key in to_remove:
            del self._keys[key]

        if keys:
            await self._renew(keys, values)
