from typing import Union, List

from timeitpoj.utils import constants
from timeitpoj.utils.misc import reformat_units, format_percentage, time_to_str

PADDING_SECONDS = len("seconds")


class TaskReport:
    def __init__(self,
                 name: str,
                 times: Union[List[float], float],
                 count: int,
                 ratio: float,
                 children: List["TaskReport"],
                 padding_name: int):
        self.name = name
        self.times = times if isinstance(times, list) else [times]
        self.count = count
        self.ratio = ratio
        self.children = children

        self.internal_time = None

        self.padding_name = padding_name
        self.unit_padding = PADDING_SECONDS
        self.avg_duration_padding = len(self.formatted_avg_duration)

    @property
    def avg_duration(self):
        return sum(self.times) / len(self.times)

    @property
    def total_duration(self):
        return sum(self.times)

    @property
    def formatted_duration(self):
        return reformat_units(self.total_duration)

    @property
    def formatted_avg_duration(self):
        return time_to_str(self.avg_duration)

    def print(self, prefix="", spacing=0, skip_first=False, unit_padding=PADDING_SECONDS, avg_duration_padding=0):
        self.unit_padding = unit_padding
        self.avg_duration_padding = avg_duration_padding

        if not skip_first:
            print(self.__str__())

        if self.children:
            child_unit_padding = max([len(child.formatted_duration[1]) for child in self.children])
            child_avg_duration_padding = max([len(child.formatted_avg_duration) for child in self.children])

            for i, child in enumerate(self.children):
                if i == len(self.children) - 1 or len(child.children) > 1:
                    print(" " * spacing + f"└── {child}")
                    if child.children:
                        child.print(prefix=prefix + " ", spacing=spacing + 4, skip_first=True,
                                    unit_padding=child_unit_padding, avg_duration_padding=child_avg_duration_padding)
                else:
                    print(" " * spacing + f"├── {child}")
                    if child.children:
                        child.print(prefix=prefix + "│", spacing=spacing + 4, skip_first=True,
                                    unit_padding=child_unit_padding, avg_duration_padding=child_avg_duration_padding)

        if self.internal_time is not None:
            internal_time = self.internal_time
            internal_time_ratio = self.internal_time / self.total_duration

            # change unit to ms if internal time is too small, if still too small, change to us
            internal_time, unit = reformat_units(internal_time, start_unit="seconds")

            print(" " * spacing + f"└── {format_percentage(internal_time_ratio)} "
                                  f"internal time: {internal_time:{constants.DURATION_FORMAT}} {unit}")

    @classmethod
    def from_dict(cls, task_report_dict: dict, padding_name=0):
        padding_children = 0
        children = []
        if "subtasks" in task_report_dict:
            for child in task_report_dict["subtasks"].values():
                padding_children = max(padding_children, len(child["name"]))
                children.append(cls.from_dict(child, padding_name=padding_children))

        return cls(
            name=task_report_dict["name"],
            times=task_report_dict["times"],
            count=task_report_dict["count"],
            ratio=task_report_dict["ratio"],
            children=children,
            padding_name=padding_name
        )

    def __str__(self):
        ratio_str = f"{format_percentage(self.ratio)} " if self.ratio < 1 else ""
        name_str = f"{self.name:{self.padding_name}}" if self.padding_name > 0 else self.name

        count_str = f"{self.count} times" if self.count > 1 else ""
        avg_duration_str = f"avg {time_to_str(self.avg_duration):{self.avg_duration_padding}}" if self.count > 1 else ""

        to_print = [
            constants.PREFIX,
            f"{ratio_str}{name_str}",
            f"{self.formatted_duration[0]:{constants.DURATION_FORMAT}} {self.formatted_duration[1]:{self.unit_padding}}",
            f"{count_str}",
            f"{avg_duration_str}"
        ]

        to_print = [x for x in to_print if x != ""]

        return constants.SEPERATOR.join(to_print)

    def __repr__(self):
        return self.__str__()
