import abc
from typing import List, Union, Any

from kaiju_tools.functions import get_short_uid
from kaiju_tools.services import ContextableService, Service
from kaiju_tools.rpc.abc import AbstractRPCCompatible
from kaiju_tools.rpc.etc import JSONRPCHeaders
from kaiju_tools.rpc.jsonrpc import RPCRequest
from kaiju_tools.exceptions import APIException

__all__ = ('RPCClientError', 'BaseRPCClientService')


class RPCClientError(APIException):
    """JSON RPC Python exception class."""

    def __init__(self, *args, response=None, **kws):
        super().__init__(*args, **kws)
        self.response = response

    def __str__(self):
        return self.message


class BaseRPCClientService(ContextableService, AbstractRPCCompatible, abc.ABC):
    """JSONRPC client."""

    transport_cls = Service

    def __init__(self, app, transport: str, uri: str = '/public/rpc', logger=None):
        super().__init__(app=app, logger=logger)
        self.base_uri = uri
        self._transport = transport

    async def init(self):
        self._transport = self.discover_service(self._transport, cls=self.transport_cls)

    async def call(
        self,
        method: str,
        params: Union[dict, None] = None,
        nowait: bool = False,
        request_id: int = 0,
        max_timeout: int = None,
        use_context: bool = True,
    ) -> Union[Any, None]:
        """Make an RPC call.

        :param method: rpc method name
        :param params: method call arguments
        :param nowait: create a 'notify' request - do not wait for the result
        :param request_id: optional request id (usually you don't need to set it)
        :param max_timeout: request timeout in sec
        :param use_context: use app request context such as correlation id and request chain deadline
        """
        headers = self._create_request_headers(max_timeout, use_context, nowait)
        _id = None if nowait else request_id
        body = RPCRequest(id=_id, method=method, params=params)
        response = await self._request(body, headers)
        result = self._process_response(response)
        if isinstance(result, Exception):
            raise result
        return result

    async def call_multiple(
        self,
        *requests: dict,
        raise_exception: bool = True,
        nowait: bool = False,
        max_timeout: int = None,
        use_context: bool = True,
    ) -> Union[List, None]:
        """Make an RPC batch call.

        :param requests: list of request dicts
        :param nowait: create a 'notify' request - do not wait for the result
        :param max_timeout: request timeout in sec
        :param use_context: use app request context such as correlation id and request chain deadline
        :param raise_exception: raise exception instead of returning error objects in the list
        """
        headers = self._create_request_headers(max_timeout, use_context, nowait)
        body = [RPCRequest(id=n, **req) for n, req in enumerate(requests)]
        response = await self._request(body, headers)
        if response is None:  # for notify requests
            return
        results = []
        for resp in response:
            resp = self._process_response(resp)
            if isinstance(resp, Exception) and raise_exception:
                raise resp
            results.append(resp)
        return results

    @abc.abstractmethod
    async def _request(self, body: Union[RPCRequest, List[RPCRequest]], headers: dict):
        """Make an external requests via transport service."""

    def _create_request_headers(self, max_timeout, use_context, nowait) -> dict:
        headers = {}
        ctx = self.get_request_context() if use_context else None
        if ctx:
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = ctx['correlation_id']
            if not nowait:
                headers[JSONRPCHeaders.REQUEST_DEADLINE_HEADER] = ctx['request_deadline']
        else:
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = get_short_uid()
        if max_timeout:
            headers[JSONRPCHeaders.REQUEST_TIMEOUT_HEADER] = max_timeout
        return headers

    def _process_response(self, response: dict):
        if 'error' in response:
            return self._create_exception(response['error'])
        else:
            return response['result']

    @staticmethod
    def _create_exception(error_data: dict) -> RPCClientError:
        exc = RPCClientError(message=error_data['message'], data=error_data['data'])
        exc.status_code = error_data['code']
        return exc
