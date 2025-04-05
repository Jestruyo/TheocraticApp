from flask import Flask, request, jsonify
from twilio.rest import Client
import time
from threading import Thread
import atexit
from utils import ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE, validate_user_number

app = Flask(__name__)

# Cliente de Twilio
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Almacenar el estado del usuario
user_state = {}

def cleanup():
    """Limpieza al cerrar la aplicación"""
    print("Cerrando hilos de monitoreo...")

def check_inactive_sessions():
    """Función que revisa periódicamente sesiones inactivas"""
    while True:
        current_time = time.time()
        users_copy = list(user_state.items())
        
        for number, data in users_copy:
            last_activity = data.get('last_activity', 0)
            time_inactive = current_time - last_activity
            
            # Debug: Mostrar tiempos de inactividad
            print(f"Usuario {number} - Inactivo por {time_inactive:.2f} segundos")
            
            if time_inactive > 180 and not data.get('inactivity_notified', False):
                try:
                    # Enviar mensaje de inactividad
                    client.messages.create(
                        body="⏳ Hemos notado que no has interactuado en los últimos 5 minutos. "
                             "Por favor, si aún necesitas ayuda, inicia una nueva conversación. "
                             "¡Estaremos encantados de atenderte! 😊",
                        from_=TWILIO_PHONE,
                        to=number
                    )
                    print(f"Mensaje de inactividad enviado a {number}")
                    
                    # Marcar como notificado
                    user_state[number]['inactivity_notified'] = True
                    
                except Exception as e:
                    print(f"Error enviando mensaje a {number}: {str(e)}")
        
        time.sleep(30)  # Revisar cada 30 segundos

# Configurar limpieza al cerrar
atexit.register(cleanup)

# Iniciar hilo para monitorear inactividad
monitor_thread = Thread(target=check_inactive_sessions, daemon=True)
monitor_thread.start()

@app.route('/webhook', methods=['POST'])
def webhook():
    from_number = request.form.get('From')
    message_body = request.form.get('Body')

    # Verificar si el usuario está registrado
    user_data = validate_user_number(from_number)
    if not user_data:
        client.messages.create(
            body='❌ 😔 *Lo siento, no estás registrado para usar este servicio*\
                \n \n *Si deseas registrarte, por favor contacta a tu super de grupo.*',
            from_=TWILIO_PHONE,
            to=from_number
        )
        return jsonify({'status': 'error'}), 400

    # Reiniciar estado si ha pasado más de 5 minutos
    if from_number in user_state:
        time_inactive = time.time() - user_state[from_number].get('last_activity', 0)
        if time_inactive > 180:  # 300 segundos = 5 minutos
            user_state[from_number] = {
                'state': 'inicio',
                'last_activity': time.time(),
                'inactivity_notified': False,
                'nombre': user_data['name']
            }
    else:
        # Nuevo usuario
        user_state[from_number] = {
            'state': 'inicio',
            'last_activity': time.time(),
            'inactivity_notified': False,
            'nombre': user_data['name']
        }

    # Actualizar última actividad (para casos donde no se reinició el estado)
    user_state[from_number]['last_activity'] = time.time()
    user_state[from_number]['inactivity_notified'] = False

    # Manejar el flujo basado en el estado actual
    current_state = user_state[from_number]['state']
    
    if current_state == 'inicio':
        # Enviar mensaje de bienvenida
        client.messages.create(
            body=f'*¡Hola! Que gusto saludarte {user_data["name"]} 😊 ¿Como puedo ayudarte?*\n\n'
                 'Ingresa el número de tu opción requerida:\n\n'
                 '🕒 *1. Hora de reuniones.*\n'
                 '🏠 *2. Lugares de Predicación.*\n'
                 '📝 *3. Envio de informes.*\n'
                 '📋 *4. Solicitudes y formularios.*\n'
                 '🚨 *5. Lineas de emergencia.*',
            from_=TWILIO_PHONE,
            to=from_number
        )
        user_state[from_number]['state'] = 'validar_solicitud'

    elif current_state == 'validar_solicitud':
        if message_body == '1':
            client.messages.create(
                body=f'*Estos son los enlaces a la plataforma zoom:*\
                    \n \n 🖥️ *1. Reunión entre semana | Jueves 7 pm*\
                    \n 📌 https://jworg.zoom.us/j/99106008401\
                    \n *Codigo de acceso:* 1234.\
                    \n \n 🖥️ *2. Reunión fin de semana | Domingo 5 pm*\
                    \n 📌 https://jworg.zoom.us/j/91928746645\
                    \n *Codigo de acceso:* 1234.\
                    \n \n *¿Hay algo mas en lo que pueda ayudarte {user_data["name"]}?*\
                    \n \n 📝 Si lo deseas puedes volver a ingresar el número de tu opción requerida:\
                    \n \n 🏠 *2. Lugares de Predicación.*\
                    \n 📝 *3. Envio de informes.*\
                    \n 📋 *4. Solicitudes y formularios.*\
                    \n 🚨 *5. Lineas de emergencia.*',
                from_=TWILIO_PHONE,
                to=from_number
            )
        elif message_body == '2':
            client.messages.create(
                body=f'📌 *A continuación te comparto los lugares de salida al servicio del campo:*\
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
                    \n Faceta (casa en casa) Hora (9:00 am).\
                    \n \n ⚠️ Si lo deseas {user_data["name"]}, *puedes volver a ingresar el número de tu opción requerida*.',
                from_=TWILIO_PHONE,  # Número de Twilio (formato WhatsApp)
                to=from_number  # Número del usuario (formato WhatsApp)
            )

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)