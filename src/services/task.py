from __future__ import annotations

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Timer, Thread
from time import time
from typing import Callable, Any

from croniter import croniter

from src.common.utils import Singleton


class PeriodicTask:

    def __init__(self, cron_string: str, task: Callable, run_on_start: bool, *args, **kwargs):
        self._task = task
        self._args = args
        self._kwargs = kwargs
        self._run_on_start = run_on_start
        self._croniter = croniter(cron_string)
        self._timer = None
        self._con_str = cron_string

    @property
    def cron_string(self) -> str:
        return self._con_str

    def _run(self, first_time: bool = False, executor: ThreadPoolExecutor | None = None):
        if not first_time or self._run_on_start:
            if executor is not None:
                executor.submit(self._task, *self._args, **self._kwargs)
            else:
                Thread(target=self._task, args=self._args, kwargs=self._kwargs).start()
        now = time()
        time_next_exec = self._croniter.get_next(start_time=now)
        delay = max(0, time_next_exec - now)
        self._timer = Timer(delay, self._run)
        self._timer.start()

    def run(self, executor: ThreadPoolExecutor | None = None):
        if self.is_running:
            return
        self._run(first_time=True, executor=executor)

    def stop(self):
        if self.is_running:
            self._timer.cancel()
            self._timer = None

    @property
    def is_running(self) -> bool:
        return self._timer is not None


class TaskManager(metaclass=Singleton):

    def __init__(self):
        self._startup_tasks: dict[str, tuple[Callable, tuple, dict]] = {}
        self._periodic_tasks: dict[str, PeriodicTask] = {}
        self._synchronous_tasks: dict[str, tuple[Callable, tuple, dict]] = {}
        self._asynchronous_tasks: dict[str, tuple[Callable, tuple, dict]] = {}
        self._executor = ThreadPoolExecutor()  # Thread pool for running tasks

    def add_periodic_task(self, task: PeriodicTask, name: str) -> TaskManager:
        self._periodic_tasks[name] = task
        return self

    def add_startup_task(self, task: Callable, name: str, *args, **kwargs) -> TaskManager:
        self._startup_tasks[name] = (task, args, kwargs)
        return self

    def add_synchronous_task(self, task: Callable, name: str, *args: Any, **kwargs: Any) -> TaskManager:
        self._synchronous_tasks[name] = (task, args, kwargs)
        return self

    def add_asynchronous_task(self, task: Callable, name: str, *args: Any, **kwargs: Any) -> TaskManager:
        self._asynchronous_tasks[name] = (task, args, kwargs)
        return self

    def run_periodic_tasks(self):
        for name, task in self._periodic_tasks.items():
            logging.info(f"[{self.__class__.__name__}] starting periodic task {name} "
                         f"(cron string: \"{task.cron_string}\")")
            task.run(executor=self._executor)

    def run_startup_tasks(self):
        for name, (task, args, kwargs) in self._startup_tasks.items():
            logging.info(f"[{self.__class__.__name__}] running startup task {name}")
            task(*args, **kwargs)

    def _run_synchronous_tasks(self):
        for name, (task, args, kwargs) in self._synchronous_tasks.items():
            logging.info(f"[{self.__class__.__name__}] running synchronous task {name}")
            task(*args, **kwargs)

    async def _run_asynchronous_tasks(self):
        loop = asyncio.get_event_loop()
        tasks = []
        for name, (task, args, kwargs) in self._asynchronous_tasks.items():
            logging.info(f"[{self.__class__.__name__}] running asynchronous task {name}")
            # Run each task in the executor
            tasks.append(loop.run_in_executor(self._executor, partial(task, *args, **kwargs)))
        await asyncio.gather(*tasks)

    def run_all_tasks(self):
        # First, run all startup tasks synchronously
        self.run_startup_tasks()
        # Run synchronous tasks in the thread pool
        self._executor.submit(self._run_synchronous_tasks)
        # Run asynchronous tasks in the thread pool using asyncio
        asyncio.run(self._run_asynchronous_tasks())
        # Empty lists of non-periodic tasks
        self._startup_tasks.clear()
        self._synchronous_tasks.clear()
        self._asynchronous_tasks.clear()
        # run periodic tasks
        self.run_periodic_tasks()
