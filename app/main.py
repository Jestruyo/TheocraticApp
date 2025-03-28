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
    profile_name = request.form.get('ProfileName') # Nombre del perfil

    # Inicializar el estado del usuario si no existe
    if from_number not in user_state:
        user_state[from_number] = {'state': 'inicio'}

    # Manejar el flujo basado en el estado del usuario
    if user_state[from_number]['state'] == 'inicio':
        # Enviar mensaje de bienvenida
        client.messages.create(
            body='¡Hola! Que gusto saludarte. ¿Cuál es tu nombre?',
            from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
            to=from_number  # Número del usuario (formato WhatsApp)
        )
        user_state[from_number]['state'] = 'solicitar_nombre'

    elif user_state[from_number]['state'] == 'solicitar_nombre':
        # Guardar el nombre y pedir confirmación
        user_state[from_number]['nombre'] = message_body
        client.messages.create(
            body=f'*Estoy para servirte {message_body} 😊 ¿Como puedo ayudarte?* Ingresa el número de tu opción requerida: \n \n 🕒 *1. Hora de reuniones.* \n 🏠 *2. Lugares de Predicación.* \n 📝 *3. Envio de informes.* \n 📋 *4. Solicitudes y formularios.*',
            from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
            to=from_number  # Número del usuario (formato WhatsApp)
        )
        user_state[from_number]['state'] = 'validar_solicitud'

    elif user_state[from_number]['state'] == 'validar_solicitud':
        if message_body.lower() == '1':
            # Confirmación exitosa
            client.messages.create(
                body=f'*Estos son los enlaces a la plataforma zoom:* \n \n 🖥️ *1. Reunión entre semana | Jueves 7 pm* \n 📌 https://jworg.zoom.us/j/99106008401 \n *Codigo de acceso:* 1234. \n \n 🖥️ *2. Reunión fin de semana | Domingo 5 pm* \n 📌 https://jworg.zoom.us/j/91928746645 \n *Codigo de acceso:* 1234. \n \n *¿Hay algo mas en lo que pueda ayudarte {user_state[from_number]["nombre"]}?*',
                from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
                to=from_number  # Número del usuario (formato WhatsApp)
            )
            user_state[from_number]['state'] = 'inicio'
        elif message_body.lower() == '2':
            # Pedir el nombre nuevamente
            client.messages.create(
                body=f'*A continuación te comparto los lugares de salida al servicio del campo:* \n \n *Lunes:* \n 🏫 *1. Salón del Reino* | \n Faceta (pública) Hora (6:50 pm). \n \n *Martes:* \n 🏠 *2. Hra Esther Rua* | \n Faceta (cartas) Hora (9:00 am). \n Faceta (casa en casa) Hora (4:30 pm). \n \n *Miercoles:* \n 🏠 *3. Hra Rosalba Serge* | \n Faceta (casa en casa) Hora (9:00 am). \n Faceta (casa en casa) Hora (4:30 pm)',
                from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
                to=from_number  # Número del usuario (formato WhatsApp)
            )
            user_state[from_number]['state'] = 'inicio'


    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)