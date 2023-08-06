import abc
import asyncio
from typing import Union, Optional

from kaiju_tools.services import ContextableService, Service
from kaiju_tools.encoding.etc import MimeTypes
from kaiju_tools.encoding.serializers import serializers
from kaiju_tools.functions import RETRY_EXCEPTION_CLASSES

__all__ = ['CacheServiceInterface', 'BaseCacheService']


class CacheServiceInterface(abc.ABC):
    """Shared cache service public methods."""

    @abc.abstractmethod
    async def exists(self, key: str, ignore_conn_errors=False) -> bool:
        """Check if key is present in the cache."""

    @abc.abstractmethod
    async def m_exists(self, keys: list, ignore_conn_errors=False) -> frozenset:
        """Return a set of existing keys."""

    @abc.abstractmethod
    async def get(self, key: str, use_serializer=True, ignore_conn_errors=False) -> Optional:
        """Get value of a key or None if not found."""

    @abc.abstractmethod
    async def m_get(self, keys: list, use_serializer=True, ignore_conn_errors=False) -> dict:
        """Get value of multiple keys."""

    @abc.abstractmethod
    async def set(self, key: str, value, ttl: int = 0, use_serializer=True, ignore_conn_errors=False, nowait=True):
        """Set a single key at once."""

    @abc.abstractmethod
    async def m_set(self, keys: dict, ttl: int = 0, use_serializer=True, ignore_conn_errors=False, nowait=True):
        """Set one or multiple keys at once."""

    @abc.abstractmethod
    async def delete(self, key: str, ignore_conn_errors=False, nowait=True):
        """Remove one key at once."""

    @abc.abstractmethod
    async def m_delete(self, keys: list, ignore_conn_errors=False, nowait=True):
        """Remove multiple keys at once."""


class BaseCacheService(ContextableService, CacheServiceInterface, abc.ABC):
    """Base class for all shared cache services.

    Implements `CacheServiceInterface` interface.
    """

    service_name = 'cache'

    DELIMITER = ':'  #: used for delimiting sections in a key
    CONNECTION_ERROR_CLASSES = RETRY_EXCEPTION_CLASSES

    # defaults

    DEFAULT_TTL = 0
    PREFIX = 'cache'
    DEFAULT_SERIALIZER_TYPE = MimeTypes.msgpack
    IGNORE_CONN_ERRORS = False
    NOWAIT = True
    MAX_QUEUE_SIZE = 128
    PARALLEL_JOBS = 1

    transport_cls = None

    def __init__(
        self,
        app,
        transport: Union[str, Service] = None,
        namespace: str = None,
        default_ttl: int = DEFAULT_TTL,
        serializer_type: str = DEFAULT_SERIALIZER_TYPE,
        serializers=serializers,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param namespace: optional namespace (by default == app.name)
        :param transport: transport service (may be Redis, DB or similar)
        :param default_ttl:  default key lifetime in seconds (0 for infinite)
        :param serializer_type: you may specify a serializer type from `kaiju-tools.encoding`
        :param serializers: serializers registry with all serializers classes
        :param logger:
        """
        Service.__init__(self, app=app, logger=logger)
        self._namespace = namespace if namespace else app['name']
        self._transport_name = transport
        self._default_ttl = max(self.DEFAULT_TTL, int(default_ttl))
        self._serializer = serializers[serializer_type]()
        self._transport = None
        self._queue = None

    async def init(self):
        """Service context init."""
        self._transport = self.discover_service(self._transport_name, cls=self.transport_cls)

    async def exists(self, key: str, ignore_conn_errors=IGNORE_CONN_ERRORS) -> bool:
        """Check if key is present in the cache."""
        _key = self._create_key(key)
        result = await self._wrap_exec(self._exists(_key), ignore_conn_errors)
        if result is None:
            self.logger.info('key not found', key=_key)
        return bool(result)

    async def _exists(self, key: str) -> bool:
        """Check if such key present and has not expired."""

    async def m_exists(self, keys: list, ignore_conn_errors=IGNORE_CONN_ERRORS) -> frozenset:
        """Return a set of existing keys."""
        _keys = (self._create_key(key) for key in keys)
        self.logger.debug('m_exists', num_keys=len(keys))
        results = await self._wrap_exec(self._m_exists(*_keys), ignore_conn_errors)
        if results:
            return frozenset(key for key, result in zip(keys, results) if bool(result))
        else:
            return frozenset()

    @abc.abstractmethod
    async def _m_exists(self, *keys: str) -> list:
        """Return a list of 0 and 1 (0 for not existing True for existing)."""

    async def get(self, key: str, use_serializer=True, ignore_conn_errors=IGNORE_CONN_ERRORS):
        """Get value of a key or None if not found.

        :param key: string only
        :param use_serializer: to use serializer for value decoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        """
        _key = self._create_key(key)
        self.logger.debug('get', key=_key)
        value = await self._wrap_exec(self._get(_key), ignore_conn_errors)
        value = self._load_value(value, use_serializer)
        if value is None:
            self.logger.info('key not found', key=_key)
        return value

    @abc.abstractmethod
    async def _get(self, key: str) -> Optional:
        """Return a key value or None if not found."""

    async def m_get(self, keys: list, use_serializer=True, ignore_conn_errors=IGNORE_CONN_ERRORS) -> dict:
        """Get values of multiple keys.

        :param keys: list of keys
        :param use_serializer: use a serializer for value decoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        """
        _keys = [self._create_key(key) for key in keys]
        self.logger.debug('m_get', num_keys=len(keys))
        values = await self._wrap_exec(self._m_get(*_keys), ignore_conn_errors)
        if values:
            result = {k: self._load_value(v, use_serializer) for k, v in zip(keys, values) if v}
        else:
            result = {}
        return result

    @abc.abstractmethod
    async def _m_get(self, *keys: str) -> list:
        """Return a list of values for given keys."""

    async def set(
        self,
        key: str,
        value,
        ttl: int = None,
        use_serializer=True,
        ignore_conn_errors=IGNORE_CONN_ERRORS,
        nowait=NOWAIT,
    ):
        """Set a single key.

        :param key: string only
        :param value: any serializable value
        :param ttl: key lifetime in seconds, 0 for infinite, None for default
        :param use_serializer: use a serializer for value encoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        :param nowait: set operation in background (don't wait for response)
        """
        if ttl is None:
            _ttl = self._default_ttl
        else:
            _ttl = ttl
        _key = self._create_key(key)
        self.logger.info('set', key=_key, ttl=ttl)
        value = self._dump_value(value, use_serializer)
        _task = self._wrap_exec(self._set(_key, value, _ttl), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _set(self, key: str, value, ttl: int):
        """Set a key value with ttl in sec (0 for infinite)."""

    async def m_set(
        self, keys: dict, ttl: int = None, use_serializer=True, ignore_conn_errors=IGNORE_CONN_ERRORS, nowait=NOWAIT
    ):
        """Set multiple keys.

        :param keys: <key>: <value>
        :param ttl: lifetime in seconds, 0 for infinite, None for default
        :param use_serializer: use a serializer for value encoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        :param nowait: set operation in background (don't wait for response)
        """
        if ttl is None:
            _ttl = self._default_ttl
        else:
            _ttl = ttl
        key_dict = {self._create_key(k): self._dump_value(v, use_serializer) for k, v in keys.items()}
        self.logger.info('m_set', keys=keys, ttl=ttl)
        _task = self._wrap_exec(self._m_set(key_dict, _ttl), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _m_set(self, keys: dict, ttl: int):
        """Set multiple keys at once with ttl in sec (0 for inf)."""

    async def delete(self, key: str, ignore_conn_errors=IGNORE_CONN_ERRORS, nowait=NOWAIT):
        """Remove a key from cache."""
        _key = self._create_key(key)
        self.logger.info('delete', key=_key)
        _task = self._wrap_exec(self._delete(_key), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _delete(self, key: str):
        """Remove one key at once."""

    async def m_delete(self, keys: list, ignore_conn_errors=IGNORE_CONN_ERRORS, nowait=NOWAIT):
        """Remove multiple keys at once."""
        _keys = [self._create_key(key) for key in keys]
        self.logger.info('m_delete', keys=keys)
        _task = self._wrap_exec(self._m_delete(*_keys), ignore_conn_errors)
        if nowait:
            asyncio.create_task(_task)
        else:
            await _task

    @abc.abstractmethod
    async def _m_delete(self, *keys: str):
        """Remove multiple keys at once."""

    async def _wrap_exec(self, f, ignore_conn_errors: bool):
        try:
            return await f
        except tuple(self.CONNECTION_ERROR_CLASSES):
            if not ignore_conn_errors:
                raise

    def _create_key(self, key: str):
        keys = (self.app.env, self._namespace, self.PREFIX, key)
        return self.DELIMITER.join((k for k in keys if k))

    def _load_value(self, value, use_serializer: bool):
        if value is None:
            return
        elif use_serializer:
            return self._serializer.loads(value)
        else:
            return value

    def _dump_value(self, value, use_serializer: bool):
        if use_serializer:
            return self._serializer.dumps(value)
        else:
            return value
