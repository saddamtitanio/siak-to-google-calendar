import os
from datetime import datetime, timedelta
import os.path
from web_scraping import retrieve_courses
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 
from tzlocal import get_localzone

# CHANGE THIS TO THE START DATE OF UNIV
UNIV_START_DATE = datetime.now(get_localzone()).replace(year=2025, month=2, day=3).date()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

def get_day_increment(local_time, target_day):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    current_day = local_time.strftime('%A')

    day_index = days.index(current_day) if current_day in days else -1
    day_increment = 0

    while day_index != target_day:
        day_index = (day_index + 1) % len(days)
        day_increment += 1
    
    return day_increment

def get_calendarId():
    with open("config/userdata.txt", 'r') as file:
        lines = file.readlines()

    calendar_id = ''
    for line in lines:
        if line.startswith('CALENDARID='):
            calendar_id = line.strip().split('=')[1]

    return calendar_id

def parse_time(course_time, target_day):
    start_time, end_time = course_time.split(" - ")
    start_hour, start_minute = map(int, start_time.split("."))
    end_hour, end_minute = map(int, end_time.split("."))

    local_time = datetime.now(get_localzone())
    utc_offset_minutes = local_time.utcoffset().total_seconds() / 60

    # Convert the offset to hours and minutes
    offset_hours = int(utc_offset_minutes // 60)
    offset_minutes = int(utc_offset_minutes % 60)

    day_increment = get_day_increment(UNIV_START_DATE, target_day)

    modified_date = UNIV_START_DATE + timedelta(days=day_increment)

    timezone_offset = f"{'+' if offset_hours >= 0 else '-'}{abs(offset_hours):02}:{abs(offset_minutes):02}"

    start_datetime = modified_date.strftime('%Y-%m-%d') + 'T' + str(start_hour) + ':' + str(start_minute) + ":00" + timezone_offset
    end_datetime = modified_date.strftime('%Y-%m-%d') + 'T' + str(end_hour) + ':' + str(end_minute) + ":00" + timezone_offset

    return start_datetime, end_datetime

def create_events(service, calendar_id, courses):
    courses = retrieve_courses()
    timezone_name = get_localzone()

    for course in courses:
        start_time, end_time = parse_time(course['time'], course['day'])

        # Check if the event already exists
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            q=course['name'],
            timeZone=str(timezone_name)
        ).execute()

        existing_events = events_result.get('items', [])

        if not existing_events:
            # Event does not exist, create it
            event = {
                "summary": course['name'],
                "location": course['room'],
                "start": {
                    "dateTime": start_time,
                    "timeZone": str(timezone_name)
                },
                "end": {
                    "dateTime": end_time,
                    "timeZone": str(timezone_name)
                },
                "recurrence": ['RRULE:FREQ=WEEKLY']
            }
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"Event created: {event['summary']} at {event['start']['dateTime']}")
        else:
            print(f"Event already exists: {course['name']} at {start_time}")


def main():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    calendar_id = get_calendarId()

    try:
        service = build("calendar", "v3", credentials=creds)
        courses = retrieve_courses()
        create_events(service, str(calendar_id), courses)

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()