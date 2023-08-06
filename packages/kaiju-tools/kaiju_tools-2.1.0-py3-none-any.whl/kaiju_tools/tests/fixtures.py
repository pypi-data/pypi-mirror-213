import gc
import logging
import multiprocessing as mp
import os
import platform
import queue
import signal
import traceback
import uuid
from datetime import timedelta, datetime
from inspect import iscoroutinefunction
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile
from time import sleep
from types import SimpleNamespace

import pytest

__all__ = (
    'logger',
    'application',
    'system_information',
    'temp_dir',
    'sample_file',
)


@pytest.fixture(scope='session')
def system_information():
    """Get system and hardware info."""
    t = datetime.now().strftime('%Y-%m-%d %H:%M')
    _sys = platform.version()
    _python = platform.python_version()

    return f"""Python {_python}
{_sys}
{t}
"""


@pytest.fixture(scope='session')
def logger():
    """Return a test logger preconfigured to DEBUG level."""
    logger = logging.getLogger('pytest')
    logger.setLevel('DEBUG')
    return logger


@pytest.fixture
def application(logger):
    """Return a sample aiohttp web app object to use in tests. Requires aiohttp.

    You may pass a list of `Service` classes. They won't be initialized but they will be registered
    in the pseudo-service context meaning you can use `app.services.<service_name>` inside you code
    as if it's a normal initialized app.
    """
    from aiohttp.web import Application

    def _application(*services, name='pytest', id=str(uuid.uuid4()), **kws):
        app = Application(logger=logger, **kws)
        app['id'] = app.id = id
        app['name'] = app.name = name
        app['env'] = app.env = 'dev'
        app.services = {service.service_name: service for service in services}
        return app

    return _application


@pytest.fixture
def temp_dir():
    with TemporaryDirectory(prefix='pytest') as d:
        yield Path(d)


@pytest.fixture
def sample_file():
    with NamedTemporaryFile(prefix='pytest', delete=False) as f:
        name = f.name
        f.write('test')
    yield Path(name)
    os.remove(name)
