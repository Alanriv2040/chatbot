import os
import json
import random
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# ——————————————————————————————
#  Configuración / Variables de entorno
# ——————————————————————————————
# Define estas variables en tu entorno:
#   TWILIO_ACCOUNT_SID
#   TWILIO_AUTH_TOKEN
#   TWILIO_WHATSAPP_NUMBER  (p.ej: "whatsapp:+14155238886")
TWILIO_ACCOUNT_SID     = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN      = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Inicializa Flask y el cliente de Twilio
app = Flask(__name__)
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ——————————————————————————————
#  Carga de intents (solo lectura)
# ——————————————————————————————
with open('intents.json', 'r', encoding='utf-8') as f:
    INTENTS = json.load(f)['intents']


def responder(mensaje: str) -> str:
    text = mensaje.lower().strip()
    for intent in INTENTS:
        for pat in intent['patterns']:
            if pat.lower() in text:
                return random.choice(intent['responses'])
    return "Lo siento, no entendí eso."

# ——————————————————————————————
#  Ruta /whatsapp para el webhook
# ——————————————————————————————
@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    reply = responder(incoming_msg)
    resp.message(reply)
    return str(resp)

if __name__ == '__main__':
    # Ejecuta el servidor local en el puerto 5000
    app.run(host='0.0.0.0', port=5000)