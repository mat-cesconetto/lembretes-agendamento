# Importando as bibliotecas
import datetime
import os.path
import dotenv
import smtplib
from email.message import EmailMessage
# Importando a api
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser
# Importando o outro arquivo (isso é feito pois o outro arquivo não rodaria diariamente propriamente, visto que o mesmo pediria todos os inputs)
<<<<<<< HEAD
import app1
=======
import app
>>>>>>> b7d6aef04c1c09fcab099139d569f41c16c19086

# Escopo para acessar o Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
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
    # Salva as credenciais para a próxima execução
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Chamando a API do Calendar
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indica a hora UTC
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

    for event in events:
      start = event["start"].get("dateTime")
      agora = datetime.datetime.utcnow().isoformat()
 
      # Envia email se o evento for hoje
      if parser.parse(start).date() == parser.parse(agora).date():
          app1.email(titulo=event['summary'])
      else:
          None
  except HttpError as error:
    print(f"Ocorreu um erro: {error}")
  
main()
