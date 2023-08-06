import datetime
import uuid

import pytest

from kaiju_tools.exceptions import InternalError
from kaiju_tools.rpc.jsonrpc import RPCRequest, RPCResponse, RPCError


@pytest.fixture
def serializable_data():
    data = {
        'int': 42,
        'str': 'some text',
        'unicode': 'уникоде',
        'bool': True,
        'uuid': uuid.uuid4(),
        'list': ['some', 'text', 42],
        'time': datetime.datetime(2001, 1, 1, 1),
    }
    return data


@pytest.fixture
def serializable_special_objects():
    data = {
        'request': RPCRequest(id=1, method='test', params=None),
        'response': RPCResponse(id=1, result=[1, 2, 3]),
        'error': RPCError(id=None, error=InternalError('Internal error', base_exc=ValueError('Sht!'))),
    }
    return data
