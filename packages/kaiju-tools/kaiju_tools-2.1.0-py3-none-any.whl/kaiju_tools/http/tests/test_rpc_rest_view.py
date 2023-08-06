from types import SimpleNamespace
from uuid import uuid4

import pytest

from ...serialization import dumps, loads
from ...rpc.tests.fixtures import *
from ...rpc.etc import JSONRPCHeaders
from ..views import JSONRPCView


@pytest.mark.asyncio
async def test_rpc_rest_view(rpc_interface, aiohttp_client, application, rpc_compatible_service, logger):

    logger.info('Testing service context initialization.')
    application = application()

    async with rpc_interface as rpc:
        service = rpc_compatible_service(logger=logger)
        rpc.register_service(service.service_name, service)
        application.router.add_view(JSONRPCView.route, JSONRPCView)
        application.services = SimpleNamespace(rpc=rpc)
        client = await aiohttp_client(application)

        logger.info('Testing basic functionality.')

        app_id = uuid4()
        correlation_id = uuid4()
        headers = {
            JSONRPCHeaders.APP_ID_HEADER: str(app_id),
            JSONRPCHeaders.CORRELATION_ID_HEADER: str(correlation_id),
            'Content-Type': 'application/json',
        }
        data = {'id': uuid4().int, 'method': 'm.echo', 'params': {'a': 1, 'b': 2, 'c': 3}}
        data = dumps(data)
        response = await client.post(JSONRPCView.route, data=data, headers=headers)
        assert response.status == 200
        text = await response.text()
        body = loads(text)
        logger.info(body)
        assert body['result'][1] == {'a': 1, 'b': 2, 'c': 3}

        logger.info('Testing batch functionality.')

        headers = {
            JSONRPCHeaders.APP_ID_HEADER: str(app_id),
            JSONRPCHeaders.CORRELATION_ID_HEADER: str(correlation_id),
            'Content-Type': 'application/json',
        }
        data = [
            {'id': uuid4().int, 'method': 'm.echo', 'params': {'a': 1}},
            {'id': uuid4().int, 'method': 'm.echo', 'params': None},
            {'id': uuid4().int, 'method': 'm.echo'},
        ]
        headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = str(uuid4())
        data = dumps(data)
        response = await client.post(JSONRPCView.route, data=data, headers=headers)
        assert response.status == 200
        text = await response.text()
        body = loads(text)
        logger.info(body)
        assert [r['result'] for r in body] == [[[], {'a': 1}], [[], {}], [[], {}]]
        logger.info('All tests finished.')
