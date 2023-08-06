import asyncio

import uuid
from typing import *

import pytest

from ..abc import AbstractRPCCompatible
from ..services import JSONRPCServer
from ...services import Service
from ...logging.types import Logger

from ... import jsonschema as j
from ...exceptions import ValidationError


@pytest.fixture
def rpc_interface(application, logger):
    app = application(debug=True)
    return JSONRPCServer(app=app, session_service=False, logger=logger)


@pytest.fixture
def rpc_compatible_service():
    class TestService(Service, AbstractRPCCompatible):
        service_name = 'm'

        def __init__(self, *args, **kws):
            super().__init__(*args, **kws)
            self.retry_counter = 0

        @property
        def validators(self) -> dict:
            return {'validated': j.Object({'a': j.Integer(), 'b': j.Integer()}, required=['a', 'b'])}

        @property
        def permissions(self) -> Optional[dict]:
            return {
                '*': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
                'method_with_user_permission': self.PermissionKeys.GLOBAL_USER_PERMISSION,
                'method_with_user_permission_2': self.PermissionKeys.GLOBAL_USER_PERMISSION,
            }

        @property
        def routes(self) -> dict:
            return {
                'echo': self.echo,
                'aecho': self.async_echo,
                'sum': self.sum,
                'fail': self.failed,
                'long_echo': self.async_long_echo,
                'split': self.split,
                'standard_echo': self.async_standard_echo,
                'validated': self.validated_method,
                'uses_context': self.uses_context,
                'method_with_user_permission': self.echo_true,
                'method_with_user_permission_2': self.echo_true,
                'method_with_retry': self.retry_method,
            }

        async def retry_method(self, when: int) -> bool:
            self.retry_counter += 1
            if self.retry_counter < when:
                raise TimeoutError('Simulated timeout')
            self.retry_counter = 0
            return True

        async def echo_true(self, *args, **kws):
            return True

        async def uses_context(self):
            """Check if a session matches the context."""
            return await self._uses_context()

        async def _uses_context(self):
            await asyncio.sleep(0.1)
            stored_session = self.get_session()
            return stored_session

        async def sum(self, x: float, y: float) -> float:
            """Sum something.

            :param x: first value
            :example x: 7
            :param y: second value
            :example y: 6
            :returns: sum of two values
            """
            return x + y

        async def split(self, value: str, delimiter: str) -> List[str]:
            """Split a string value by delimiter.

            :returns: split parts
            """
            return value.split(delimiter)

        async def failed(self):
            """Do wrong command."""
            raise ValueError('Something bad happened.')

        async def echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing echo.')
            return args, kws

        async def async_echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing async echo.')
            await asyncio.sleep(0.01)
            return args, kws

        async def async_standard_echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing echo.')
            await asyncio.sleep(0.01)
            return args, kws

        async def async_long_echo(self, *args, **kws):
            """Echo command which accepts any arguments."""
            self.logger.info('Executing long echo.')
            await asyncio.sleep(2.2)
            return args, kws

        async def validated_method(self, a: int, b: int):
            """Call a method with a validated input."""
            return a * b

    return TestService


@pytest.fixture
def user_session():
    return {'user_id': uuid.uuid4(), 'permissions': [AbstractRPCCompatible.PermissionKeys.GLOBAL_USER_PERMISSION]}


@pytest.fixture
def admin_session():
    return {'user_id': uuid.uuid4(), 'permissions': [AbstractRPCCompatible.PermissionKeys.GLOBAL_SYSTEM_PERMISSION]}


@pytest.fixture
def guest_session():
    return {'user_id': uuid.uuid4(), 'permissions': [AbstractRPCCompatible.PermissionKeys.GLOBAL_GUEST_PERMISSION]}
