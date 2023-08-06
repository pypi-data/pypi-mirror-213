from typing import cast, Type

import pytest

from ..serializers import serializers
from ..abc import SerializerInterface
from .fixtures import *


@pytest.mark.parametrize('serializer', tuple(serializers.values()), ids=tuple(serializers.keys()))
def test_serializers(serializer, serializable_data, logger):
    serializer = cast(Type[SerializerInterface], serializer)
    serializer = serializer()
    s = serializer.dumps(serializable_data)
    logger.debug(s)
    data = serializer.loads(s)
    logger.debug(serializable_data)
    logger.debug(data)
    assert serializable_data == data


@pytest.mark.parametrize('serializer', tuple(serializers.values()), ids=tuple(serializers.keys()))
def test_serializers_for_special_objects(serializer, serializable_special_objects, logger):
    serializer = cast(Type[SerializerInterface], serializer)
    serializer = serializer()
    s = serializer.dumps(serializable_special_objects)
    logger.debug(s)
    data = serializer.loads(s)
    logger.debug(serializable_special_objects)
    logger.debug(data)
    assert {k: v.repr() for k, v in serializable_special_objects.items()} == data
