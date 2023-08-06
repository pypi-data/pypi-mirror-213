import pytest

from kaiju_tools.services import Service, RequestContext
from kaiju_tools.logging.services import LoggingService
from kaiju_tools.rpc.server import REQUEST_CONTEXT


class _TestService(Service):
    @staticmethod
    def _get_logger_ctx() -> dict:
        return {'request': REQUEST_CONTEXT}


@pytest.fixture
def logger_settings():
    return {'name': 'root', 'enabled': True, 'handlers': ['default'], 'loglevel': 'DEBUG'}


@pytest.fixture
def handler_settings():
    return {'cls': 'StreamHandler', 'name': 'default', 'enabled': True, 'settings': {}, 'loglevel': 'DEBUG'}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['formatter', 'settings'],
    [('TextFormatter', {}), ('DataFormatter', {'debug': False}), ('DataFormatter', {'debug': True})],
    ids=['Text', 'Data', 'Data (debug)'],
)
async def test_logging_service(application, logger_settings, handler_settings, formatter, settings):
    def _raise_exc():
        raise ValueError('Some error.')

    handler_settings['formatter'] = formatter
    handler_settings['formatter_settings'] = settings
    logging_service = LoggingService(
        app=application(), loggers=[logger_settings], handlers=[handler_settings], logger=None
    )
    REQUEST_CONTEXT.set(RequestContext(correlation_id='ffffffff', session_id=None, request_deadline=1000))
    service = _TestService(app=logging_service.app, logger=None)
    service.logger.debug('Testing DEBUG message %s.', 'test', extra_data=True)
    service.logger.info('Testing INFO message %s.', 'test', extra_data=True)
    service.logger.warning('Testing WARNING message %s.', 'test', extra_data=True)
    service.logger.error('Testing ERROR message %s.', 'test', extra_data=True)
    try:
        _raise_exc()
    except Exception as exc:
        service.logger.error('ERROR trace.', exc_info=exc)
