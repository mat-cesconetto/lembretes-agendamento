import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

data = input()
hora_inicial = input()
hora_final = input()
inicio = ''
fim = ''

def conversoes():
  data = datetime.datetime.strptime(data, '%d-%m-%Y')
  data = data.date()
  data = data.strftime('%Y-%m-%d')
  
  inicio = data + 'T' + hora_inicial + '-03:00'
  fim = data + 'T' + hora_final + '-03:00'


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    event = {
        'start': {
          # 'dateTime': '2024-07-24T09:00:00-03:00',
            'dateTime': inicio,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': fim,
            'timeZone': 'America/Sao_Paulo',
        },
        'summary': 'Teste',
        'description': 'Teste da descricao mulekada',
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
        ],
        'attendees': [
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    service = build("calendar", "v3", credentials=creds)

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
      


  except HttpError as error:
    print(f"An error occurred: {error}")


# if __name__ == "__main__":
#   main()

  
# 'dateTime': '2024-07-24T09:00:00-03:00',
conversoes()
main()