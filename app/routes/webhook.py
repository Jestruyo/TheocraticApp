from flask import Blueprint, request, jsonify
from ..extensions import twilio_client
from ..state import user_state, output_mesage
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
            body=output_mesage["not_registered_message"],
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
                body=output_mesage["welcome_message"].format(name=user_data['name']),
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
            body=output_mesage["start_message"].format(name=user_data['name']),
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
                body=output_mesage["option_1"],
                from_=TWILIO_PHONE,
                to=from_number
            )

        elif message_body == '2':
            twilio_client.messages.create(
                body=output_mesage["option_2"],
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
            print("test: ",user_state)
            twilio_client.messages.create(
                body=output_mesage["option_3"],
                from_=TWILIO_PHONE,
                to=from_number
            )

    return jsonify({'status': 'success'}), 200
