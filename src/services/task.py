import logging
from asyncio import Task
from threading import Timer
from time import time
from typing import Callable

from croniter import croniter

from src.common.utils import Singleton


class PeriodicTask:

    def __init__(self, cron_string: str, task: Callable, *args, **kwargs):
        self._task = task
        self._args = args
        self._kwargs = kwargs
        self._croniter = croniter(cron_string)
        self._timer = None
        self._con_str = cron_string

    @property
    def cron_string(self) -> str:
        return self._con_str

    def _run(self, first_time: bool = False, run_first_time: bool = True):
        if not first_time or run_first_time:
            self._task(*self._args, **self._kwargs)
        now = time()
        time_next_exec = self._croniter.get_next(start_time=now)
        delay = max(0, time_next_exec - now)
        self._timer = Timer(delay, self._run)
        self._timer.start()

    def run(self, run_first_time: bool = True):
        """
        Run periodic task. The task function will be executed whenever the current time matches the cron string
        of the task. If the task is already running, nothing is done.

        Args:
            run_first_time:  whether the task should be run a first time, regardless of the con string (True by default)
        """
        if self.is_running:
            return
        self._run(first_time=True, run_first_time=run_first_time)

    def stop(self):
        """
        Stops periodic task if it is running.
        """
        if self.is_running:
            self._timer.cancel()
            self._timer = None

    @property
    def is_running(self) -> bool:
        """
        Indicates whether the periodic task is running.
        """
        return self._timer is not None


class PeriodicTaskManager(metaclass=Singleton):

    def __init__(self):
        self._startup_tasks: dict[str, Task] = {}
        self._periodic_tasks: dict[str, PeriodicTask] = {}

    def add_periodic_task(self, name: str, task: PeriodicTask):
        self._periodic_tasks[name] = task

    def run_periodic_tasks(self):
        for name, task in self._periodic_tasks.items():
            logging.info(f"[{self.__class__.__name__}] starting periodic task {name} "
                         f"(cron string: \"{task.cron_string}\")")
            task.run()


if __name__ == '__main__':
    from time import sleep

    def greet(name: str):
        print(f'Hello, {name}!')

    ptask = PeriodicTask(cron_string='* * * * *', task=greet, name='John')
    ptask.run(run_first_time=True)
    sleep(130)
    ptask.stop()


