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

# Função que define o título e a descrição do compromisso
def compromisso():
  print('Digite o nome do compromisso')
  titulo = input()
  print('Digite a descrição do seu compromisso - (Se optar por não colocar, enviar vazio)')
  descricao = input()
  
  return titulo, descricao

# Função que define a data do compromisso
def data():
  print('Digite a data do compromisso no formato dia-mês-ano')
  data = datetime.datetime.strptime(input(), '%d-%m-%Y').strftime('%Y-%m-%d')
  print('Digite a hora de início do compromisso no formato hora:minuto')
  hora_inicial = input() + ':00-03:00'
  print('Digite a hora do final do compromisso no formato hora:minuto')
  hora_final = input() + ':00-03:00'
  inicio = data + 'T' + hora_inicial
  fim = data + 'T' + hora_final
  return inicio, fim

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

# Função para enviar email
def email(titulo):
  msg = EmailMessage()
  email_sender = os.getenv('email_sender')
  email_receiver = os.getenv('email_receiver')
  password = os.getenv('password')
  
  msg['Subject'] = titulo.upper()
  msg['From'] = email_sender
  msg['To'] = email_receiver
  msg.set_content(f'O seu compromisso {titulo.upper()} é hoje')
  
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_sender, password)
    smtp.send_message(msg)

if __name__ == '__main__':
  titulo, descricao = compromisso()
  inicio, fim = data()
  main(inicio, fim, titulo, descricao)
  email(titulo=titulo)
