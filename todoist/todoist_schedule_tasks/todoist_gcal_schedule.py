import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from todoist_api_python.api import TodoistAPI

SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=60546)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

service = build("calendar", "v3", credentials=creds)
calendar = service.calendarList().list().execute()

service.events().list(
    calendarId="iratsnl6jo8k7mor2sb0dtuq48@group.calendar.google.com"
).execute()

# events are a list of dictionaries. each dictionary has a start and end time.
# write a function that takes a list of events and a duration and return a time
# that has at least duration minutes free
def get_free_time(events, duration):
    # sort events by start time
    events.sort(key=lambda event: event["start"]["dateTime"])
    # get the first event
    first_event = events[0]
    # get the start time of the first event
    first_event_start = first_event["start"]["dateTime"]
    # get the end time of the first event
    first_event_end = first_event["end"]["dateTime"]
    # get the start time of the first event as a datetime object
    first_event_start_datetime = datetime.datetime.strptime(
        first_event_start, "%Y-%m-%dT%H:%M:%S%z"
    )
    # get the end time of the first event as a datetime object
    first_event_end_datetime = datetime.datetime.strptime(
        first_event_end, "%Y-%m-%dT%H:%M:%S%z"
    )
    # get the difference between the start and end time of the first event
    first_event_duration = first_event_end_datetime - first_event_start_datetime
    # if the duration of the first event is greater than the duration we're looking for
    if first_event_duration > duration:
        # return the start time of the first event
        return first_event_start_datetime
    # if the duration of the first event is less than the duration we're looking for
    else:
        # get the end time of the first event
        first_event_end = first_event["end"]["dateTime"]
        # get the end time of the first event as a datetime object
        first_event_end_datetime = datetime.datetime.strptime(
            first_event_end, "%Y-%m-%dT%H:%M:%S%z"
        )
        # get the start time of the second event
        second_event_start = events[1]["start"]["dateTime"]
        # get the start time of the second event as a datetime object
        second_event_start_datetime = datetime.datetime.strptime(
            second_event_start, "%Y-%m-%dT%H:%M:%S%z"
        )
        # get the difference between the end time of the first event and the start time of the second event
        time_between_events = second_event_start_datetime - first_event_end_datetime
        # if the difference between the end time of the first event and the start time of the second event is greater than the duration we're looking for
        if time_between_events > duration:
            # return the end time of the first event




# events are a list of dictionaries. each dictionary has a start and end time.
# the start time and end time are strings in the format 2018-11-13T19:00:00-08:00.
# write a function that takes a list of events, and also takes a list of durations.
# return a list of start times that have enough time free to fit the durations.
def get_free_times(events, durations):
    # sort events by start time
    events.sort(key=lambda event: event["start"]["dateTime"])
    # sort durations by length
    durations.sort()
    # get the first event
    first_event = events[0]
    # get the start time of the first event
    first_event_start = first_event["start"]["dateTime"]
    # get the end time of the first event
    first_event_end = first_event["end"]["dateTime"]
    # get the start time of the first event as a datetime object
    first_event_start_datetime = datetime.datetime.strptime(
        first_event_start, "%Y-%m-%dT%H:%M:%S%z"
    )
    # get the end time of the first event as a datetime object
    first_event_end_datetime = datetime.datetime.strptime(
        first_event_end, "%Y-%m-%dT%H:%M:%S%z"
    )
    # get the difference between the start and end time of the first event
    first_event_duration = first_event_end_datetime - first_event_start_datetime
    # if the duration of the first event is greater than the duration we're looking for
    if first_event_duration > durations[0]:
        # return the start time of the first event
        return first_event_start_datetime
    # if the duration of the first event is less than the duration we're looking for
    else:
        # get the end time of the first event
        first_event_end = first_event["end"]["dateTime"]
        # get the end time of the first event as a datetime object
        first_event_end_datetime = datetime.datetime.strptime(
            first_event_end, "%Y-%m-%dT%H:%M:%S%z"
        )
        # get the start time of the second event
        second_event_start = events[1]["start"]["dateTime"]
        # get the start time of the second event as a datetime object
        second_event_start_datetime = datetime.datetime.strptime(
            second_event_start, "%Y-%m-%dT%H:%M:%S%z"
        )
        # get the difference between the end time of the first event and the start time of the second event
        time_between_events = second_event_start_datetime - first_event_end_datetime
        # if the difference between the end time of the first event and the start time of the second event is greater than the duration we're looking for
        if time_between_events > durations:
            # return the end time of the first event
            return first_event_end_datetime