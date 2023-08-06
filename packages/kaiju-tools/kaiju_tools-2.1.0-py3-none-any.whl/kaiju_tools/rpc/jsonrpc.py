import abc
from typing import *

from kaiju_tools.serialization import Serializable
from kaiju_tools.encoding.msgpack import MsgpackType, msgpack_types, ReservedClassIDs, dumps, loads
from kaiju_tools.exceptions import APIException

__all__ = ('JSONRPC', 'RPCMessage', 'RPCRequest', 'RPCResponse', 'RPCError')

JSONRPC = '2.0'  #: JSON RPC supported protocol version


class RPCMessage(Serializable, MsgpackType, abc.ABC):
    """Base JSONRPC message class."""


class RPCRequest(RPCMessage):
    """Valid JSONRPC request."""

    ext_class_id = ReservedClassIDs.jsonrpc_request

    __slots__ = ('id', 'method', 'params')

    def __init__(self, id: Union[int, None], method: str = None, params: Union[list, dict] = None):
        """Initialize."""
        self.id = id
        self.method = method
        self.params = params if params else None

    def repr(self):
        """Create a JSONRPC body."""
        data = {'jsonrpc': JSONRPC, 'id': self.id, 'method': self.method, 'params': self.params}
        return data

    def to_bytes(self) -> bytes:
        """Dump to msgpack."""
        return dumps((self.id, self.method, self.params))

    @classmethod
    def from_bytes(cls, data: bytes) -> dict:
        """Load from msgpack."""
        data = loads(data)
        return {'jsonrpc': JSONRPC, 'id': data[0], 'method': data[1], 'params': data[2]}


class RPCResponse(RPCMessage):
    """Valid JSON RPC response."""

    ext_class_id = ReservedClassIDs.jsonrpc_response

    __slots__ = ('id', 'result')

    def __init__(self, id: Union[int, None], result: Any):
        """Initialize."""
        self.id = id
        self.result = result

    def repr(self):
        """Create a JSONRPC body."""
        return {'jsonrpc': JSONRPC, 'id': self.id, 'result': self.result}

    def to_bytes(self) -> bytes:
        """Dump to msgpack."""
        return dumps((self.id, self.result))

    @classmethod
    def from_bytes(cls, data: bytes) -> dict:
        """Load from msgpack."""
        data = loads(data)
        return {'jsonrpc': JSONRPC, 'id': data[0], 'result': data[1]}


class RPCError(RPCMessage):
    """RPC error object."""

    ext_class_id = ReservedClassIDs.jsonrpc_error

    __slots__ = ('id', 'error')

    def __init__(self, id: Union[int, None], error: APIException):
        """Initialize."""
        self.id = id
        self.error = error

    def repr(self) -> dict:
        """Create a JSONRPC body."""
        return {'jsonrpc': JSONRPC, 'id': self.id, 'error': self.error.repr()}

    def to_bytes(self) -> bytes:
        """Dump to msgpack."""
        return dumps((self.id, self.error))

    @classmethod
    def from_bytes(cls, data: bytes) -> dict:
        """Load from msgpack."""
        data = loads(data)
        return {'jsonrpc': JSONRPC, 'id': data[0], 'error': data[1]}


msgpack_types.register_class(RPCRequest)
msgpack_types.register_class(RPCResponse)
msgpack_types.register_class(RPCError)
