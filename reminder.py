from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

calendar_service = build('calendar', 'v3', credentials=credentials)

def create_event(summary, start_time, end_time):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': end_time, 'timeZone': 'America/Los_Angeles'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30}
            ],
        },
    }
    created_event = calendar_service.events().insert(calendarId='primary', body=event).execute()
    return created_event['id']

# Example Usage
create_event(
    summary="Yoga Session",
    start_time="2024-11-20T18:00:00-08:00",
    end_time="2024-11-20T19:00:00-08:00"
)

# ALTERNATIVE

import schedule
import time

def notify_user():
    print("Reminder: Your training session starts in 30 minutes!")

# Schedule Notification
schedule.every().day.at("17:30").do(notify_user)

while True:
    schedule.run_pending()
    time.sleep(1)
