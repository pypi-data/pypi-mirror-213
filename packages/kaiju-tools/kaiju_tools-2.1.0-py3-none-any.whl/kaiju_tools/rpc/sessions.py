import abc
import uuid
from datetime import datetime
from hashlib import blake2b
from secrets import randbits
from time import time
from typing import Optional, Union

from kaiju_tools.cache import BaseCacheService
from kaiju_tools.services import Session, Service
from kaiju_tools.exceptions import NotFound

__all__ = ['BaseSessionService']


class BaseSessionService(Service, abc.ABC):
    """Session store interface used by the rpc server."""

    service_name = 'sessions'
    session_key = 'session:{session_id}'
    session_cls = Session

    def __init__(
        self,
        app,
        cache_service: BaseCacheService = None,
        session_idle_timeout: int = 24 * 3600,
        exp_renew_interval: int = 3600,
        salt: str = 'SALT',
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param cache_service: cache service instance
        :param session_idle_timeout: (s) Idle lifetime for each session.
        :param exp_renew_interval: (s)
        :param salt: salt for user agent hashing, change it to invalidate all current sessions
        :param logger:
        """
        Service.__init__(self, app, logger=logger)
        self._cache: BaseCacheService = self.discover_service(cache_service, cls=BaseCacheService)
        self.session_idle_timeout = session_idle_timeout
        self.exp_renew_interval = exp_renew_interval
        self.salt = salt.encode('utf-8')

    def get_new_session(self, data: dict, *, user_agent: Union[str, bytes] = '') -> Session:
        """Create and return a new session (not stored yet).

        :param data: session data
        :param user_agent: user agent or client id or hash to match session in subsequent requests
        """
        h_agent = self._get_agent_hash(user_agent) if type(user_agent) is str else user_agent
        session = self._create_new_session(data, h_agent)
        self.logger.debug('new session', session_id=session.id)
        return session

    async def session_exists(self, session_id: str, /) -> bool:
        """Check if session exists in the session cache."""
        key = self._get_session_key(session_id)
        return await self._cache.exists(key)

    async def save_session(self, session: Session, /) -> None:
        """Save session to the storage.

        The session will be stored only if it is marked as stored, and it has been changed.
        Token-auth sessions and initial sessions without data won't be stored.
        """
        if not session or not session.stored:
            return

        key = self._get_session_key(session.id)
        exp = int(time()) + self.session_idle_timeout
        if session.changed:
            self.logger.info('saving session', session_id=session.id)
            key = self._get_session_key(session.id)
            await self._cache.set(key, session.repr(), ttl=exp, nowait=True)
            data = session.repr()
            data['expires'] = exp
            await self._save_session(data)
        elif session.loaded and session.expires - time() < self.exp_renew_interval:
            asyncio.create_task(self._cache._transport.expire(key, exp))  # noqa
            await self._update_session_exp(session.id, exp)

    @abc.abstractmethod
    async def _save_session(self, session_data: dict) -> None:
        """Save session in database backend."""

    @abc.abstractmethod
    async def _update_session_exp(self, session_id, exp) -> None:
        """Save session in database backend."""

    async def delete_session(self, session: Session, /) -> None:
        """Delete session from the storage."""
        if session and session.stored and session.loaded:
            self.logger.info('removing session', session_id=session.id)
            key = self._get_session_key(session.id)
            await self._cache.delete(key, nowait=True)
            try:
                await self._delete_session(session.id)
            except NotFound:
                pass

    @abc.abstractmethod
    async def _delete_session(self, session_id) -> None:
        """Delete session in database."""

    async def load_session(self, session_id: str, /, *, user_agent: str = '') -> Optional[Session]:
        """Load session from the storage.

        :param session_id: unique session id
        :param user_agent: user agent or client id for security purposes
        :return: returns None when session is not available
        """
        key = self._get_session_key(session_id)
        session = cached = await self._cache.get(key)
        if not session:
            try:
                session = await self._get_session(session_id)
            except NotFound:
                self.logger.info('session not found', session_id=session_id)
                return

            if session['expires'] < time():
                self.logger.debug('session expired', session_id=session_id)
                await self._cache.delete(key, nowait=True)
                await self._delete_session(session_id)
                return

        agent_hash = self._get_agent_hash(user_agent)
        session = self.session_cls(**session, _stored=True, _changed=False, _loaded=True)
        if session.h_agent != agent_hash:
            self.logger.info('user agent mismatch', session_id=session_id)
            return

        self.logger.debug('session loaded', session_id=session_id)
        if not cached:
            await self._cache.set(key, session.repr(), nowait=True)
        return session

    @abc.abstractmethod
    async def _get_session(self, session_id) -> dict:
        """Get session."""

    def _create_new_session(self, data: dict, h_agent: bytes) -> Session:
        """Create a new session object."""
        return self.session_cls(
            id=uuid.UUID(int=randbits(128)).hex,
            user_id=None,
            permissions=frozenset(),
            data=data,
            expires=int(time()) + self.session_idle_timeout,
            created=datetime.now(),
            h_agent=h_agent,
            _changed=bool(data),
            _stored=True,
            _loaded=False,
        )

    def _get_session_key(self, session_id: str) -> str:
        return self.session_key.format(session_id=session_id)

    def _get_agent_hash(self, user_agent: str) -> bytes:
        return blake2b(user_agent.encode('utf-8'), digest_size=16, salt=self.salt).digest()
