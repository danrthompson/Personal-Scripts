import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import sys

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_date_relative_to_today(relative_days: int) -> datetime.date:
    today = datetime.datetime.utcnow().date()
    target_date = today + datetime.timedelta(days=relative_days)
    return target_date

def main():
    relative_days = 0
    if len(sys.argv) > 1:
        try:
            relative_days = int(sys.argv[1])
        except ValueError:
            print("Invalid argument. Please provide an integer.")
            sys.exit(1)

    target_date = get_date_relative_to_today(relative_days)
    start_of_day = datetime.datetime(target_date.year, target_date.month, target_date.day)
    end_of_day = start_of_day + datetime.timedelta(days=1)

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)

    start_of_day_iso = start_of_day.isoformat() + 'Z'
    end_of_day_iso = end_of_day.isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='source_calendar_id',
        timeMin=start_of_day_iso,
        timeMax=end_of_day_iso,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print(f'No upcoming events found for {target_date}.')
        return

    for event in events:
        if 'recurrence' in event or 'recurringEventId' in event:
            continue  # Skip recurring events

        new_event = {
            'summary': event['summary'],
            'description': event.get('description', ''),
            'start': event['start'],
            'end': event['end'],
            'colorId': event.get('colorId', '1'),
            'transparency': event.get('transparency', 'opaque'),
            'status': event.get('status', 'confirmed'),
        }

        service.events().insert(calendarId='target_calendar_id', body=new_event).execute()

if __name__ == '__main__':
    main()
