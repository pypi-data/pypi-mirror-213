import asyncio
from enum import Enum
from time import time
from typing import Union, List, cast, Callable, Awaitable
from weakref import proxy

from kaiju_tools.services import ContextableService
from kaiju_tools.mapping import SortedStack
from kaiju_tools.functions import timeout, retry

__all__ = ['Scheduler', 'ExecPolicy']

_Callable = Callable[..., Awaitable]


class ExecPolicy(Enum):
    """Task policy for a scheduled task."""

    WAIT = 'WAIT'  #: wait until the current task iteration is executed
    CANCEL = 'CANCEL'  #: cancel the current iteration immediately and restart the task
    IGNORE = 'IGNORE'  #: ignore current task completely and start a new one


class _ScheduledTask:
    """Scheduled task information."""

    __slots__ = (
        '_scheduler',
        'name',
        'method',
        'params',
        'interval',
        'policy',
        'called_at',
        '_enabled',
        'executed',
        'retries',
        '__weakref__',
    )

    def __init__(
        self,
        scheduler: 'Scheduler',
        name: str,
        method: Callable,
        params: Union[dict, None],
        interval: int,
        policy: ExecPolicy,
        retries: int,
    ):
        """Initialize."""
        self._scheduler = proxy(scheduler)
        self.name = name
        self.method = method
        self.params = params
        self.interval = interval
        self.policy = policy
        self.called_at = 0
        self.retries = retries
        self._enabled = True
        self.executed: Union[asyncio.Task, None] = None

    @property
    def enabled(self) -> bool:
        """Task is enabled for execution."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Enable or disable task."""
        self._enabled = value
        if value is True:
            t_ex = self.called_at + self.interval
            self.scheduler._stack.insert(t_ex, self)  # noqa

    @property
    def max_timeout(self) -> int:
        if self.policy is ExecPolicy.CANCEL:
            return min(1, self.interval - 1)
        else:
            return min(1, self.interval * 2 - 1)


class Scheduler(ContextableService):
    """Scheduler for periodic tasks execution."""

    ExecPolicy = ExecPolicy

    def __init__(self, *args, refresh_rate: int = 1, **kws):
        """Initialize.

        :param refresh_rate: base refresh rate
        """
        super().__init__(*args, **kws)
        self.refresh_rate = refresh_rate
        self._stack = SortedStack()
        self._tasks: List[_ScheduledTask] = []
        self._scheduler_task: Union[asyncio.Task, None] = None

    async def init(self):
        """Initialize."""
        self._scheduler_task = asyncio.create_task(self._iter())

    async def close(self):
        """Close."""
        self._scheduler_task.cancel()
        self._scheduler_task = None
        self._stack.clear()
        await asyncio.gather(
            *(
                task.executed
                for task in self._tasks
                if task.executed and not (task.executed.done() or task.executed.cancelled())
            ),
            return_exceptions=True,
        )

    @property
    def tasks(self):
        """Get a list of registered tasks."""
        return self._tasks

    def schedule_task(
        self,
        method: _Callable,
        interval: int,
        params: Union[dict, None] = None,
        *,
        policy: ExecPolicy = ExecPolicy.CANCEL,
        retries: int = 0,
        name: str = None,
    ) -> _ScheduledTask:
        """Schedule a periodic task.

        :param method: RPC server method name
        :param params: method input arguments
        :param interval: exec interval in seconds
        :param policy: exec policy
        :param retries: number of retries if any
        :param name: optional custom task name (for tracing)
        :returns: an instance of scheduled task
            you can temporarily suspend this task from execution by settings `task.enabled = False`
            it will not be picked up by the scheduler until you set it back to `True`
        """
        if name is None:
            name = f'scheduled:{method.__name__}'
        if params is None:
            params = {}
        self.logger.debug('schedule', task_name=name, interval=interval, policy=policy.value)
        task = _ScheduledTask(self, name, method, params, interval, policy, retries)
        self._tasks.append(task)
        t_ex = time() + interval
        self._stack.insert(t_ex, task)
        return task

    async def _iter(self) -> None:
        """Iterate over the tasks ready to run."""
        while 1:
            to_execute = self._stack.pop_many(time())
            for scheduled in to_execute:
                scheduled = cast(_ScheduledTask, scheduled)
                if not scheduled.enabled:
                    continue
                if scheduled.executed and not (scheduled.executed.done() or scheduled.executed.cancelled()):
                    if scheduled.policy is ExecPolicy.CANCEL:
                        scheduled.executed.cancel(msg='Cancelled by the task scheduler')
                    elif scheduled.policy is ExecPolicy.WAIT:
                        continue
                    # else 'IGNORE'

                scheduled.executed = task = asyncio.create_task(self._run_task(scheduled))
                scheduled.called_at = time()
                task._scheduled = proxy(scheduled)
                task.add_done_callback(self._task_callback)
                task.set_name(scheduled.name)

            await asyncio.sleep(self._get_sleep_interval())

    async def _run_task(self, task: _ScheduledTask) -> None:
        """Run task in a wrapper."""
        try:
            async with timeout(task.max_timeout):
                if task.retries:
                    await retry(task.method, kws=task.params, retries=task.retries)
                else:
                    await task.method(**task.params)
        except Exception as exc:
            self.logger.error('task error', task_name=task.name, exc_info=exc)

    def _get_sleep_interval(self) -> float:
        """Get real sleep interval for the scheduler loop."""
        lowest_score = self._stack.lowest_score
        if lowest_score is None:
            lowest_score = 0
        t0 = time()
        interval = min(max(lowest_score - t0, t0), self.refresh_rate)
        return interval

    def _task_callback(self, task: asyncio.Task) -> None:
        """Capture a task result."""
        result = task.result()
        if isinstance(result, Exception):
            self.logger.error(str(result), exc_info=result)
        scheduled = task._scheduled  # noqa
        self._stack.insert(scheduled.called_at + scheduled.interval, scheduled)
        scheduled.executed = None
        task._scheduled = None
