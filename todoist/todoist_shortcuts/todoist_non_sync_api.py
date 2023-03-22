import re
import os
import typing as T
from datetime import date, datetime, timedelta
from queue import Queue

import pyto_ui as ui
from notifications import Notification, send_notification
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task

# import json
# import sys
# from datetime import date, datetime, time, timedelta
# from pprint import pprint


def trunc_to_minutes(date_time: datetime):
    return date_time.replace(second=0, microsecond=0)


DURATION_REGEX = re.compile("//(\\d+)m")
DEFAULT_FILTER = "#Main & today"
NO_TIME_DELTA = timedelta()
TODAY = date.today()
TIME_STR_FORMAT = "%I:%M%p"
NOW = trunc_to_minutes(datetime.now())


class InputTextView:
    def __init__(
        self,
        label_text: str,
        input_queue: "Queue[str]",
        default_value: str = "",
        text_is_number: bool = False,
    ):
        self.input_queue = input_queue

        self.view = self.create_view()
        self.label = self.create_label(label_text)
        self.text_field = self.create_text_field(default_value, text_is_number)
        ui.show_view(self.view, ui.PRESENTATION_MODE_SHEET)

    def create_view(self):
        view = ui.View()
        view.background_color = ui.COLOR_SYSTEM_BACKGROUND

        return view

    def create_label(self, label_text: str):
        label = ui.Label()
        label.text_alignment = ui.TEXT_ALIGNMENT_CENTER
        label.size = (self.view.width, 50)
        label.flex = [ui.FLEXIBLE_WIDTH]

        label.text = label_text

        self.view.add_subview(label)

        return label

    def create_text_field(self, default_value: str, text_is_number: bool):
        text_field = ui.TextField(text=default_value)
        text_field.become_first_responder()
        text_field.width = 200
        text_field.center = (self.view.width / 2, self.view.height / 2)
        text_field.flex = [
            ui.FLEXIBLE_BOTTOM_MARGIN,
            ui.FLEXIBLE_TOP_MARGIN,
            ui.FLEXIBLE_LEFT_MARGIN,
            ui.FLEXIBLE_RIGHT_MARGIN,
        ]

        if text_is_number:
            text_field.keyboard_type = ui.KEYBOARD_TYPE_NUMBER_PAD

        text_field.did_end_editing = self.done_editing_cb

        self.view.add_subview(text_field)

        return text_field

    def done_editing_cb(self, sender: ui.TextField):
        sender_text = sender.text
        self.view.close()
        self.input_queue.put(sender_text)


def get_text_input(
    label_text: str, default_value: str = "", text_is_number: bool = False
) -> str:
    input_queue: "Queue[str]" = Queue()
    input_view = InputTextView(label_text, input_queue, default_value, text_is_number)
    return input_queue.get()


def get_task_filter() -> str:
    return get_text_input("Input task filter", "#Main & today")


def get_duration_for_task(task: Task) -> T.Optional[int]:
    match = DURATION_REGEX.search(task.content)
    if not match:
        return None

    duration_str = match.group(1)
    duration = int(duration_str)

    return duration


def get_duration_for_tasks(tasks: T.Iterable[Task]) -> int:
    return sum((get_duration_for_task(task) or 0 for task in tasks))


def format_duration(duration: int) -> str:
    delta = timedelta(minutes=duration)
    return str(delta)[:-3]


def format_time(date_time: datetime) -> str:
    if NOW.day == date_time.day:
        return date_time.strftime(TIME_STR_FORMAT)

    return date_time.strftime(f"Tomorrow, {TIME_STR_FORMAT}")


def get_end_time(
    duration: int, start_time: datetime, break_duration: int = 0
) -> datetime:
    break_delta = timedelta(minutes=break_duration)
    duration_delta = timedelta(minutes=duration)
    end_time = start_time + duration_delta + break_delta

    return end_time


def diff_from_goal_end_time(goal_end_time: datetime, actual_end_time: datetime) -> str:
    time_over = actual_end_time - goal_end_time
    if time_over < NO_TIME_DELTA:
        time_over = NO_TIME_DELTA - time_over
        return f"{str(time_over)[:-3]} extra time"

    return f"{str(time_over)[:-3]} over time"


def convert_time_str_to_datetime(time_str: str) -> datetime:
    date_time = datetime.strptime(time_str, TIME_STR_FORMAT)
    date_time = date_time.replace(TODAY.year, TODAY.month, TODAY.day)
    return trunc_to_minutes(date_time)


def get_tasks_by_filter(api: TodoistAPI, task_filter: str) -> T.Iterable[Task]:
    if task_filter:
        return api.get_tasks(filter=task_filter)

    return api.get_tasks()


def get_start_time() -> datetime:
    start_time_str = get_text_input("Input start time (either a time or 'now')", "now")
    if start_time_str.lower() == "now":
        start_time = NOW
    else:
        start_time = convert_time_str_to_datetime(start_time_str)

    return trunc_to_minutes(start_time)


def get_break_duration() -> int:
    return int(get_text_input("Input break duration", "0", True))


def get_goal_end_time_str() -> str:
    return get_text_input("Input goal end time", "6:00pm")


def get_action_input() -> str:
    # TODO:D
    return "get_total_time"
    # return "get_ending_time"
    # return "get_diff_from_goal_end_time"


# def get_group_by_input() ->


# def create_group_by_filters() -> str:
#     # TODO:D
#     VALID_GROUP_BY_OPTIONS = {
#         "priorities": ["p1", "p2", "p3", "p4"],
#         # "days": False,
#         "labels": [
#             "@active",
#             "@required",
#             "@committed",
#             "@low-commitment",
#             "@undated-but-important",
#         ],
#     }


#     return "priorities"


def get_total_time(tasks: T.Iterable[Task]) -> str:
    # TODO:PI add group by
    duration = get_duration_for_tasks(tasks)
    return format_duration(duration)


def get_end_time_for_tasks(tasks: T.Iterable[Task]) -> str:
    start_time = get_start_time()
    break_duration = get_break_duration()

    duration = get_duration_for_tasks(tasks)
    end_time = get_end_time(duration, start_time, break_duration)

    return format_time(end_time)


def how_far_over_goal_time(tasks: T.Iterable[Task]) -> str:
    start_time = get_start_time()
    break_duration = get_break_duration()
    goal_end_time_str = get_goal_end_time_str()
    goal_end_time = convert_time_str_to_datetime(goal_end_time_str)

    duration = get_duration_for_tasks(tasks)
    actual_end_time = get_end_time(duration, start_time, break_duration)

    return diff_from_goal_end_time(goal_end_time, actual_end_time)


def get_action_method() -> T.Callable[[T.Iterable[Task]], str]:
    ACTION_OPTION_TO_METHOD_DICT: T.Dict[str, T.Callable[[T.Iterable[Task]], str]] = {
        "get_total_time": get_total_time,
        "get_ending_time": get_end_time_for_tasks,
        "get_diff_from_goal_end_time": how_far_over_goal_time,
    }

    action_input = get_action_input()

    action_method = ACTION_OPTION_TO_METHOD_DICT.get(action_input)

    if action_method is None:
        raise ValueError(
            f"Invalid action input. Value was: {action_input}. Allowable values: {', '.join(ACTION_OPTION_TO_METHOD_DICT.keys())}"
        )

    return action_method


def get_notification_text(api: TodoistAPI) -> str:
    task_filter = get_task_filter()
    tasks = get_tasks_by_filter(api, task_filter)
    action_method = get_action_method()

    return action_method(tasks)


def send_notifications(api: TodoistAPI):
    notification_text = get_notification_text(api)
    send_notification(Notification(notification_text))


def main():
    api = TodoistAPI(os.environ.get("TODOIST_API_KEY"))
    send_notifications(api)
    api._session.close()


if __name__ == "__main__":
    main()


# main()

# what data we might want:
# get total time (only this allows groupings)
# get ending time
# get time over desired ending time

# if calculating ending time, we would need:
# start time (custom, default, or now if today)
# end time (custom or default)
# time between tasks
# total additional breaks

# filter tasks by:
# Project (Main, Inbox, All)
# Day (overdue, overdue + today, today, ...), or range
# Labels
# Custom

# Group times by
# day (if range)
# priority
# labels
# multiple group bys

# GLOBAL_ARGS = []

# "get_total_time"
# "get_ending_time"
# "time_over_desired_ending_time"


# task1 = tasks[0]
# task2 = tasks[2]

# td1 = task1.to_dict()
# td2 = task2.to_dict()
# pprint(td1)

# match = DURATION_REGEX.search(task1.content)
# match.group(1)

# projects = api.get_projects()
# sections = api.get_sections()
# labels = api.get_labels()
# api.get_comments()

# pprint(projects)
# pprint(labels)


# def get_argument(args, key, default=None):
#     arg = args.get(key, default)
#     if arg is None:
#         raise ValueError(f"argument: {key} is not present, but is required.")

#     return arg


# args_json = sys.argv[1]
# args = json.loads(args_json)

# action = get_argument(args, "action")
