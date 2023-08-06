"""Commonly used functions."""

import asyncio
import ctypes
import os
from asyncio import sleep
from binascii import b2a_hex
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ConcurrentTimeoutError
from secrets import randbits
from functools import partial
from typing import TypedDict, Collection, Type, Union
from uuid import UUID

__all__ = [
    'retry',
    'retry_',
    'RETRY_EXCEPTION_CLASSES',
    'terminate_thread',
    'async_run_in_thread',
    'async_',
    'RetryParams',
    'secure_uuid',
    'not_implemented',
    'timeout',
    'debug_only',
    'get_short_uid',
    'RetryException',
]


class RetryException(Exception):
    """Exception should be raised by a method expecting a retry after this exception."""


RETRY_EXCEPTION_CLASSES = frozenset([TimeoutError, asyncio.TimeoutError, asyncio.CancelledError, RetryException])


def get_short_uid() -> str:
    """Get a short uid string."""
    return b2a_hex(os.urandom(4)).decode()


class RetryParams(TypedDict, total=False):
    """Parameters for the retry function."""

    exec_timeout: int
    retries: int
    retry_timeout: float
    multiplier: float
    max_retry_timeout: float
    exception_classes: Collection[Union[str, Exception]]


async def retry(
    func,
    args: tuple = None,
    kws: dict = None,
    *,
    exec_timeout: int = None,
    retries: int = 1,
    retry_timeout: float = 0.5,
    multiplier: float = 0.1,
    max_retry_timeout: float = 10.0,
    exception_classes: Collection[Type[Exception]] = RETRY_EXCEPTION_CLASSES,
    logger=None,
):
    """Repeat an asynchronous operation if a specific exception occurs.

    This function is designed to wait a little longer each consequent try.
    You can override this behaviour by setting `multiplier` to 0.

    If the number of retries is exceeded this function will automatically raise the last stored
    exception, otherwise the function result will be directly returned.

    Example of use:

    >>> import asyncio
    >>> counter = 0
    >>> async def f(n):
    ...     global counter
    ...     if counter < n:
    ...         counter += 1
    ...         raise OSError(str(counter))
    ...     return True
    >>> r = retry(f, (3,), retry_timeout=0.001, retries=4, exception_classes=[OSError])
    >>> asyncio.run(r)
    True

    If the retry limit is reached it will automatically propagate the captured exception:

    >>> counter = 0
    >>> r = retry(f, (3,), retry_timeout=0.001, retries=3, exception_classes=[OSError])
    >>> asyncio.run(r) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    OSError:

    :param func: async callable
    :param args: function arguments
    :param kws: function keyword arguments
    :param exec_timeout: exec timeout (None for no timeout) for each function call
    :param retries: max number of retries:
        -1 for infinite retries, 1 - means no retries only a single request, 0 - meaningless
    :param retry_timeout: time between consequent tries
    :param max_retry_timeout: max time between consequent tries
    :param multiplier: retry_timeout multiplier for each try, the formula:

            new_retry_timeout = min(max_timeout, retry_timeout * (1 + multiplier)**try)

        Note, that an actual execution time is not included so the actual time will be:

            retry_time = min(max_timeout, retry_timeout * (1 + multiplier)**try) + last_execution_time

    :param exception_classes: exception classes for retrying, all other classes will be propagated immediately
        with no retries, you also may pass a list of exception name strings in here. Mixing exception classes
        with string names in not supported, you should use either one or another.
    :param logger: you may pass a logger object to log tries

    :returns: function result
    :raises StopIteration: if max number of retries reached and no exception was stored (rare)
    """
    exc = None
    modifier = 1.0 + multiplier
    if args is None:
        args = tuple()
    if kws is None:
        kws = {}
    if retries == -1:
        retries = float('Inf')

    while retries:
        try:
            if exec_timeout:
                async with timeout(exec_timeout):
                    result = await func(*args, **kws)
            else:
                result = await func(*args, **kws)
        except Exception as err:
            if err.__class__ in exception_classes:
                if logger:
                    logger.info('Retrying: %s', err)
                exc = err
                await sleep(retry_timeout)
                retry_timeout = min(max_retry_timeout, retry_timeout * modifier)
                retries -= 1
                continue
            raise

        return result

    if exc:
        raise exc

    raise StopIteration


def retry_(**retry_params):
    """Get a decorator for `retry` function."""

    def wrapper(func):
        def retry_func(*args, **kws):
            return retry(func, args=args, kws=kws, **retry_params)

        return retry_func

    return wrapper


async def async_run_in_thread(f, args: tuple = None, kws: dict = None, max_timeout: float = None):
    """Run a synchronous function in a separate thread as an async function. Use with caution.

    :param f: function
    :param args: function arguments
    :param kws: function keyword arguments
    :param max_timeout: max execution time in seconds (None for no limit)

    :return: function result
    :raises ConcurrentTimeoutError: on execution timeout
    """
    loop = asyncio.get_event_loop()
    if args is None:
        args = tuple()
    if kws is None:
        kws = {}
    f = partial(f, *args, **kws)

    with ThreadPoolExecutor(max_workers=1) as tp:
        future = loop.run_in_executor(tp, f)
        try:
            if max_timeout:
                async with timeout(max_timeout):
                    result = await future
            else:
                result = await future
        except ConcurrentTimeoutError:
            tp.shutdown(wait=False)
            for t in tp._threads:  # noqa  can't do otherwise
                terminate_thread(t)
            raise
        else:
            return result


def async_(__f):
    """Get a decorator for `async_run_in_thread` function."""

    def _wrapper(*args, **kws):
        return async_run_in_thread(__f, *args, **kws)

    return _wrapper


def terminate_thread(__thread):
    """Terminates a python thread from another thread.

    Found it on stack overflow as an only real way to stop a stuck python thread.
    https://code.activestate.com/recipes/496960-thread2-killable-threads/
    Use with caution.
    """
    if not __thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(__thread.ident), exc)
    if res == 0:
        raise ValueError('Nonexistent thread id.')
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(__thread.ident, None)
        raise SystemError('PyThreadState_SetAsyncExc failed.')


def secure_uuid() -> UUID:
    """Get a more secure version of random UUID."""
    return UUID(int=randbits(128))


def not_implemented(__message: str = None):
    """Decorate a not implemented method or function to raise an error on access."""

    def __params(_):
        def _wrap(*_, **__):
            raise NotImplementedError(__message)

        return _wrap

    return __params


def debug_only(f):
    """Decorate a debug-only method (will not be available in the production mode."""
    f._debug_only_ = True
    return f


class _Timeout:
    __slots__ = ('_timeout', '_loop', '_task', '_handler')

    def __init__(self, _timeout: float, loop=None):
        self._timeout = max(0.0, _timeout)
        self._loop = loop
        self._handler = None

    async def __aenter__(self):
        if self._loop is None:
            loop = asyncio.get_running_loop()
        else:
            loop = self._loop
        task = asyncio.current_task()
        self._handler = loop.call_at(loop.time() + self._timeout, self._cancel_task, task)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is asyncio.CancelledError:
            raise asyncio.TimeoutError
        if self._handler:
            self._handler.cancel()

    @staticmethod
    def _cancel_task(task: asyncio.Task):
        task.cancel()


def timeout(__timeout: float):
    """Run asynchronous tasks with a timeout."""
    return _Timeout(__timeout)
