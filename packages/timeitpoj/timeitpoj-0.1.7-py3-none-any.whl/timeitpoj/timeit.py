#  Copyright (c) 2023 Jari Van Melckebeke
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
import time
from distutils.util import strtobool
import os
from functools import wraps

from timeitpoj.timer.internal_timer import InternalTimer
from timeitpoj.task_report import TaskReport
from timeitpoj.timer.timer import Timer
from timeitpoj.utils.misc import reformat_units, time_to_str


class TimeIt:
    """
    Jari's infamous timeit class for all your performance measuring needs

    Usage:
    with TimeIt("my timer") as timer:
        # do stuff
        with timer("my subtimer"):
            # do stuff
            with timer("my subtimer 2"):
                # do stuff


    or as a decorator:
    @TimeIt.as_decorator("my timer")
    def my_function(*args, timer, **kwargs):
        # do stuff

    """

    def __init__(self, name: str):
        self.internal_timer = InternalTimer()
        self.timer = None
        with self.internal_timer:
            self.name = name
            self.start_time = None
            self.end_time = None

            self.active = bool(strtobool(os.getenv("TIME_IT", "true")))

    def __enter__(self):
        with self.internal_timer:
            self.start_time = time.time()
            if self.timer is None:
                self.timer = Timer(self.name, self.internal_timer, None)
            return self.timer.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.__print_timeit_report()
        pass

    @property
    def elapsed_time(self):
        return self.end_time - self.start_time if self.end_time is not None else None

    def __call__(self, name, *args, **kwargs):
        if self.timer is None:
            self.timer = Timer(name, self.internal_timer, None)

        return self.timer(name)

    def __print_timeit_report(self):
        def print_report_title_line():
            print(f"================= [{self.name}] TIMEIT REPORT =================")

        def generate_task_report_dict(tasks):

            report = {}

            for task_timer in tasks:
                task_name = task_timer["name"]

                if task_name in report:
                    report[task_name]["count"] += 1
                    report[task_name]["times"].append(task_timer["elapsed_time"])
                    report[task_name]["avg"] = sum(report[task_name]["times"]) / report[task_name]["count"]
                else:
                    report[task_name] = {
                        "name": task_name,
                        "count": 1,
                        "times": [task_timer["elapsed_time"]],
                        "ratio": 0,
                        "avg": task_timer["elapsed_time"],
                    }

                if len(task_timer["task_timers"]) > 0:
                    report[task_name]["subtasks"] = generate_task_report_dict(task_timer["task_timers"])
            total_time = sum([sum(task["times"]) for task in report.values()])

            for task in report.values():
                task["ratio"] = sum(task["times"]) / total_time

            return report

        def print_report(_report, spacing=0):
            task_report = TaskReport.from_dict(
                {
                    "name": self.name,
                    "count": 1,
                    "times": [self.elapsed_time],
                    "ratio": 0,
                    "avg": self.elapsed_time,
                    "subtasks": _report,
                }
            )
            task_report.internal_time = self.internal_timer.internal_time
            task_report.print(spacing=spacing, skip_first=True)

        elapsed_time = self.elapsed_time

        generate_report_start = time.time()

        if len(self.timer.task_timers) < 1:
            print(f"[TIMEIT] {self.name} took {time_to_str(elapsed_time)}")
            return

        print_report_title_line()

        print(f"[TIMEIT] {self.name} took {time_to_str(elapsed_time)}")

        report = generate_task_report_dict(self.timer.task_timers)

        print_report(report, spacing=0)

        # print coverage stats

        time_accounted_for = 0
        total_time = elapsed_time + self.internal_timer.internal_time

        for task in report.values():
            time_accounted_for += sum(task["times"])

        coverage = time_accounted_for / total_time
        time_unaccounted_for = total_time - time_accounted_for
        print(
            f"[{coverage:.2%}% COVERAGE] time accounted for: {time_to_str(time_accounted_for)}, "
            f"time unaccounted for: {time_to_str(time_unaccounted_for)}")

        generate_report_end = time.time()
        generate_report_duration = generate_report_end - generate_report_start

        duration, unit = reformat_units(generate_report_duration)

        print(f"[TIMEIT] report generation took {time_to_str(generate_report_duration)}")

        print_report_title_line()

    @classmethod
    def as_decorator(cls, name=None, include=False):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal name
                if name is None:
                    name = func.__name__
                with cls(name) as timer:
                    if include:
                        return func(*args, timer=timer, **kwargs)
                    else:
                        return func(*args, **kwargs)

            return wrapper

        return decorator

