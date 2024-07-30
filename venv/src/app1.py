# Importando as bibliotecas
import datetime
import os.path
import dotenv
import smtplib
from email.message import EmailMessage
# Importando a API do Google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Link para estabelecer a conexão com o calendário
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Procurando e carregando o ambiente virtual
dotenv.load_dotenv(dotenv.find_dotenv())

# Função para criar compromissos e conectar com o Google Calendar
def main(inicio, fim, titulo, descricao):
  """Mostra o uso básico da API do Google Calendar.
  Imprime o início e o nome dos próximos 10 eventos no calendário do usuário.
  """
  creds = None
  # O arquivo token.json armazena os tokens de acesso e atualização do usuário, 
  # e é criado automaticamente quando o fluxo de autorização é concluído pela primeira vez.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # Se não houver credenciais válidas disponíveis, faça o login do usuário.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Salva as credenciais
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Criando o evento
    event = {
        'start': {
            'dateTime': inicio,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': fim,
            'timeZone': 'America/Sao_Paulo',
        },
        'summary': titulo,
        'description': descricao,
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=1'
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

    # Chamando a API do Calendar
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indica a hora UTC
    print("Próximos 10 eventos na sua agenda")
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
      print("Nenhum evento futuro encontrado.")
      return

    # Mostra o início e o nome dos próximos 10 eventos
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
      
  except HttpError as error:
    print(f"Ocorreu um erro: {error}")

if __name__ == '__main__':
  main()
