from collections.abc import Mapping
from enum import Enum
from types import SimpleNamespace
from typing import NamedTuple

import rapidjson
import rapidjson as rj  # type: ignore

from .abc import SerializerInterface, Serializable
from .etc import MimeTypes

__all__ = ('dumps', 'dumps_bytes', 'loads', 'load', 'Serializer', 'JSONEncoder')


class Serializer(SerializerInterface):
    """Base serializer class."""

    mime_type = MimeTypes.json

    @classmethod
    def _dumps_defaults(cls, value):
        if isinstance(value, Serializable):
            return {k: cls._dumps_defaults(v) for k, v in value.repr().items()}
        elif type(value) in {set, frozenset, tuple, NamedTuple}:
            return list(value)
        elif type(value) == SimpleNamespace:
            return value.__dict__
        elif isinstance(value, Enum):
            return value.value
        elif type(value) is bytes:
            return '[BYTES]'
        else:
            return value

    def dumps(
        self,
        *args,
        uuid_mode=rj.UM_CANONICAL,
        datetime_mode=rj.DM_ISO8601,
        ensure_ascii=False,
        number_mode=rj.NM_DECIMAL,
        iterable_mode=rj.IM_ONLY_LISTS,
        allow_nan=False,
        **kws,
    ):
        return rj.dumps(
            *args,
            uuid_mode=uuid_mode,
            ensure_ascii=ensure_ascii,
            datetime_mode=datetime_mode,
            number_mode=number_mode,
            iterable_mode=iterable_mode,
            allow_nan=allow_nan,
            default=self._dumps_defaults,
            **kws,
        )

    def dumps_bytes(
        self,
        value,
        *args,
        uuid_mode=rj.UM_CANONICAL,
        datetime_mode=rj.DM_ISO8601,
        ensure_ascii=False,
        number_mode=rj.NM_DECIMAL,
        iterable_mode=rj.IM_ONLY_LISTS,
        allow_nan=False,
        **kws,
    ):
        """Use `dumps`, but with useful default serialization settings."""
        return rj.dumps(
            value,
            *args,
            uuid_mode=uuid_mode,
            ensure_ascii=ensure_ascii,
            datetime_mode=datetime_mode,
            number_mode=number_mode,
            iterable_mode=iterable_mode,
            allow_nan=allow_nan,
            default=self._dumps_defaults,
            **kws,
        ).encode('utf-8')

    def loads(
        self,
        *args,
        uuid_mode=rj.UM_CANONICAL,
        datetime_mode=rj.DM_ISO8601,
        number_mode=rj.NM_DECIMAL,
        allow_nan=False,
        **kws,
    ):
        return rj.loads(
            *args,
            uuid_mode=uuid_mode,
            datetime_mode=datetime_mode,
            number_mode=number_mode,
            allow_nan=allow_nan,
            object_hook=self._load_serialized_obj,
            **kws,
        )

    def load(
        self,
        *args,
        uuid_mode=rj.UM_CANONICAL,
        datetime_mode=rj.DM_ISO8601,
        number_mode=rj.NM_DECIMAL,
        allow_nan=False,
        **kws,
    ):
        """Use `load`, but with useful default serialization settings."""
        return rj.load(
            *args,
            uuid_mode=uuid_mode,
            datetime_mode=datetime_mode,
            number_mode=number_mode,
            allow_nan=allow_nan,
            object_hook=self._load_serialized_obj,
            **kws,
        )


JSONEncoder = Serializer
_encoder = Serializer()
dumps = _encoder.dumps
loads = _encoder.loads
load = _encoder.load
dumps_bytes = _encoder.dumps_bytes
