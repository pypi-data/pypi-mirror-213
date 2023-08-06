import abc
import calendar
import datetime
import uuid
from decimal import Decimal
from enum import Enum
from typing import Mapping, cast
from types import SimpleNamespace

import msgpack
from msgpack import dumps as msgpack_dumps
from msgpack import loads as msgpack_loads

from kaiju_tools.class_registry import AbstractClassRegistry
from .abc import SerializerInterface, Serializable, SerializedClass
from .etc import MimeTypes

__all__ = ('MsgpackType', 'ReservedClassIDs', 'Types', 'msgpack_types', 'dumps', 'loads', 'Serializer')


class MsgpackType(abc.ABC):
    """Serializable binary object."""

    ext_class_id: int  # must be set

    def repr(self) -> dict:
        raise NotImplementedError(
            'You either need to inherit from `kaiju_tools.serialization.Serializable`'
            ' or to set up your own `repr()` method or to set up you own'
            ' `pack_b` and `unpack_b` methods.'
        )

    def to_bytes(self) -> bytes:
        """Pack object to bytes (you can use a struct here to optimize size)."""
        return dumps(self.repr())  # noqa

    @classmethod
    def from_bytes(cls, data: bytes) -> 'MsgpackType':
        """Unpack bytes into object."""
        return cls(**loads(data))  # noqa


class ReservedClassIDs:
    """Msgpack ids reserved by the library."""

    # reserved from 0 to 16 (incl.)

    uuid = 1
    datetime = 3
    decimal = 4
    date = 5

    serialized_class = 19
    jsonrpc_request = 20
    jsonrpc_response = 21
    jsonrpc_error = 22


class Types(AbstractClassRegistry):
    """Msgpack types registry."""

    base_classes = (MsgpackType,)

    @staticmethod
    def class_key(obj) -> int:
        """Determine a name by which a registered class will be referenced in the class mapping."""
        return obj.ext_class_id

    def _validate_class(self, obj):
        super()._validate_class(obj)
        key = self.class_key(obj)
        if not 16 < key < 128:
            raise ValueError('Msgpack ext type id allowed to be in range from 17 to 127 but got "%s".', key)


msgpack_types = Types(raise_if_exists=True)


class Serializer(SerializerInterface):
    """Base serializer class."""

    mime_type = MimeTypes.msgpack

    @classmethod
    def _default_types(cls, obj):
        """Convert type."""
        if isinstance(obj, uuid.UUID):
            return msgpack.ExtType(ReservedClassIDs.uuid, obj.bytes)
        elif isinstance(obj, datetime.datetime):
            return msgpack.ExtType(ReservedClassIDs.datetime, msgpack_dumps(calendar.timegm(obj.utctimetuple())))
        elif isinstance(obj, datetime.date):
            return msgpack.ExtType(ReservedClassIDs.date, msgpack_dumps(calendar.timegm(obj.timetuple())))
        elif isinstance(obj, MsgpackType):
            return msgpack.ExtType(obj.ext_class_id, obj.to_bytes())
        elif isinstance(obj, SerializedClass):
            return msgpack.ExtType(ReservedClassIDs.serialized_class, msgpack_dumps(tuple(obj.repr().values())))
        elif isinstance(obj, Serializable):
            return {k: cls._default_types(v) for k, v in obj.repr().items()}
        elif isinstance(obj, (set, frozenset)):
            return list(obj)
        elif isinstance(obj, Mapping):
            return dict(obj)
        elif type(obj) == SimpleNamespace:
            return obj.__dict__
        elif isinstance(obj, Enum):
            return obj.value
        elif type(obj) == Decimal:
            return msgpack.ExtType(ReservedClassIDs.decimal, msgpack_dumps(str(obj)))
        else:
            return obj

    def _ext_hook(self, code, data):
        """Load type."""
        if code == ReservedClassIDs.uuid:
            return uuid.UUID(bytes=data)
        elif code == ReservedClassIDs.datetime:
            return datetime.datetime.utcfromtimestamp(msgpack_loads(data))
        elif code == ReservedClassIDs.date:
            return datetime.date.fromtimestamp(msgpack_loads(data))
        elif code == ReservedClassIDs.decimal:
            return Decimal(msgpack_loads(data))
        elif code == ReservedClassIDs.serialized_class:
            data = msgpack_loads(data)
            return self._load_serialized_obj({'__cls': data[0], '__attrs': data[1]})
        elif code in msgpack_types:
            cls = cast(MsgpackType, msgpack_types[code])
            return cls.from_bytes(data)
        elif type(data) is dict and '__cls' in data:
            return self._load_serialized_obj(data)
        else:
            raise ValueError(code)

    def loads(self, *args, **kws):
        return msgpack_loads(*args, ext_hook=self._ext_hook, **kws)

    def dumps(self, *args, **kws):
        return msgpack_dumps(*args, default=self._default_types, **kws)

    def dumps_bytes(self, *args, **kws):
        return msgpack_dumps(*args, default=self._default_types, **kws)


_serializer = Serializer()
dumps = _serializer.dumps
loads = _serializer.loads
