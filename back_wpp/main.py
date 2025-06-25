from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste para seu domínio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ULTRA_TOKEN = os.getenv("ULTRA_TOKEN")
ULTRA_INSTANCE = os.getenv("ULTRA_INSTANCE")

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service-account.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
calendar_service = build('calendar', 'v3', credentials=credentials)

@app.post("/agendar")
async def agendar(request: Request):
    data = await request.json()
    nome = data.get("nome")
    telefone = data.get("telefone")
    servico = data.get("servico")
    data_preferida = data.get("dataPreferida")  # ISO 8601 string

    try:
        start_dt = datetime.fromisoformat(data_preferida)
    except Exception:
        return {"error": "Formato de data inválido. Use ISO 8601."}

    end_dt = start_dt + timedelta(hours=1)

    evento = {
        'summary': f'Agendamento - {nome}',
        'description': f'Serviço: {servico}',
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'America/Sao_Paulo'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
                {'method': 'email', 'minutes': 60},
            ],
        },
    }

    evento_criado = calendar_service.events().insert(calendarId='primary', body=evento).execute()

    telefone_formatado = telefone.strip().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if not telefone_formatado.startswith("55"):
        telefone_formatado = "55" + telefone_formatado

    mensagem = (
        f"Olá {nome}, seu agendamento para *{servico}* no dia "
        f"{start_dt.strftime('%d/%m/%Y %H:%M')} foi confirmado! Até breve! ✂️"
    )

    response = requests.post(
        f"https://api.ultramsg.com/{ULTRA_INSTANCE}/messages/chat",
        json={
            "token": ULTRA_TOKEN,
            "to": telefone_formatado,
            "body": mensagem
        }
    )

    return {
        "status": "ok",
        "evento_link": evento_criado.get('htmlLink'),
        "whatsapp_response": response.json()
    }
