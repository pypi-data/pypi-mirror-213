from types import SimpleNamespace

import pytest

from ...rpc.tests.fixtures import *
from ...http.client import RPCClientService
from ..client import HTTPService
from ..views import JSONRPCView


@pytest.mark.asyncio
async def test_rpc_http_client(rpc_interface, aiohttp_server, application, rpc_compatible_service, logger):
    port = 7677
    application = application(debug=True)

    async with rpc_interface as rpc:
        service = rpc_compatible_service(logger=logger)
        rpc.register_service('do', service)
        application.router.add_view(JSONRPCView.route, JSONRPCView)
        application.services = SimpleNamespace(rpc=rpc)
        server = await aiohttp_server(application, port=port)

        try:
            async with HTTPService(application, host=f'http://localhost:{port}', logger=logger) as http_client:
                async with RPCClientService(
                    app=None, transport=http_client, uri=JSONRPCView.route, logger=logger
                ) as client:
                    args, kws = await client.call('do.echo', {'value': True})
                    assert kws['value']

                    result = await client.call_multiple(
                        {'method': 'do.echo', 'params': {'value': 1}},
                        {'method': 'do.echo', 'params': {'value': 2}},
                        {'method': 'do.echo', 'params': {'value': 3}},
                    )

                    assert [r[1]['value'] for r in result] == [1, 2, 3]

        finally:
            await server.close()
