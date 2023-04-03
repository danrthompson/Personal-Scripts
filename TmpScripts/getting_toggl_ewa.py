import os
from urllib.parse import urlencode
from typing import Optional
from datetime import date, datetime, timedelta


import requests
import pytz

DATE_FORMAT = "%Y-%m-%d"


def get_time_entries(
    end_date: Optional[datetime] = None, num_days: int = 30
) -> list[dict]:
    if not end_date:
        end_date = datetime.now()
    start_date_str = (end_date - timedelta(days=num_days)).strftime(DATE_FORMAT)

    end_date_str = datetime.now().strftime(DATE_FORMAT)
    endpoint = "https://api.track.toggl.com/api/v9/me/time_entries"
    headers = {"Content-Type": "application/json"}
    auth = (os.environ["TOGGL_API_KEY"], "api_token")
    payload = {
        "start_date": start_date_str,
        "end_date": end_date_str,
    }
    query_string = urlencode(payload)
    url = f"{endpoint}?{query_string}"

    response = requests.get(url, headers=headers, auth=auth, timeout=10)
    return response.json()


def get_hours_worked_per_day(
    entries: list[dict],
    project_ids: Optional[set[int]] = None,
    end_date: Optional[date] = None,
    num_days: int = 30,
) -> list[float]:
    if not end_date:
        end_date = date.today()
    start_date = end_date - timedelta(days=num_days)

    # filter out time entries that are not in the specified project ids
    if project_ids:
        entries = [entry for entry in entries if entry["pid"] in project_ids]

    # Define NYC timezone
    nyc_timezone = pytz.timezone("America/New_York")

    # Initialize dictionary to store total hours worked per day
    hours_per_day = {}

    # Loop through each time entry
    for entry in entries:
        # Convert start and end times to datetime objects in UTC timezone
        start_time = datetime.strptime(entry["start"], "%Y-%m-%dT%H:%M:%S%z")
        if entry["stop"] is not None:
            end_time = datetime.strptime(entry["stop"], "%Y-%m-%dT%H:%M:%S%z")
        else:
            end_time = datetime.now(pytz.utc)

        # Convert start and end times to NYC timezone
        start_time_nyc = start_time.astimezone(nyc_timezone)

        # Determine the day that the time entry took place on, in NYC timezone
        day_nyc: date = start_time_nyc.date()

        # If the day is within the specified range, add the duration to the total hours for that day
        if start_date <= day_nyc <= end_date:
            duration = (end_time - start_time).total_seconds() / 3600
            if day_nyc not in hours_per_day:
                hours_per_day[day_nyc] = duration
            else:
                hours_per_day[day_nyc] += duration

    # Generate list of hours worked per day, with 0 hours for days with no time entries
    hours_worked_per_day = []
    current_day = start_date
    while current_day <= end_date:
        if current_day in hours_per_day:
            hours_worked_per_day.append(hours_per_day[current_day])
        else:
            hours_worked_per_day.append(0)
        current_day += timedelta(days=1)

    return hours_worked_per_day


# def get_time_entries(start_date, project_ids, end_date=None):
#     if end_date is None:
#         end_date = datetime.now().strftime(DATE_FORMAT)
#     url = "https://api.track.toggl.com/reports/api/v3/workspace/397836/summary/time_entries"
#     headers = {"Content-Type": "application/json"}
#     auth = (os.environ.get("TOGGL_API_KEY"), "api_token")
#     payload = {
#         "start_date": start_date,
#         "end_date": end_date,
#         "project_ids": project_ids,
#     }

#     response = requests.post(url, headers=headers, auth=auth, json=payload)
#     response_json = response.json()
#     subgroups = (group["sub_groups"] for group in response_json["groups"])
#     nested_subgroups = (subgroup for subgroup in subgroups for subgroup in subgroup)
#     return sum([subgroup["seconds"] for subgroup in nested_subgroups])
