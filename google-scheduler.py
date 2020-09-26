import logging 
from datetime import datetime as dt
import pickle 
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gtts import gTTS
import calendar
# if modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials.json'

class google_scheduler(object):


    def __init__(self, account_name):
        self.account_name = account_name
               
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if creds == None or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def list_events(self):
        now = dt.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting List of 10 events')
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
        print(events)   
        if not events:
            print('No upcoming events found.')
        welcome_msg = "Hey Kent, we have found {} events".format(len(events))
        audio = gTTS(text=welcome_msg, lang='en', slow=False)
        audio.save("welcome.mp3")
        os.system("mpg321 welcome.mp3")
        os.remove("welcome.mp3")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
        
            # date = event['start']['datetime'] or event['start']['date']
            for key in event['start']:
                year = event['start'][key][0:4]
                month = calendar.month_name[int(event['start'][key][5:7])]
                day = event['start'][key][8:10]
                print(year, month, day)
                if key == "dateTime":
                    hour = int(event['start'][key][11:13])
                    if hour < 12:
                        day_divider = "in the morning"
                    else:
                        hour = hour - 12
                        day_divider = "in the afternoon"
                    
                    minutes = int(event['start'][key][14:16])
                    if minutes == 0:
                        minutes = "oh clock"
                    seconds = int(event['start'][key][17:19])
                    if seconds == 0:
                        seconds = ""
            
            event_description = "{} on {} {} starting at {} {} {} utc time.".format(event['summary'], month, day, hour, minutes, day_divider)
            audio = gTTS(text=event_description, lang='en', slow=False)
            audio.save("event.mp3")
            os.system("mpg321 event.mp3")
            os.remove("event.mp3")

    def delete_events(self, eventid):
        '''
            Delete events
        
        '''
        try:
            self.service.events().delete(calendarId="primary", 
        eventid=eventid,).execute()

        except googleapiclient.errors.HttpError:
            print("Failed to delete event")

        print("Event deleted")

    def list_calendars(self):
        calendars_query = self.servic.calendarList().list().execute()
        calendars = calendars_query.get('items', [])

        if not calendars:
            print("No calendars found.")
        for calendar in calendars:
            summary = calendar['summary']
            primary = "Primary" if calendar.get('primary') else ""
            print("%s\t%s\t%s" % (summary, id, primary))

    def create_event(self):
        d = dt.now().date()
        tomorrow = dt(d.year, d.month, d.day, 10)+timedelta(days=1)
        start = tomorrow.isoformat()
        end = (tomorrow + timedelta(hours=1)).isoformat()

        event_result = self.service.events().insert(calendarId='primary', \
            body={ 
            "summary": 'Automating calendar', 
            "description": 'This is a tutorial example of automating google calendar with python',
            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'}, 
            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
            }
        ).execute()

        print("created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    def update_event(self):
        service = get_calendar_service()

        d = datetime.now().date()
        tomorrow = datetime(d.year, d.month, d.day, 9)+timedelta(days=1)
        start = tomorrow.isoformat()
        end = (tomorrow + timedelta(hours=2)).isoformat()

        event_result = service.events().update(
        calendarId='primary',
        eventId='4qnt0okd4dmr0hik3mh073qnls',
        body={ 
            "summary": 'Updated Automating calendar',
            "description": 'This is a tutorial example of automating google calendar with python, updated time.',
            "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'}, 
            "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
        },
        ).execute()

        print("updated event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])


if __name__ == "__main__":
    calendar_instance = google_scheduler("Kent").list_events()
    
