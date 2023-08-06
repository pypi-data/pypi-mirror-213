from aiohttp.web import middleware, json_response, Request
from aiohttp.web_exceptions import HTTPClientError

from kaiju_tools.exceptions import InternalError, ClientError
from kaiju_tools.rpc.jsonrpc import RPCError
from kaiju_tools.serialization import dumps

__all__ = ['error_middleware']


@middleware
async def error_middleware(request: Request, handler):
    """Wrap an error in RPC exception."""
    try:
        response = await handler(request)
    except HTTPClientError as exc:
        error = ClientError(message=str(exc), base_exc=exc)
        request.app.logger.error(str(exc))
        return json_response(RPCError(id=None, error=error), dumps=dumps)
    except Exception as exc:
        error = InternalError(message='Internal error', base_exc=exc)
        request.app.logger.error(str(exc), exc_info=exc)
        return json_response(RPCError(id=None, error=error), dumps=dumps)
    else:
        return response
