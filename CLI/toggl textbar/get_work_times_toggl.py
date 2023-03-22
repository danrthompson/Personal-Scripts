import os

import click
import requests
from datetime import datetime, timedelta

# AI Thinking learning 186181594
# investments 187316243
# special work projects 188326563
# work planning 188079427
# AI Project implementation 189390036

# work med prod 186193242
# thinking discussing 187041688
# tooling 186181587

# personal chores 188045536
# routines 187633817
# chores 186676441
# SP cleaning room 188537695
# exercise 186944059

# mindless 187986408

CONFIG_DICT = {
    "tooling": {
        "project_ids": [186181587],
        "today": "/Users/danthompson/Code/Scripts/CLI/toggl textbar/opt_tooling_time_today.txt",
        "last_week": "/Users/danthompson/Code/Scripts/CLI/toggl textbar/opt_tooling_time_last_week.txt",
    },
    "work": {
        "project_ids": [186181594, 188079427, 187316243, 188326563, 189390036],
        "today": "/Users/danthompson/Code/Scripts/CLI/toggl textbar/total_work_time_today.txt",
        "last_week": "/Users/danthompson/Code/Scripts/CLI/toggl textbar/total_work_time_last_week.txt",
    },
}

PROJECT_TYPES = list(CONFIG_DICT.keys())
TIME_OPTIONS = ["today", "last_week"]

DATE_FORMAT = "%Y-%m-%d"


def get_time_entries(start_date, project_ids, end_date=None):
    if end_date is None:
        end_date = datetime.now().strftime(DATE_FORMAT)
    url = "https://api.track.toggl.com/reports/api/v3/workspace/397836/summary/time_entries"
    headers = {"Content-Type": "application/json"}
    auth = (os.environ.get("TOGGL_API_KEY"), "api_token")
    payload = {
        "start_date": start_date,
        "end_date": end_date,
        "project_ids": project_ids,
    }

    response = requests.post(url, headers=headers, auth=auth, json=payload)
    response_json = response.json()
    subgroups = (group["sub_groups"] for group in response_json["groups"])
    nested_subgroups = (subgroup for subgroup in subgroups for subgroup in subgroup)
    return sum([subgroup["seconds"] for subgroup in nested_subgroups])


def get_current_time_entry(project_ids):
    url = "https://api.track.toggl.com/api/v9/me/time_entries/current"
    headers = {"Content-Type": "application/json"}
    auth = (os.environ.get("TOGGL_API_KEY"), "api_token")

    response = requests.get(url, headers=headers, auth=auth)
    response_json = response.json()

    if (
        not response_json
        or "start" not in response_json
        or "project_id" not in response_json
        or response_json["project_id"] not in project_ids
    ):
        return None

    return response_json["start"]


def get_time_from_current_time_entry(project_ids):
    start_time_str = get_current_time_entry(project_ids)
    if not start_time_str:
        return 0

    start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S%z")

    return int((datetime.now(start_time.tzinfo) - start_time).total_seconds() / 60)


def get_total_time(project_ids, start_date, current_time, file_name, end_date=None):
    summary = get_time_entries(start_date, project_ids)
    total_mins = current_time + int(summary / 60)
    with open(file_name, "w") as f:
        f.write(str(total_mins))

    return total_mins


def get_project_ids_and_file_name(time, project_type):
    project = CONFIG_DICT[project_type]
    project_ids = project["project_ids"]
    file_name = project[time]
    return project_ids, file_name


def get_last_week_and_today_time(time: str, project_type: str):
    project_ids, file_name = get_project_ids_and_file_name(time, project_type)

    current_time = get_time_from_current_time_entry(project_ids)

    if time == "today":
        start_date = datetime.now().strftime(DATE_FORMAT)
    else:
        start_date = (datetime.now() - timedelta(days=6)).strftime(DATE_FORMAT)

    return get_total_time(project_ids, start_date, current_time, file_name)


def echo_time_formatted(total_time):
    click.echo(f"{total_time // 60}:{total_time % 60:02d}")


def get_total_time_from_file(time, project_type):
    _, file_name = get_project_ids_and_file_name(time, project_type)
    with open(file_name, "r") as f:
        total_time = int(f.read())

    return total_time


@click.group()
def cli():
    pass


@cli.command()
@click.option("--time", type=click.Choice(TIME_OPTIONS), default=None)
@click.option("--project-type", type=click.Choice(PROJECT_TYPES), default=None)
@click.option("--echo", type=click.Choice(["y", "n"]), default="n")
def fetch_time(time, project_type, echo):
    if time is not None:
        times = [time]
    else:
        times = TIME_OPTIONS

    if project_type is not None:
        project_types = [project_type]
    else:
        project_types = PROJECT_TYPES

    if echo == "y":
        echo = True
    else:
        echo = False

    for project_type in project_types:
        for time in times:
            total_time = get_last_week_and_today_time(time, project_type)
            if echo:
                click.echo(f"Project type: {project_type}, time: {time}")
                echo_time_formatted(total_time)


@cli.command()
@click.option("--time", type=click.Choice(TIME_OPTIONS), required=True)
@click.option("--project-type", type=click.Choice(PROJECT_TYPES), required=True)
def get_echo_time(time, project_type):
    total_time = get_total_time_from_file(time, project_type)
    echo_time_formatted(total_time)


@cli.command()
@click.option("--time", type=click.Choice(TIME_OPTIONS), required=True)
@click.option("--project-type", type=click.Choice(PROJECT_TYPES), required=True)
def get_ratio(time, project_type):
    total_time = 0
    for this_project_type in PROJECT_TYPES:
        total_time += get_total_time_from_file(time, this_project_type)

    project_time = get_total_time_from_file(time, project_type)

    click.echo(f"{int(project_time * 100 / total_time)}")


if __name__ == "__main__":
    cli()
