"""JSONSchema validation classes."""

import abc
from typing import Dict, List, Collection, Callable

from fastjsonschema import compile
from fastjsonschema.exceptions import JsonSchemaException

from .serialization import Serializable

__all__ = (
    'custom_formatters',
    'compile_schema',
    'JSONSchemaObject',
    'Enumerated',
    'Boolean',
    'String',
    'Number',
    'Integer',
    'Array',
    'Object',
    'Generic',
    'JSONSchemaKeyword',
    'AnyOf',
    'OneOf',
    'AllOf',
    'Not',
    'GUID',
    'Date',
    'DateTime',
    'Null',
    'Constant',
)


class JSONSchemaObject(Serializable):
    """Base JSONSchema object."""

    type: str = None

    __slots__ = ('default', 'title', 'description', 'examples', 'enum', 'nullable')

    def __init__(
        self,
        title: str = None,
        description: str = None,
        default=...,
        examples: list = None,
        enum: list = None,
        nullable: bool = None,
    ):
        """Initialize."""
        self.default = default
        self.title = title
        self.description = description
        self.examples = examples
        self.enum = enum
        self.nullable = nullable

    def _set_non_null_values(self, data, keys):
        for key in keys:
            value = getattr(self, key)
            if value is not None:
                if isinstance(value, JSONSchemaObject):
                    value = value.repr()
                data[key] = value

    def repr(self) -> dict:
        """Serialize."""
        data = {}
        if self.type:
            data['type'] = self.type
        self._set_non_null_values(data, ('title', 'description', 'examples', 'enum'))
        if self.default is not ...:
            data['default'] = self.default
        return data


class Boolean(JSONSchemaObject):
    """Boolean `True` or `False`."""

    type = 'boolean'


Enumerated = JSONSchemaObject  # compatibility, the base object has enum


class String(JSONSchemaObject):
    """Text/string data type."""

    type = 'string'
    format_: str = None

    STRING_FORMATS = frozenset(
        {
            'date-time',
            'time',
            'date',
            'email',
            'idn-email',
            'hostname',
            'idn-hostname',
            'ipv4',
            'ipv6',
            'uri',
            'uri-reference',
            'iri',
            'iri-reference',
            'regex',
        }
    )

    __slots__ = ('minLength', 'maxLength', 'pattern', 'format')

    def __init__(
        self, *args, minLength: int = None, maxLength: int = None, pattern: str = None, format: str = None, **kws
    ):
        """Initialize."""
        super().__init__(*args, **kws)
        self.minLength = minLength
        self.maxLength = maxLength
        self.pattern = pattern
        if format and format not in self.STRING_FORMATS:
            raise JsonSchemaException(
                'Invalid string format "%s".' 'Must be one of: "%s".' % (format, list(self.STRING_FORMATS))
            )
        self.format = self.format_ if self.format_ else format

    def repr(self) -> dict:
        """Serialize."""
        data = super().repr()
        self._set_non_null_values(data, ('minLength', 'maxLength', 'pattern', 'format'))
        return data


class DateTime(String):
    """Datetime string alias."""

    format_ = 'date-time'
    __slots__ = tuple()


class Date(String):
    """Date string alias."""

    format_ = 'date'
    __slots__ = tuple()


class GUID(String):
    """UUID string alias."""

    format_ = 'uuid'
    __slots__ = tuple()


class Constant(Enumerated):
    """Value is a constant."""

    __slots__ = tuple()

    def __init__(self, const, *args, **kws):
        """Initialize."""
        super().__init__(enum=[const], *args, **kws)


class _Null(Enumerated):
    """Null value only."""

    __slots__ = tuple()

    def __init__(self):
        """Initialize."""
        super().__init__(enum=[None])


Null = _Null()


class Number(JSONSchemaObject):
    """Numeric data type (use it for both float or integer params)."""

    type = 'number'
    __slots__ = ('multipleOf', 'minimum', 'exclusiveMinimum', 'maximum', 'exclusiveMaximum')

    def __init__(
        self,
        *args,
        multipleOf: float = None,
        minimum: float = None,
        maximum: float = None,
        exclusiveMinimum: float = None,
        exclusiveMaximum: float = None,
        **kws,
    ):
        """Initialize."""
        super().__init__(*args, **kws)
        self.multipleOf = multipleOf
        self.minimum = minimum
        self.maximum = maximum
        self.exclusiveMinimum = exclusiveMinimum
        self.exclusiveMaximum = exclusiveMaximum

    def repr(self) -> dict:
        """Serialize."""
        data = super().repr()
        self._set_non_null_values(data, ('multipleOf', 'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum'))
        return data


class Integer(Number):
    """Integer type."""

    type = 'integer'
    __slots__ = tuple()


class Array(JSONSchemaObject):
    """Array, list, set or tuple definition (depends on params)."""

    type = 'array'
    __slots__ = ('items', 'prefixItems', 'contains', 'additionalItems', 'uniqueItems', 'minItems', 'maxItems')

    def __init__(
        self,
        items: JSONSchemaObject = None,
        prefixItems: Collection[JSONSchemaObject] = None,
        contains: JSONSchemaObject = None,
        additionalItems: bool = None,
        uniqueItems: bool = None,
        minItems: int = None,
        maxItems: int = None,
        **kws,
    ):
        """Initialize."""
        super().__init__(**kws)
        self.items = items
        self.prefixItems = prefixItems
        self.contains = contains
        self.additionalItems = additionalItems
        self.uniqueItems = uniqueItems
        self.minItems = minItems
        self.maxItems = maxItems

    @staticmethod
    def _unpack_items(data: dict, key: str):
        if key in data:
            data[key] = [item.repr() for item in data[key]]

    def repr(self) -> dict:
        data = super().repr()
        self._set_non_null_values(
            data, ('items', 'prefixItems', 'contains', 'additionalItems', 'uniqueItems', 'minItems', 'maxItems')
        )
        for key in ('prefixItems',):
            self._unpack_items(data, key)
        return data


class Object(JSONSchemaObject):
    """JSON object (dictionary) definition."""

    type = 'object'
    __slots__ = (
        'properties',
        'propertyNames',
        'required',
        'patternProperties',
        'additionalProperties',
        'minProperties',
        'maxProperties',
    )

    def __init__(
        self,
        properties: Dict[str, JSONSchemaObject] = None,
        patternProperties: Dict[str, JSONSchemaObject] = None,
        propertyNames: dict = None,
        additionalProperties: bool = None,
        minProperties: int = None,
        maxProperties: int = None,
        required: List[str] = None,
        **kws,
    ):
        """Initialize."""
        super().__init__(**kws)
        self.properties = properties if properties else {}
        self.patternProperties = patternProperties
        self.propertyNames = propertyNames
        self.additionalProperties = additionalProperties
        self.minProperties = minProperties
        self.maxProperties = maxProperties
        self.required = required

    def repr(self) -> dict:
        """Serialize."""
        data = super().repr()
        self._set_non_null_values(
            data,
            (
                'properties',
                'propertyNames',
                'required',
                'patternProperties',
                'additionalProperties',
                'minProperties',
                'maxProperties',
            ),
        )
        data['properties'] = {key: value.repr() for key, value in data['properties'].items()}
        if 'patternProperties' in data:
            data['patternProperties'] = {key: value.repr() for key, value in data['patternProperties'].items()}
        return data


Generic = JSONSchemaObject  # compatibility


class JSONSchemaKeyword(JSONSchemaObject, abc.ABC):
    """Abstract class for JSON Schema specific logical keywords."""

    type: str = None
    __slots__ = ('items',)

    def __init__(self, *items: JSONSchemaObject):
        """Initialize."""
        super().__init__()
        self.items = items

    def repr(self) -> dict:
        """Serialize."""
        return {self.type: [item.repr() for item in self.items]}


class AnyOf(JSONSchemaKeyword):
    """Given data must be valid against any (one or more) of the given sub-schemas."""

    type = 'anyOf'
    __slots__ = tuple()


class OneOf(JSONSchemaKeyword):
    """Given data must be valid against exactly one of the given sub-schemas."""

    type = 'oneOf'
    __slots__ = tuple()


class AllOf(JSONSchemaKeyword):
    """Given data must be valid against all of the given sub-schemas."""

    type = 'allOf'
    __slots__ = tuple()


class Nullable(AnyOf):
    """Nullable value."""

    type = 'oneOf'
    __slots__ = tuple()

    def __init__(self, item: JSONSchemaObject):
        """Initialize."""
        super().__init__(item, Null)


class Not(JSONSchemaObject):
    """Reverse the condition."""

    __slots__ = ('item',)

    def __init__(self, item: JSONSchemaObject):
        """Initialize."""
        super().__init__()
        self.item = item

    def repr(self):
        """Serialize."""
        return {'not': self.item.repr()}


custom_formatters = {
    'uuid': r'^[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}$'
}  # these are used by the fastjsonschema compiler to validate some specific data types


def compile_schema(validator, formats=None) -> Callable[[dict], dict]:
    """Compile JSONSchema object into a validator function."""
    if formats is None:
        formats = custom_formatters
    if isinstance(validator, JSONSchemaObject):
        validator = validator.repr()
    return compile(validator, formats=formats)
