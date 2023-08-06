import pytest

from ..services import *


@pytest.mark.asyncio
async def test_service_context_manager_basic_functions(aiohttp_server, application, logger):
    class SimpleUnnamedService(Service):
        def __init__(self, x, *args, **kws):
            super().__init__(*args, **kws)
            self.x = x

        def __call__(self, *args, **kwargs):
            return self.x

    class SimpleUnnamedServiceWithDefaults(Service):
        def __init__(self, x, *args, **kws):
            super().__init__(*args, **kws)
            self.x = x

        def __call__(self, *args, **kwargs):
            return self.x

    class _ContextableService(ContextableService):

        service_name = 'contextable_service'

        def __init__(self, x, *args, **kws):
            super().__init__(*args, **kws)
            self.x = x
            self.y = None

        def closed(self) -> bool:
            return self.y is None

        async def init(self):
            self.y = self.x

        async def close(self):
            self.y = None

        def call(self, *args, **kwargs):
            return self.y

    class ContextableFailedService(_ContextableService):

        service_name = 'contextable_failed'

        def __init__(self, *args, **kws):
            super().__init__(*args, **kws)
            self.y = 42

        async def init(self):
            raise ValueError()

    class ContextableDoubleFailedService(ContextableFailedService):

        service_name = 'contextable_double_failed'

        async def close(self):
            raise ValueError()

    settings = [
        {'cls': 'SimpleUnnamedService', 'settings': {'x': 42}},
        {'cls': 'SimpleUnnamedServiceWithDefaults', 'settings': {'x': 42}},
        {'cls': 'SimpleUnnamedService', 'name': 'another_simple_unnamed', 'settings': {'x': 43}},
        {'cls': '_ContextableService', 'settings': {'x': 44}},
        {'cls': 'ContextableFailedService', 'required': False, 'settings': {'x': 44}},
        {'cls': 'ContextableDoubleFailedService', 'required': False, 'settings': {'x': 44}},
        {'cls': 'SimpleUnnamedService', 'name': 'unregistered', 'settings': {'x': 42}},
    ]

    application = application()
    registry = ServiceClassRegistry()
    registry.register_classes_from_namespace(locals())

    manager = ServiceContextManager(application, class_registry=registry, settings=settings, logger=logger)
    application.services = manager

    # testing app initialization

    application.cleanup_ctx.append(manager.cleanup_context)
    await aiohttp_server(application)

    # checking all services are OK
    assert application.services.SimpleUnnamedService() == 42
    assert application.services.another_simple_unnamed() == 43
    assert application.services.contextable_service.call() == 44
