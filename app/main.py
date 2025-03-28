from flask import Flask, request, jsonify
from twilio.rest import Client
from utils import ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE, USER_ADMIN

app = Flask(__name__)

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
    if user_state[from_number]['state'] == 'inicio' and from_number == USER_ADMIN['number']:
        # Guardar el nombre en el estado del usuario
        user_state[from_number]['nombre'] = USER_ADMIN['name']
        # Enviar mensaje de bienvenida
        client.messages.create(
            body=f'*¡Hola! Que gusto saludarte {USER_ADMIN["name"]} 😊 ¿Como puedo ayudarte?*\
                  \n Ingresa el número de tu opción requerida:\
                  \n \n 🕒 *1. Hora de reuniones.*\
                  \n 🏠 *2. Lugares de Predicación.*\
                  \n 📝 *3. Envio de informes.*\
                  \n 📋 *4. Solicitudes y formularios.*\
                  \n 🚨 *5. Lineas de emergencia.*',
            from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
            to=from_number  # Número del usuario (formato WhatsApp)
        )
        user_state[from_number]['state'] = 'validar_solicitud'

    elif user_state[from_number]['state'] == 'validar_solicitud':
        if message_body.lower() == '1':
            # Confirmación exitosa
            client.messages.create(
                body=f'*Estos son los enlaces a la plataforma zoom:*\
                    \n \n 🖥️ *1. Reunión entre semana | Jueves 7 pm*\
                    \n 📌 https://jworg.zoom.us/j/99106008401\
                    \n *Codigo de acceso:* 1234.\
                    \n \n 🖥️ *2. Reunión fin de semana | Domingo 5 pm*\
                    \n 📌 https://jworg.zoom.us/j/91928746645\
                    \n *Codigo de acceso:* 1234.\
                    \n \n *¿Hay algo mas en lo que pueda ayudarte {user_state[from_number]["nombre"]}?*',
                from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
                to=from_number  # Número del usuario (formato WhatsApp)
            )
            user_state[from_number]['state'] = 'inicio'
        elif message_body.lower() == '2':
            # Pedir el nombre nuevamente
            client.messages.create(
                body=f'*A continuación te comparto los lugares de salida al servicio del campo:*\
                    \n \n *Lunes:*\
                    \n 🏫 *Salón del Reino* | \
                    \n Faceta (pública) Hora (6:50 pm). \
                    \n \n *Martes:*\
                    \n 🏠 *Hra Esther Rua* | \
                    \n Faceta (cartas) Hora (9:00 am). \
                    \n 🏠 *Hra Rosalba Serge* | \
                    \n Faceta (casa en casa) Hora (4:30 pm). \
                    \n \n *Miercoles:*\
                    \n 🏠 *Hra Maria Herrera* | \
                    \n Faceta (casa en casa) Hora (9:00 am). \
                    \n 🏠 *Hra Vanessa Villa* | \
                    \n Faceta (casa en casa) Hora (4:30 pm). \
                    \n \n *Jueves:*\
                    \n ❌ *No hay Predicación* | \
                    \n Dia de reunion. \
                    \n \n *Viernes:* \
                    \n 🏫 *Salón del Reino* | \
                    \n Faceta (cartas y llamadas) Hora (9:00 am). \
                    \n Faceta (por definir) Hora (4:30 pm). \
                    \n \n *Sabado:*\
                    \n 🏠 *Hra Vanessa Villa* | \
                    \n Faceta (casa en casa) Hora (9:00 am). \
                    \n \n *Domingo:*\
                    \n 🏠 *Por definir* | \
                    \n Faceta (casa en casa) Hora (9:00 am).',
                from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
                to=from_number  # Número del usuario (formato WhatsApp)
            )
            user_state[from_number]['state'] = 'inicio'


    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)