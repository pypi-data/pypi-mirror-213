import logging
from pathlib import Path
from time import time
from typing import *

from aiohttp import BasicAuth
from aiohttp.client import ClientSession, TCPConnector, ClientResponseError
from aiohttp.cookiejar import CookieJar

from kaiju_tools.rpc.client import BaseRPCClientService
from kaiju_tools.rpc.jsonrpc import RPCRequest
from kaiju_tools.exceptions import HTTPRequestError
from kaiju_tools.services import ContextableService
from kaiju_tools.serialization import dumps, loads

__all__ = ['HTTPService', 'RPCClientService']


class HTTPService(ContextableService):
    """HTTP transport."""

    UPLOAD_CHUNK_SIZE = 4096 * 1024

    def __init__(
        self,
        app,
        *,
        host: str = 'http://localhost:80',
        headers: dict = None,
        session: ClientSession = None,
        conn_settings: dict = None,
        auth: Union[dict, str] = None,
        cookie_settings: dict = None,
        request_logs: bool = False,
        response_logs: bool = False,
        logger: logging.Logger = None,
    ):
        """Initialize.

        :param app:
        :param host: full hostname
        :param headers: default request headers
        :param session: session object
        :param conn_settings: session connection settings
        :param auth: basic auth settings — "login", "password" and
            (optional) "encoding" (ignored if a session has been passed)
            or pass a single string which goes directly into the authorization header.
        :param cookie_settings:
        :param response_logs: log responses
        :param logger: a logger for a super class
        :param request_logs: enable request logs
        """
        super().__init__(app=app, logger=logger)
        self.host = host.rstrip('/')
        if session is None:
            if headers is None:
                headers = {}
            if isinstance(auth, str):
                headers['Authorization'] = auth
                auth = None
            elif isinstance(auth, dict):
                auth = BasicAuth(**auth)
            if cookie_settings is None:
                cookie_settings = {}
            if conn_settings is None:
                conn_settings = {}
            connector = TCPConnector(verify_ssl=False, limit=256, ttl_dns_cache=60)
            session = ClientSession(
                connector=connector,
                cookie_jar=CookieJar(**cookie_settings),
                headers=headers,
                json_serialize=dumps,
                raise_for_status=False,
                auth=auth,
                **conn_settings,
            )
        self.session = session
        self._request_logs = request_logs
        self._response_logs = response_logs

    async def init(self):
        pass

    async def close(self):
        if not self.closed:
            await self.session.close()

    async def upload_file(self, uri: str, file: Union[Path, str], method: str = 'post', chunk_size=UPLOAD_CHUNK_SIZE):
        """Upload file to a remote location."""
        """Upload a file."""

        def _read_file(path):
            with open(path, 'rb') as f:
                chunk = f.read(chunk_size)
                while chunk:
                    yield chunk
                    chunk = f.read(chunk_size)

        if type(file) is str:
            file = Path(file)
        result = await self.request(method=method, uri=uri, data=_read_file(file))
        return result

    async def request(
        self,
        method: str,
        uri: str,
        *args,
        data=None,
        json=None,
        params=None,
        headers=None,
        accept_json: bool = True,
        **kws,
    ) -> dict:
        """Make a http rest request."""
        url = self.resolve(uri)
        if params:
            params = {str(k): str(v) for k, v in params.items()}
        if self._request_logs:
            record = json if json else '[BYTES]'
            self.logger.info('Request', method=method, url=url, params=params, body=record)
        if headers:
            headers = {k: str(v) for k, v in headers.items()}
        t0 = time()
        async with self.session.request(
            method,
            url,
            params=params,
            headers=headers,
            data=data,
            cookies=self.session.cookie_jar._cookies,  # noqa ? pycharm
            json=json,
            **kws,
        ) as response:
            response.encoding = 'utf-8'
            text = await response.text()
            t = int((time() - t0) * 1000)
            if response.status >= 400:
                try:
                    text = loads(text)
                except ValueError:
                    text = None
                exc = ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                )
                exc.params = params
                exc.took_ms = t
                exc.request = json if json else None
                exc.response = text
                raise HTTPRequestError(base_exc=exc, message='HTTP request error')

        if text is not None and accept_json:
            text = loads(text)
        if self._response_logs:
            self.logger.info(
                'Response',
                method=method,
                url=url,
                params=params,
                status=response.status,
                body=text if accept_json else '[BYTES]',
                took_ms=t,
            )
        return text

    def resolve(self, uri: str) -> str:
        return f"{self.host}/{uri.lstrip('/')}"


class RPCClientService(BaseRPCClientService):
    """HTTP JSONRPC client service."""

    transport_cls = HTTPService
    _transport: HTTPService

    async def _request(self, body: Union[RPCRequest, List[RPCRequest]], headers: dict):
        """Make a HTTP request."""
        return await self._transport.request('post', self.base_uri, json=body, headers=headers)
