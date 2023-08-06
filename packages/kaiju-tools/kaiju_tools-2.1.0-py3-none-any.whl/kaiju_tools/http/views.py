import asyncio
from typing import cast

from aiohttp.web import Request, Response, View, json_response, WebSocketResponse, WSMsgType
from aiohttp.http_websocket import WSMessage
from aiohttp_cors import CorsViewMixin

from kaiju_tools.serialization import dumps, loads
from kaiju_tools.services import Scope, Session, ServiceContextManager
from kaiju_tools.rpc.sessions import BaseSessionService
from kaiju_tools.rpc.services import JSONRPCServer
from kaiju_tools.rpc.etc import JSONRPCHeaders

__all__ = ['JSONRPCView', 'jsonrpc_websocket_handler']


async def jsonrpc_websocket_handler(
    request: Request, rpc_server_name: str = None, session_service_name: str = None, validate_session: bool = True
):
    """Read from websocket."""
    ws = WebSocketResponse()
    counter = 0
    services: ServiceContextManager = request.app.services  # noqa
    rpc: JSONRPCServer = services.discover_service(rpc_server_name, cls=JSONRPCServer)
    sessions: BaseSessionService = services.discover_service(session_service_name, cls=BaseSessionService)
    session: Session = request.get('session', None)
    scope: Scope = session.scope if session else Scope.GUEST
    headers = dict(request.headers)

    async def _send_response(_session: Session, headers: dict, result):  # noqa
        nonlocal session, scope, request
        session = request['session'] = _session
        scope = session.scope
        await ws.send_json(result.repr(), dumps=dumps)

    await ws.prepare(request)

    try:
        async for msg in ws:
            msg = cast(WSMessage, msg)
            if msg.type == WSMsgType.ERROR:
                request.app.logger.error('Websocket error: %s', ws.exception())
            elif msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                    break

                if validate_session:
                    session_exists = await sessions.session_exists(session.id)
                    if not session_exists:
                        session = None  # noqa
                        del request['session']
                        await ws.close()
                        break

                data = loads(msg.data)
                counter += 1
                if 'id' not in data:
                    data['id'] = counter
                result = await rpc.call(
                    data, headers=headers, session=session, scope=scope, nowait=True, callback=_send_response
                )
                if type(result) is not asyncio.Task:
                    _headers, result = result
                    if result:
                        await ws.send_json(result, dumps=dumps)
    except Exception as exc:
        request.app.logger.error('Websocket error', exc_info=exc)

    finally:
        ws._headers[JSONRPCHeaders.SESSION_ID_HEADER] = session.id if session else ''  # noqa
        if not ws.closed:
            await ws.close()
        return ws


class JSONRPCView(CorsViewMixin, View):
    """JSON RPC server endpoint."""

    route = '/public/rpc'
    rpc_server_name = 'rpc'

    async def post(self):
        """Make an RPC request."""
        if not self.request.can_read_body:
            return Response()
        data = await self.request.text()
        session: Session = self.request.get('session', None)
        scope: Scope = session.scope if session else Scope.GUEST
        rpc: JSONRPCServer = getattr(self.request.app.services, self.rpc_server_name)  # noqa
        headers, result = await rpc.call(
            loads(data), headers=dict(self.request.headers), session=session, scope=scope, nowait=False
        )
        return json_response(result, headers=headers, dumps=dumps)
