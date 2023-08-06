import abc
import logging
from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict, FrozenSet
from uuid import UUID
from contextvars import ContextVar  # noqa pycharm

from aiohttp.web import Application

from kaiju_tools.serialization import Serializable


class Scope(Enum):
    """Permission scope for application methods."""

    SYSTEM = 0
    ADMIN = 10
    USER = 100
    GUEST = 1000


SCOPE_MAP = {Scope.SYSTEM: 'system', Scope.ADMIN: 'admin', Scope.USER: 'user'}  # used by permission services


class Session(Serializable):
    """User session data."""

    __slots__ = ('id', 'h_agent', 'user_id', 'expires', 'permissions', 'data', 'created', '_stored', '_changed')

    def __init__(
        self,
        *,
        id: str,  # noqa
        h_agent: bytes,
        user_id: Optional[UUID],
        expires: int,
        permissions: FrozenSet[str],
        data: dict,
        created: datetime,
        _stored: bool,
        _changed: bool,
        _loaded: bool,
    ):
        """Initialize.

        :param id:
        :param h_agent:
        :param user_id:
        :param expires:
        :param permissions:
        :param data:
        :param created:
        :param _stored:
        :param _changed:
        :param _loaded:
        """
        self.id = id
        self.h_agent = h_agent
        self.user_id = user_id
        self.expires = expires
        self.permissions = frozenset(permissions)
        self.data = data
        self.created = created
        self._stored = _stored
        self._changed = _changed
        self._loaded = _loaded

    def __getitem__(self, item):
        return self.data.get(item)

    def __setitem__(self, key, value):
        self.update({key: value})

    @property
    def scope(self) -> Scope:
        """Base user scope."""
        if SCOPE_MAP[Scope.SYSTEM] in self.permissions:
            return Scope.SYSTEM
        elif SCOPE_MAP[Scope.USER] in self.permissions:
            return Scope.USER
        else:
            return Scope.GUEST

    @property
    def stored(self) -> bool:
        """Session should be stored."""
        return self._stored

    @property
    def changed(self) -> bool:
        """Session has changed."""
        return self._changed

    @property
    def loaded(self) -> bool:
        """Session has been loaded from db."""
        return self._loaded

    def update(self, data: dict):
        """Update session data."""
        self.data.update(data)
        self._changed = True

    def clear(self):
        """Clear all session data."""
        self.data.clear()
        self._changed = True

    def repr(self) -> dict:
        """Get object representation."""
        return {slot: getattr(self, slot) for slot in self.__slots__ if not slot.startswith('_')}


class RequestContext(TypedDict):
    """Request context stored for the request chain."""

    correlation_id: str
    session_id: Optional[str]
    request_deadline: Optional[int]


class ServiceConfig(TypedDict, total=False):
    """Service configuration parameters."""

    cls: str  #: service class name as in :py:class:`~kaiju_tools.services.service_class_registry`
    name: str  #: unique service name, each service should have a default value for this
    enabled: bool  #: disable service
    required: bool  #: skip a service and proceed on initialization error
    override: bool  #: replace an existing service with the same name
    settings: dict  #: custom settings, unpacked to a service's __init__


class App(Application):
    """Web application interface."""

    id: str
    name: str
    version: str
    env: str
    debug: bool
    loglevel: str
    logger: logging.Logger
    services: dict
    settings: dict

    def get_context(self) -> RequestContext:
        ...

    def get_session(self) -> Optional[Session]:
        ...


REQUEST_CONTEXT: ContextVar[Optional[RequestContext]] = ContextVar('RequestContext', default=None)
REQUEST_SESSION: ContextVar[Optional[Session]] = ContextVar('RequestSession', default=None)
