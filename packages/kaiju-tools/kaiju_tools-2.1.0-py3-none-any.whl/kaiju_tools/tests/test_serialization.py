import pytest

from ..serialization import Serializable


def test_serialization(logger):
    class C(Serializable):

        serializable_attrs = ('a', 'b')

        def __init__(self, a, b):
            self.a = a
            self.b = b
            self.c = a + b

    for cls in (C,):
        logger.info('testing subclass of %s ...', cls.__bases__[-1].__name__)
        logger.info(' - construction')
        c = cls(1, 2)
        d = cls(**c.repr())
        assert c.a == d.a
