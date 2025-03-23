from flask import Flask, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Credenciales de Twilio
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')  # Número de Twilio Sandbox (sin punto al final)

# Cliente de Twilio
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Almacenar el estado del usuario (en memoria, para producción usa una base de datos)
user_state = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    from_number = request.form.get('From')  # Número del usuario (formato WhatsApp)
    message_body = request.form.get('Body') # Cuerpo del mensaje

    # Inicializar el estado del usuario si no existe
    if from_number not in user_state:
        user_state[from_number] = {'state': 'inicio'}

    # Manejar el flujo basado en el estado del usuario
    if user_state[from_number]['state'] == 'inicio':
        # Enviar mensaje de bienvenida
        client.messages.create(
            body='¡Hola! Bienvenido. ¿Cuál es tu nombre?',
            from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
            to=from_number  # Número del usuario (formato WhatsApp)
        )
        user_state[from_number]['state'] = 'solicitar_nombre'

    elif user_state[from_number]['state'] == 'solicitar_nombre':
        # Guardar el nombre y pedir confirmación
        user_state[from_number]['nombre'] = message_body
        client.messages.create(
            body=f'Gracias, {message_body}. ¿Confirmas que este es tu nombre? (si/no)',
            from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
            to=from_number  # Número del usuario (formato WhatsApp)
        )
        user_state[from_number]['state'] = 'confirmar_datos'

    elif user_state[from_number]['state'] == 'confirmar_datos':
        if message_body.lower() == 'si':
            # Confirmación exitosa
            client.messages.create(
                body=f'Perfecto, {user_state[from_number]["nombre"]}. Gracias por tu dia de trabajo, a domir y comer.',
                from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
                to=from_number  # Número del usuario (formato WhatsApp)
            )
            user_state[from_number]['state'] = 'inicio'
        else:
            # Pedir el nombre nuevamente
            client.messages.create(
                body='Por favor, ingresa tu nombre nuevamente.',
                from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
                to=from_number  # Número del usuario (formato WhatsApp)
            )
            user_state[from_number]['state'] = 'solicitar_nombre'

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)