import time
from functools import wraps

from timeitpoj.timer.internal_timer import InternalTimer
from timeitpoj.utils.misc import random_task_name


class Timer:
    def __init__(self, name, internal_timer: InternalTimer, parent_timer=None):
        self.internal_timer = internal_timer
        self.start_time = None
        self.end_time = None

        self.name = name
        self.parent_timer = parent_timer
        self.internal_timer = internal_timer

        self.current_task = None
        self.current_task_name = None

        self.task_timers = []

        self.report_object = {}

    def __call__(self, name=None, *args, **kwargs):
        if name is None:
            name = random_task_name()

        with self.internal_timer:
            # oh boy this looks ugly
            if self.current_task is not None:
                return self.current_task(name, *args, **kwargs)
            else:
                self.current_task_name = name
                self.current_task = self.__class__(name, self.internal_timer, self)
            return self.current_task

    def __enter__(self):
        with self.internal_timer:
            if self.current_task_name is not None:
                self.current_task = self.__class__(self.current_task_name, self.internal_timer, self)
                self.current_task.start_timer()
                self.current_task_name = None

            self.start_time = time.time()
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()

        if self.parent_timer is not None:
            self.parent_timer.register_task_end({
                "name": self.name,
                "elapsed_time": self.end_time - self.start_time,
                "task_timers": self.task_timers,
            })
            return

        elapsed_time = self.end_time - self.start_time

        self.report_object = {
            "name": self.name,
            "elapsed_time": elapsed_time,
            "task_timers": self.task_timers
        }

    @property
    def elapsed_time(self):
        return self.end_time - self.start_time if self.end_time is not None else None

    def start_timer(self):
        self.start_time = time.time()

    def register_task_end(self, task_report):
        self.current_task = None
        self.task_timers.append(task_report)

    def function(self, name=None, include=False):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal name
                if name is None:
                    name = func.__name__
                with self(name) as timer:
                    if include:
                        return func(*args, timer=timer, **kwargs)
                    else:
                        return func(*args, **kwargs)

            return wrapper

        return decorator

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Timer(name=[{self.name}], tasks={self.task_timers}, current_task=[{self.current_task}])"
