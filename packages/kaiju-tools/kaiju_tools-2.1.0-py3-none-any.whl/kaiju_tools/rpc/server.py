import asyncio
import os
import warnings
from binascii import b2a_hex
from fnmatch import fnmatch
from time import time
from typing import cast, List, Union, TypedDict, Callable, Dict, Optional, Tuple, Awaitable, NewType

import fastjsonschema  # type: ignore

from kaiju_tools.rpc.abc import AbstractRPCCompatible
from kaiju_tools.rpc.etc import JSONRPCHeaders
from kaiju_tools.rpc.sessions import BaseSessionService
from kaiju_tools.rpc.jsonrpc import RPCError, RPCResponse, JSONRPC
from kaiju_tools.functions import timeout, retry
from kaiju_tools.templates import Template
from kaiju_tools.exceptions import (
    APIException,
    RequestTimeout,
    InternalError,
    InvalidRequest,
    InvalidParams,
    Aborted,
    MethodNotFound,
    PermissionDenied,
    JSONRPCError,
    ClientError,
)
from kaiju_tools.services import ContextableService, RequestContext, Session, Scope
from kaiju_tools.jsonschema import compile_schema
from .context import REQUEST_CONTEXT, REQUEST_SESSION
from .annotations import AnnotationParser, FunctionAnnotation

__all__ = ['RequestHeaders', 'MethodInfo', 'JSONRPCServer']


_RequestId = NewType('_RequestId', Union[int, None])


class _Task(asyncio.Task):
    deadline: int
    started: int


class _Aborted(APIException):
    pass


class RequestHeaders(TypedDict):
    """Request headers acknowledged by the server."""

    correlation_id: str
    request_deadline: int
    abort_on_error: bool
    use_template: bool
    retries: int


class MethodInfo(TypedDict):
    """Stored method data."""

    f: Callable
    signature: FunctionAnnotation
    service_name: str
    permission: Scope
    validator: Callable


class JSONRPCServer(ContextableService, AbstractRPCCompatible):
    """A simple JSON RPC interface with method execution and management tasks."""

    service_name = 'rpc'
    _permission_levels = {
        AbstractRPCCompatible.PermissionKeys.GLOBAL_SYSTEM_PERMISSION: Scope.SYSTEM,
        AbstractRPCCompatible.PermissionKeys.GLOBAL_USER_PERMISSION: Scope.USER,
        AbstractRPCCompatible.PermissionKeys.GLOBAL_GUEST_PERMISSION: Scope.GUEST,
    }

    def __init__(
        self,
        app,
        *,
        session_service: BaseSessionService = None,
        max_parallel_tasks: int = 64,
        default_request_time: int = 120,
        max_request_time: int = 600,
        enable_permissions: bool = True,
        request_logs: bool = False,
        response_logs: bool = False,
        blacklist_routes: List[str] = None,
        blacklist_scope: int = Scope.SYSTEM.value - 1,
        use_annotation_parser: bool = True,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param session_service: session backend
        :param max_parallel_tasks: max number of tasks in the loop
        :param default_request_time: default request time in seconds if not specified by a header
        :param max_request_time: maximum allowed request time in seconds
        :param enable_permissions: enable perm checks in requests
        :param request_logs: log request body and also log responses (even successful ones)
        :param blacklist_routes: wildcard patterns to blacklist certain RPC routes
        :param blacklist_scope: integer value to blacklist permission scopes lower or equal to this value
        :param use_annotation_parser: annotation parser for non-validated method will be used and will try to
            create a method validator from its annotations
        :param logger:
        """
        ContextableService.__init__(self, app=app, logger=logger)
        self._sessions = session_service
        self._max_parallel_tasks = max(1, int(max_parallel_tasks))
        self._default_request_time = max(1, int(default_request_time))
        self._max_request_time = max(self._default_request_time, int(max_request_time))
        self._enable_permissions = enable_permissions
        self._debug = self.app.debug
        self._request_logs = request_logs
        self._response_logs = response_logs
        self._blacklist_routes = blacklist_routes if blacklist_routes else []
        self._blacklist_scope = blacklist_scope
        self._use_annotation_parser = use_annotation_parser
        self._counter = self._max_parallel_tasks
        self._not_full = asyncio.Event()
        self._not_full.set()
        self._empty = asyncio.Event()
        self._empty.set()
        self._methods: Dict[str, MethodInfo] = {}

    async def init(self):
        if not self._enable_permissions:
            warnings.warn('Server permissions are disabled.')
        self._counter = self._max_parallel_tasks
        self._empty.set()
        self._not_full.set()
        self._sessions = self.discover_service(self._sessions, cls=BaseSessionService, required=False)
        for service_name, service in self.app.services.items():
            if isinstance(service, AbstractRPCCompatible):
                self.register_service(service_name, service)
        await super().init()

    async def close(self):
        await self._empty.wait()
        await super().close()

    @property
    def routes(self):
        return {'api': self.get_routes, 'status': self.get_status, 'tasks': self.get_tasks}

    @property
    def permissions(self):
        return {
            'api': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'status': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
            'tasks': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
        }

    @staticmethod
    async def get_tasks() -> list:
        """Get all current asyncio tasks."""
        tasks = asyncio.all_tasks(asyncio.get_running_loop())
        t = int(time())
        tasks_info = []
        for task in tasks:
            name = task.get_name()
            data = {'name': name}
            if name.startswith('rpc:'):
                task = cast(_Task, task)
                data.update(
                    {
                        'system': False,
                        'cid': name.split(':')[1],
                        'time_elapsed': t - task.started,
                        'time_left': task.deadline - task.started,
                    }
                )
            else:
                f_code = task.get_stack(limit=1)[-1].f_code
                data.update({'system': True, 'coro': f_code.co_name})
            tasks_info.append(data)

        tasks_info.sort(key=lambda o: (o['system'], o['name']))
        return tasks_info

    async def get_status(self) -> dict:
        """Get server status and current tasks."""
        return {
            'app': self.app.name,
            'app_id': self.app.id,
            'env': self.app.env,
            'debug': self._debug,
            'rpc_tasks': self._max_parallel_tasks - self._counter,
            'queue_full': not self._not_full.is_set(),
            'server_time': int(time()),
            'max_tasks': self._max_parallel_tasks,
            'max_timeout': self._max_request_time,
            'default_timeout': self._default_request_time,
            'enable_permissions': self._enable_permissions,
        }

    async def get_routes(self, pattern: str = '*') -> dict:
        """Get all RPC routes (you are here)."""
        session = self.get_session()
        routes = [
            {
                'route': route,
                'signature': method['signature'],
            }
            for route, method in self._methods.items()
            if method['permission'].value >= session.scope.value and fnmatch(route, pattern)
        ]
        routes.sort(key=lambda o: o['route'])
        return {'api': 'jsonrpc', 'version': JSONRPC, 'spec': 'https://www.jsonrpc.org/specification', 'routes': routes}

    def register_service(self, service_name: str, service: AbstractRPCCompatible) -> None:
        """Register an RPC compatible service and its methods."""
        if not isinstance(service, AbstractRPCCompatible):
            raise TypeError('Service must be rpc compatible.')
        permissions = service.permissions
        validators = service.validators
        for route, f in service.routes.items():
            full_name = f'{service_name}.{route}'
            if self._route_blacklisted(full_name):
                continue
            route_perm = AbstractRPCCompatible.PermissionKeys.GLOBAL_SYSTEM_PERMISSION
            for pattern, perm in permissions.items():
                if fnmatch(route, pattern):
                    route_perm = perm
            if route_perm.value <= self._blacklist_scope:
                continue
            try:
                annotation = AnnotationParser.parse_method(type(service), route, f)
            except Exception as exc:
                warnings.warn(f'Cannot automatically create validator for {route}: {exc}')
                annotation = None
            validator = None
            if route in validators:
                params = validators[route]
                if params:
                    validator = compile_schema(params)
            elif self._use_annotation_parser and annotation:
                params = annotation['params']
                if params:
                    params = params.repr()
                    if params:
                        validator = compile_schema(params)
            # signature = inspect.signature(f)
            # sig_text = [str(value) for key, value in signature.parameters.items() if not key.startswith('_')]
            method = MethodInfo(
                f=f,
                permission=self._permission_levels[route_perm],
                validator=validator,
                service_name=service_name,
                signature=annotation,
            )
            self._methods[full_name] = method

    def _route_blacklisted(self, route: str) -> bool:
        """Check if route is blacklisted by this server instance."""
        for pattern in self._blacklist_routes:
            if fnmatch(route, pattern):
                return True
        return False

    async def call(
        self,
        body: Union[List, Dict],
        headers: dict = None,
        session: Session = None,
        nowait: bool = False,
        scope: Scope = Scope.SYSTEM,
        callback: Callable[..., Awaitable] = None,
    ) -> (dict, RequestHeaders):
        """Call a server command.

        :param body: request body
        :param headers: request headers (optional)
        :param session: client session object
        :param scope: user scope
        :param nowait: do not wait for the result
        :param callback: optional response callback which should contain (session, headers, result) input params
        """
        headers = self._get_request_headers(headers)
        if type(body) in {list, tuple}:
            try:
                reqs = [
                    self._prepare_request(req, session, scope, n, use_template=headers['use_template'])
                    for n, req in enumerate(body)
                ]
                return_result = any(req[0] is not None for req in reqs)
            except JSONRPCError as exc:
                headers = self._get_response_headers(headers['correlation_id'], session)
                return headers, RPCError(id=exc.data.get('id'), error=exc)
            coro = self._execute_batch(
                reqs,
                retries=headers['retries'],
                request_deadline=headers['request_deadline'],
                abort_on_error=headers['abort_on_error'],
                use_template=headers['use_template'],
                session=session,
                correlation_id=headers['correlation_id'],
                callback=callback,
            )
        else:
            try:
                req_id, f, params, body = self._prepare_request(
                    body, session, scope, 0, use_template=headers['use_template']
                )
                return_result = req_id is not None
            except JSONRPCError as exc:
                headers = self._get_response_headers(headers['correlation_id'], session)
                return headers, RPCError(id=exc.data.get('id'), error=exc)
            coro = self._execute_single(
                f,
                params,
                request_id=req_id,
                body=body,
                retries=headers['retries'],
                request_deadline=headers['request_deadline'],
                session=session,
                correlation_id=headers['correlation_id'],
                callback=callback,
            )
        self._counter -= 1
        if not self._not_full.is_set():
            await self._not_full.wait()
        task = asyncio.create_task(coro)
        task.set_name(f'rpc:{headers["correlation_id"]}')
        setattr(task, 'deadline', headers['request_deadline'])
        setattr(task, 'started', int(time()))
        task.add_done_callback(self._request_done_cb)
        if self._empty.is_set():
            self._empty.clear()
        if self._counter <= 0:
            self._counter = 0
            self._not_full.clear()
        if not return_result:
            return self._get_response_headers(headers['correlation_id'], session), None
        elif nowait:
            return task
        else:
            return await task

    @staticmethod
    def _get_int_header(value: Union[str, None], default) -> int:
        """Parse an integer header value.

        https://httpwg.org/specs/rfc8941.html#integer
        """
        try:
            return int(value) if value else default
        except ValueError:
            return default

    @staticmethod
    def _get_bool_header(value: Union[str, bool, None], default: bool) -> bool:
        """Parse a boolean header value.

        https://httpwg.org/specs/rfc8941.html#boolean
        """
        if type(value) is bool:
            return value
        return value == '?1' if value else default

    def _get_request_headers(self, headers: Union[dict, None]) -> RequestHeaders:
        if headers is None:
            headers = {}
        request_deadline = headers.get(JSONRPCHeaders.REQUEST_DEADLINE_HEADER)
        t0 = int(time())
        if request_deadline:
            request_deadline = min(self._get_int_header(request_deadline, 0), t0 + self._max_request_time)
        else:
            request_timeout = headers.get(JSONRPCHeaders.REQUEST_TIMEOUT_HEADER)
            request_timeout = min(
                self._max_request_time, max(1, self._get_int_header(request_timeout, self._default_request_time))
            )
            request_deadline = t0 + request_timeout + 1
        correlation_id = headers.get(JSONRPCHeaders.CORRELATION_ID_HEADER)
        if not correlation_id:
            correlation_id = b2a_hex(os.urandom(4)).decode()
        return RequestHeaders(
            correlation_id=correlation_id,
            request_deadline=request_deadline,
            abort_on_error=self._get_bool_header(headers.get(JSONRPCHeaders.ABORT_ON_ERROR), False),
            use_template=self._get_bool_header(headers.get(JSONRPCHeaders.USE_TEMPLATE), False),
            retries=min(10, max(0, self._get_int_header(headers.get(JSONRPCHeaders.RETRIES), 0))),
        )

    async def _execute_single(
        self,
        f: Callable,
        params: dict,
        request_id: _RequestId,
        body: dict,
        retries: int,
        request_deadline: int,
        session: Optional[Session],
        correlation_id: Optional[str],
        callback: Callable[..., Awaitable],
    ) -> Tuple[dict, Union[RPCResponse, RPCError]]:
        """Execute a single rpc request."""
        ctx = RequestContext(
            session_id=session.id if session else None,
            request_deadline=request_deadline,
            correlation_id=correlation_id,
        )
        REQUEST_SESSION.set(session)
        REQUEST_CONTEXT.set(ctx)
        try:
            async with timeout(request_deadline - time()):
                result = await self._execute_request(f, params, retries, request_id, body)
        except asyncio.TimeoutError:
            result = RPCError(
                id=request_id, error=RequestTimeout(message='Request timeout', request_deadline=request_deadline)
            )
        session = self.get_session()
        if self._sessions and session and session.stored and session.changed:
            await self._sessions.save_session(session)
        if result.id is not None or type(result) is not RPCResponse:
            headers = self._get_response_headers(correlation_id, session)
            if callback:
                cb = asyncio.create_task(callback(session, headers, result))  # noqa
                cb.set_name(f'rpc:{correlation_id}:callback')
            return headers, result

    @staticmethod
    def _get_response_headers(correlation_id: str, session: Optional[Session]) -> dict:
        headers = {}
        if correlation_id:
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = correlation_id
        if session and session.stored and (session.changed or session.loaded):
            headers[JSONRPCHeaders.SESSION_ID_HEADER] = session.id
        return headers

    async def _execute_batch(
        self,
        requests: List[Tuple[_RequestId, Callable, dict, dict]],
        retries: int,
        request_deadline: int,
        abort_on_error: bool,
        use_template: bool,
        session: Optional[Session],
        correlation_id: Optional[str],
        callback: Callable[..., Awaitable],
    ) -> Tuple[dict, List[Union[RPCResponse, RPCError]]]:
        """Execute multiple coroutine functions."""
        ctx = RequestContext(
            session_id=session.id if session else None,
            request_deadline=request_deadline,
            correlation_id=correlation_id,
        )
        REQUEST_SESSION.set(session)
        REQUEST_CONTEXT.set(ctx)
        results, template_ctx, req_id = [], {}, None
        for n, (req_id, f, params, body) in enumerate(requests):
            try:
                if use_template:
                    if n > 0:
                        params = Template(params).fill(template_ctx)
                    method = self._methods[body['method']]
                    if method['validator']:
                        params = method['validator'](params)
                async with timeout(request_deadline - time()):
                    result = await self._execute_request(f, params, retries, req_id, body)
                if abort_on_error and isinstance(result, RPCError):
                    raise _Aborted
                if use_template and req_id is not None and type(result) is RPCResponse:
                    template_ctx[str(req_id)] = result.result
            except asyncio.TimeoutError:
                results.extend(
                    (
                        RPCError(
                            id=req_id,
                            error=RequestTimeout(message='Request timeout', request_deadline=request_deadline),
                        )
                        for req_id, f, params, body in requests[n:]
                    )
                )
                break
            except Exception as exc:
                self.logger.error('Batch error', batch_num=n, request_id=req_id, exc_info=exc)
                results.extend(
                    (RPCError(id=req_id, error=Aborted(message='Aborted')) for req_id, f, params, body in requests[n:])
                )
                break
            else:
                if result.id is not None or type(result) is not RPCResponse:
                    results.append(result)
        session = self.get_session()
        if self._sessions and session and session.stored and session.changed:
            await self._sessions.save_session(session)
        headers = self._get_response_headers(correlation_id, session)
        if results:
            if callback:
                cb = asyncio.create_task(callback(session, headers, results))  # noqa
                cb.set_name(f'rpc:{correlation_id}:callback')
            return headers, results

    def _prepare_request(
        self, body, session: Optional[Session], scope: Scope, default_id: int, use_template: bool
    ) -> (_RequestId, Callable, dict, dict):
        """Pre-validate and prepare request for the execution."""
        # request body validation
        if type(body) is not dict:
            raise InvalidRequest(id=None, message='Request must be an object')
        if 'id' not in body:
            body['id'] = _id = default_id
        else:
            _id = body['id']
            if _id is not None and type(_id) is not int:
                raise InvalidRequest(id=None, message='Request "id" must be an integer or null', request_id=_id)

        # method visibility check

        method_name = body.get('method')
        if not method_name:
            raise InvalidRequest(id=_id, message='Request "method" must be a string', request_method=method_name)
        try:
            method = self._methods[method_name]
        except KeyError:
            raise MethodNotFound(id=_id, message='Method not found', request_method=method_name)
        else:
            if self._enable_permissions:
                if all(
                    (
                        method['permission'].value < scope.value,
                        session and method_name not in session.permissions,
                        session and method['service_name'] not in session.permissions,
                    )
                ):
                    raise PermissionDenied(id=_id, message='Method not found', request_method=method_name)

        # request params validation

        params = body.get('params')
        if params is None:
            params = {}
        else:
            params = {k: v for k, v in params.items() if not k.startswith('_')}
        if params:
            if not type(params) is dict:
                raise InvalidParams(id=_id, message='Request "params" must be an object', request_params=params)
            if not use_template and method['validator']:  # template validation is postponed
                try:
                    params = method['validator'](params)
                except Exception as exc:
                    raise InvalidParams(id=_id, message=str(exc), base_exc=exc)

        return _RequestId(_id), method['f'], params, body

    async def _execute_request(
        self,
        f: Callable,
        params: dict,
        retries: int,
        request_id: _RequestId,
        request: dict,
    ) -> Union[RPCResponse, RPCError]:
        """Execute a coro and process an exception."""
        t0 = time()
        try:
            if retries:
                result = await retry(f, kws=params, retries=retries, logger=self.logger)
            else:
                result = await f(**params)
        except ClientError as exc:
            result = RPCError(id=request_id, error=exc)
            self.logger.info('Client error', result=exc)
        except APIException as exc:
            result = RPCError(id=request_id, error=exc)
            self.logger.error('Internal error', request=request, exc_info=exc)
        except Exception as exc:
            result = RPCError(id=request_id, error=InternalError(base_exc=exc, message='Internal error'))
            self.logger.error('Internal error', request=request, exc_info=exc)
        else:
            result = RPCResponse(id=request_id, result=result)
            if self._request_logs:
                self.logger.info('Request', request=request, took_ms=int((time() - t0) * 1000))
            elif self._response_logs:
                self.logger.info('Request', request=request, result=result.result, took_ms=int((time() - t0) * 1000))
        return result

    def _request_done_cb(self, task: asyncio.Task) -> None:
        """Increment the counter when a request is finished."""
        self._counter += 1
        if self._counter >= self._max_parallel_tasks:
            self._counter = self._max_parallel_tasks
            self._empty.set()
        if not self._not_full.is_set():
            self._not_full.set()
        exc = task.exception()
        if exc:
            self.logger.error('task execution error', exc_info=exc)
