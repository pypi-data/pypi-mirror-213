import random

from timeitpoj.utils import constants


def reformat_units(value: float, start_unit="seconds"):
    unit_order = ["seconds", "milliseconds", "microseconds", "nanoseconds"]
    unit_index = unit_order.index(start_unit)

    while value < 0.1 and unit_index < len(unit_order) - 1:
        value *= 1000
        unit_index += 1

    return value, unit_order[unit_index]


def time_to_str(value: float, unit: str = "seconds", time_format=constants.DURATION_FORMAT):
    nvalue, nunit = reformat_units(value, unit)
    return f"{nvalue:{time_format}} {nunit}"


def format_percentage(value: float, include_brackets=True):
    percentage = f"{value:{constants.PERCENTAGE_FORMAT}}"
    percentage = f"{percentage:>6}"
    if include_brackets:
        percentage = f"[{percentage}]"
    return percentage


def random_task_name():
    adjectives = ['green', 'blue', 'red', 'yellow', 'orange', 'purple']
    nouns = ['apple', 'pistachio', 'ocean', 'sun', 'moon', 'mountain']

    adjective = random.choice(adjectives)
    noun = random.choice(nouns)

    number = random.randint(0, 100)

    return f"task {adjective} {noun} {number}"
