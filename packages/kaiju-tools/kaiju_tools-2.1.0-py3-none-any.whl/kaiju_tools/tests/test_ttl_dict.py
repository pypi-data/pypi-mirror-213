from collections import deque
from time import time, sleep

import pytest

from ..ttl_dict import TTLDict


def test_ttl_dict(logger):

    fixture = {'a': 42}

    logger.info('Testing basic operation.')

    ttl = TTLDict(**fixture)
    assert dict(ttl) == fixture
    assert list(ttl.items()) == list(fixture.items())
    assert list(ttl.values()) == list(fixture.values())
    assert dict(**ttl) == fixture
    assert ttl.pop('a') == fixture['a']
    assert len(ttl) < len(fixture)
    assert not ttl
    ttl['b'] = 42
    assert 'b' in ttl

    logger.info('Testing ttl operations.')

    with pytest.raises(ValueError):
        ttl.set_ttl(-1)

    ttl.set_ttl(1)
    ttl['k'] = 1
    sleep(1.1)
    assert 'k' not in ttl
    assert ttl.get('k') is None

    logger.info('Finished tests.')
