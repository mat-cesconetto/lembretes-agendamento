# Importando as bibliotecas necessárias
import datetime
import os.path
import dotenv
import smtplib
from dateutil import parser
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Link para estabelecer a conexão com o Google Calendar
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Carregando as variáveis de ambiente do arquivo .env
dotenv.load_dotenv(dotenv.find_dotenv())

def main(inicio, fim, titulo, descricao):
    """
    Cria um evento no Google Calendar.
    
    Args:
        inicio (str): Data e hora de início do evento no formato ISO 8601.
        fim (str): Data e hora de término do evento no formato ISO 8601.
        titulo (str): Título do evento.
        descricao (str): Descrição do evento.
    """
    creds = None
    # Verifica se o arquivo token.json existe e carrega as credenciais
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Se não houver credenciais válidas, realiza o login do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para futuras execuções
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Configura o evento a ser criado
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
        # Conecta ao serviço do Google Calendar e cria o evento
        service = build("calendar", "v3", credentials=creds)
        event = service.events().insert(calendarId='primary', body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print(f"Ocorreu um erro: {error}")

def proximos():
    """
    Lista os próximos 10 eventos do Google Calendar.

    Returns:
        str: Uma string formatada com os próximos eventos.
    """
    creds = None
    # Verifica se o arquivo token.json existe e carrega as credenciais
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Se não houver credenciais válidas, realiza o login do usuário
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para futuras execuções
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    resultado = ''
    
    try:
        # Conecta ao serviço do Google Calendar
        service = build("calendar", "v3", credentials=creds)
        
        # Obtém o horário atual em UTC
        now = datetime.datetime.utcnow().isoformat() + "Z"
        
        # Chama a API do Calendar para listar os eventos
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])

        if not events:
            resultado = "Nenhum evento futuro encontrado."

        # Formata a lista de eventos
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            data = parser.parse(start).date().strftime('%d/%m/%Y')
            hora1 = parser.parse(start).strftime('%H:%M')
            hora2 = parser.parse(end).strftime('%H:%M')
            resultado += f"{data} - ({hora1} - {hora2}) - {event.get('summary')}\n"
            
    except HttpError as error:
        resultado = f"Ocorreu um erro: {error}"
    return resultado

if __name__ == '__main__':
    proximos()
