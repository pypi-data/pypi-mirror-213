from typing import Union, List

from kaiju_tools.rpc.client import BaseRPCClientService
from kaiju_tools.rpc.jsonrpc import RPCRequest
from kaiju_tools.streams.abc import Listener

__all__ = ['StreamRPCClient']


class StreamRPCClient(BaseRPCClientService):
    """Streams compatible RPC client."""

    transport_cls = Listener
    _transport: Listener

    def __init__(self, *args, topic: str = None, **kws):
        super().__init__(*args, **kws)
        self.topic = topic if topic else self.app.name

    async def _request(self, body: Union[RPCRequest, List[RPCRequest]], headers: dict):
        if type(body) is list:
            for req in body:
                req.id = None
        else:
            body.id = None
        await self._transport._producer.send(self.app.env, self.app.name, body, headers)  # noqa
