from flask import Blueprint, request, jsonify
from ..extensions import twilio_client
from ..state import user_state
from ..utils import validate_user_number, TWILIO_PHONE
import time

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    from_number = request.form.get('From')
    message_body = request.form.get('Body', '').strip().lower()
    user_data = validate_user_number(from_number)

    if not user_data:
        twilio_client.messages.create(
            body='❌ 😔 *Lo siento, no estás registrado para usar este servicio.*\
                \n\nSi deseas registrarte, por favor contacta a tu super de grupo.\
                \n\nMientras tanto, quiero compartirte los horarios de reunión de la congregacion cordialidad:\
                \n\n🖥️ *1. Reunión entre semana | Jueves 7 pm*\
                \n📌 https://jworg.zoom.us/j/99106008401\
                \n*Código de acceso:* 1234.\
                \n\n🖥️ *2. Reunión fin de semana | Domingo 5 pm*\
                \n📌 https://jworg.zoom.us/j/91928746645\
                \n*Código de acceso:* 1234.\
                \n\n📍 *3. Dirección:* Cl. 76 # 7B - 45, El Bosque, Barranquilla.\
                \n📌 https://maps.app.goo.gl/gteL23tYX32KUeb79\
                \n\n🌐 *4. Sitio oficial:*\
                \n📌 https://www.jw.org/es/',
            from_=TWILIO_PHONE,
            to=from_number
        )
        return jsonify({'status': 'error'}), 400

    # Reinicio con "menú"
    if message_body in ['menu', 'menú']:
        user_state[from_number] = {
            'state': 'inicio',
            'last_activity': time.time(),
            'inactivity_notified': False,
            'nombre': user_data['name']
        }

    if from_number in user_state:
        time_inactive = time.time() - user_state[from_number].get('last_activity', 0)
        if time_inactive > 180:
            user_state[from_number] = {
                'state': 'inicio',
                'last_activity': time.time(),
                'inactivity_notified': False,
                'nombre': user_data['name']
            }
    else:
        if message_body not in ['menu', 'menú']:
            twilio_client.messages.create(
                body=f'Hola {user_data["name"]} 😊 👋, por favor escribe *"menú"* para comenzar.',
                from_=TWILIO_PHONE,
                to=from_number
            )
            return jsonify({'status': 'success'}), 200
        else:
            user_state[from_number] = {
                'state': 'inicio',
                'last_activity': time.time(),
                'inactivity_notified': False,
                'nombre': user_data['name']
            }

    user_state[from_number]['last_activity'] = time.time()
    user_state[from_number]['inactivity_notified'] = False

    current_state = user_state[from_number]['state']

    if current_state == 'inicio':
        twilio_client.messages.create(
            body=f'*¡Ahora sí, mi querid@ herman@ {user_data["name"]}. 😊 ¿Cómo puedo ayudarte?*\n\n'
                 '<<Escribe el # número de tu opción requerida>>:\n\n'
                 '🕒 *1. Horas de reuniones.*\n'
                 '🏠 *2. Lugares de Predicación.*\n'
                 '📝 *3. Envío de informes.*\n'
                 '📋 *4. Solicitudes.*\n'
                 '👌 *5. Siervos ministeriales.*\n'
                 '🫶 *6. Ancianos.*\n'
                 '🚨 *7. Líneas de emergencia.*\n',
            from_=TWILIO_PHONE,
            to=from_number
        )
        user_state[from_number]['state'] = 'validar_solicitud'

    elif current_state == 'validar_solicitud':
        if message_body in ['menu', 'menú']:
            user_state[from_number]['state'] = 'inicio'
            return jsonify({'status': 'success'}), 200

        if message_body == '1':
            twilio_client.messages.create(
                body='*Estos son los enlaces a la plataforma Zoom:*\
                      \n\n🖥️ *1. Reunión entre semana | Jueves 7 pm*\
                      \n📌 https://jworg.zoom.us/j/99106008401\
                      \n*Código de acceso:* 1234.\
                      \n\n🖥️ *2. Reunión fin de semana | Domingo 5 pm*\
                      \n📌 https://jworg.zoom.us/j/91928746645\
                      \n*Código de acceso:* 1234.\
                      \n\n📍 *3. Dirección:* Cl. 76 # 7B - 45, El Bosque, Barranquilla.\
                      \n📌 https://maps.app.goo.gl/gteL23tYX32KUeb79\
                      \n\n🌐 *Sitio oficial:* https://www.jw.org/es/\
                      \n\n📢 *Recuerda:* Puedes volver a escribir *"menú"* para regresar.',
                from_=TWILIO_PHONE,
                to=from_number
            )

        elif message_body == '2':
            twilio_client.messages.create(
                body='📌 *Aquí tienes los lugares de predicación para la semana:*\
                      \n\n*Lunes:* 🏫 Salón del Reino – 6:50pm (pública)\
                      \n*Martes:* 🏠 Esther Rua – 9:00am (cartas) | 🏠 Rosalba Serge – 4:30pm (casa en casa)\
                      \n*Miercoles:* 🏠 Maria Herrera – 9:00am | 🏠 Vanessa Villa – 4:30pm\
                      \n*Jueves:* ❌ No hay predicación (día de reunión)\
                      \n*Viernes:* 🏫 Salón del Reino – 9:00am (cartas/llamadas) | 4:30pm (por definir)\
                      \n*Sábado:* 🏠 Vanessa Villa – 9:00am\
                      \n*Domingo:* 🏠 Por definir – 9:00am\
                      \n\n📢 *Recuerda:* Escribe *"menú"* cuando quieras regresar al inicio.',
                from_=TWILIO_PHONE,
                to=from_number
            )

        elif message_body == '3':
            user_state[from_number]['state'] = 'enviando_informe_fecha'
            user_state[from_number]['reporte_actual'] = {
                'usuario': {
                    'nombre': user_data['name'],
                    'numero': from_number,
                },
                'datos': {}
            }
            twilio_client.messages.create(
                body='🗓️ Por favor, ingresa la *fecha* del informe en formato *AAAA-MM-DD*:',
                from_=TWILIO_PHONE,
                to=from_number
            )

    return jsonify({'status': 'success'}), 200
