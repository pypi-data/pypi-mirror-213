import abc
from contextvars import ContextVar  # noqa pycharm?
from typing import Union

from kaiju_tools.services import Session, Scope, RequestContext

from .context import REQUEST_CONTEXT, REQUEST_SESSION

__all__ = ('AbstractRPCCompatible', 'PermissionKeys', 'AbstractTokenInterface')


class PermissionKeys:
    """Permission scopes."""

    GLOBAL_SYSTEM_PERMISSION = Scope.SYSTEM
    GLOBAL_USER_PERMISSION = Scope.USER
    GLOBAL_GUEST_PERMISSION = Scope.GUEST


class AbstractRPCCompatible(abc.ABC):
    """Class with an RPC interface."""

    DEFAULT_PERMISSION = '*'
    PermissionKeys = PermissionKeys

    @staticmethod
    def get_session() -> Union[Session, None]:
        """Get current user session."""
        return REQUEST_SESSION.get()

    @staticmethod
    def get_request_context() -> Union[RequestContext, None]:
        """Get current user request context."""
        return REQUEST_CONTEXT.get()

    def get_user_id(self):
        """Return current session user id."""
        session = self.get_session()
        return session.user_id if session else None

    def has_permission(self, permission: str) -> bool:
        """Check  if a user session has a particular permission."""
        session = self.get_session()
        return permission in session.permissions or self.system_user() if session else True

    def system_user(self) -> bool:
        """Check if user session has the system scope."""
        session = self.get_session()
        return PermissionKeys.GLOBAL_SYSTEM_PERMISSION.value >= session.scope.value if session else None

    @property
    def routes(self) -> dict:
        """List RPC routes."""
        return {}

    @property
    def permissions(self) -> dict:
        """List RPC routes permissions."""
        return {}

    @property
    def validators(self) -> dict:
        """List of RPC routes validation schemas."""
        return {}


class AbstractTokenInterface(abc.ABC):
    """Describes a token provider service methods to be able to be used by the :class:`.AbstractRPCClientService`."""

    @abc.abstractmethod
    async def get_token(self) -> str:
        """Must always return a valid auth token."""
