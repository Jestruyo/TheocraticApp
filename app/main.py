# Importación de bibliotecas necesarias
from flask import Flask, request, jsonify  # Flask para el servidor web
from twilio.rest import Client  # Cliente de Twilio para WhatsApp
import time  # Para manejar tiempos de inactividad
from threading import Thread  # Para ejecutar tareas en segundo plano
import atexit  # Para manejar el cierre de la aplicación
from utils import ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE, validate_user_number  # Credenciales y funciones auxiliares

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración del cliente de Twilio con las credenciales
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Diccionario para almacenar el estado de cada usuario
# Estructura: {número: {state: str, last_activity: float, inactivity_notified: bool, nombre: str}}
user_state = {}

def cleanup():
    """
    Función de limpieza que se ejecuta al cerrar la aplicación.
    Imprime un mensaje para indicar que se están cerrando los hilos.
    """
    print("Cerrando hilos de monitoreo...")

def check_inactive_sessions():
    """
    Función que se ejecuta en segundo plano para monitorear sesiones inactivas.
    Revisa cada 30 segundos si algún usuario lleva más de 3 minutos sin interactuar.
    """
    while True:
        current_time = time.time()  # Obtiene el tiempo actual
        users_copy = list(user_state.items())  # Copia segura para iterar
        
        for number, data in users_copy:
            last_activity = data.get('last_activity', 0)
            time_inactive = current_time - last_activity  # Calcula tiempo inactivo
            
            # Debug: Muestra tiempos de inactividad
            print(f"Usuario {number} - Inactivo por {time_inactive:.2f} segundos")
            
            # Si lleva más de 3 minutos inactivo y no se ha notificado
            if time_inactive > 180 and not data.get('inactivity_notified', False):
                try:
                    # Envía mensaje de inactividad
                    client.messages.create(
                        body='⏳ He notado que no has interactuado en los últimos *3* minutos.\
                             \n \nPor favor, si aún necesitas ayuda, inicia una nueva conversación.\
                             \n \n*¡Estare encantado de atenderte!* 😊',
                        from_=TWILIO_PHONE,
                        to=number
                    )
                    print(f"Mensaje de inactividad enviado a {number}")
                    
                    # Marca como notificado para no enviar múltiples mensajes
                    user_state[number]['inactivity_notified'] = True
                    
                except Exception as e:
                    print(f"Error enviando mensaje a {number}: {str(e)}")
        
        time.sleep(30)  # Espera 30 segundos entre verificaciones

# Configura la función de limpieza al cerrar la aplicación
atexit.register(cleanup)

# Inicia el hilo para monitorear inactividad
# daemon=True permite que el hilo se cierre cuando termine el programa principal
monitor_thread = Thread(target=check_inactive_sessions, daemon=True)
monitor_thread.start()

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint principal que recibe los mensajes de WhatsApp.
    Procesa las interacciones con los usuarios y gestiona el flujo de conversación.
    """
    # Obtiene el número del remitente y el cuerpo del mensaje
    from_number = request.form.get('From')
    message_body = request.form.get('Body').strip().lower() # Convertimos a minúsculas y quitamos espacios

    # Verifica si el usuario está registrado
    user_data = validate_user_number(from_number)
    if not user_data:
        # Si no está registrado, envía mensaje con información básica
        client.messages.create(
            body='❌ 😔 *Lo siento, no estás registrado para usar este servicio.*\
                \nSi deseas registrarte, por favor contacta a tu super de grupo.\
                \n \nMientras tanto, quiero compartirte los horarios de reunión de la congregacion cordialidad:\
                \n \n 🖥️ *1. Reunión entre semana | Jueves 7 pm*\
                \n 📌 https://jworg.zoom.us/j/99106008401\
                \n *Codigo de acceso:* 1234.\
                \n \n 🖥️ *2. Reunión fin de semana | Domingo 5 pm*\
                \n 📌 https://jworg.zoom.us/j/91928746645\
                \n *Codigo de acceso:* 1234.\
                \n \n 📍 *3. Direccion:* Cl. 76 # 7B - 45, El Bosque, Barranquilla, Atlántico.\
                \n 📌 https://maps.app.goo.gl/gteL23tYX32KUeb79\
                \n \n 🌐 *4. Sitio oficial:*\
                \n 📌 https://www.jw.org/es/',
            from_=TWILIO_PHONE,
            to=from_number
        )
        return jsonify({'status': 'error'}), 400

    # Verificar si el usuario escribió "menu" o "menú" para reiniciar el flujo
    if message_body in ['menu', 'menú']:
        user_state[from_number] = {
            'state': 'inicio',
            'last_activity': time.time(),
            'inactivity_notified': False,
            'nombre': user_data['name']
        }
        # Continuará con el flujo normal mostrando el menú

    # Gestiona el estado del usuario
    if from_number in user_state:
        # Calcula tiempo de inactividad
        time_inactive = time.time() - user_state[from_number].get('last_activity', 0)
        if time_inactive > 180:  # 3 minutos de inactividad
            # Reinicia el estado si lleva mucho tiempo inactivo
            user_state[from_number] = {
                'state': 'inicio',
                'last_activity': time.time(),
                'inactivity_notified': False,
                'nombre': user_data['name']
            }
    else:
        # Nuevo usuario - inicializa su estado
        # SOLO si es el primer mensaje y no es "menu" o "menú"
        if message_body not in ['menu', 'menú', 'Menu', 'Menú']:
            client.messages.create(
                body=f'Hola {user_data["name"]} 😊 👋, por favor escribe *"menu"* , *"menú"* o *"Menú"* para comenzar.',
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

    # Actualiza la última actividad (para casos donde no se alcanzo a reinició el estado, porque escribio de nuevo)
    user_state[from_number]['last_activity'] = time.time()
    user_state[from_number]['inactivity_notified'] = False

    # Obtiene el estado actual del usuario
    current_state = user_state[from_number]['state']
    
    # Lógica principal del flujo de conversación
    if current_state == 'inicio':
        # Envía mensaje de bienvenida con el menú principal
        client.messages.create(
            body=f'*¡Hola! Que gusto saludarte de nuevo {user_data["name"]} 😊 ¿Como puedo ayudarte?*\n\n'
                 'Ingresa el número de tu opción requerida:\n\n'
                 '🕒 *1. Hora de reuniones.*\n'
                 '🏠 *2. Lugares de Predicación.*\n'
                 '📝 *3. Envio de informes.*\n'
                 '📋 *4. Solicitudes y formularios.*\n'
                 '🚨 *5. Lineas de emergencia.*',
            from_=TWILIO_PHONE,
            to=from_number
        )
        # Cambia al estado de validar solicitud
        user_state[from_number]['state'] = 'validar_solicitud'

    elif current_state == 'validar_solicitud':
        # Verificar nuevamente si escribió "menu" o "menú"
        if message_body in ['menu', 'menú']:
            user_state[from_number]['state'] = 'inicio'
            # Volverá al inicio en la siguiente iteración
            return jsonify({'status': 'success'}), 200
        
        # Procesa la opción seleccionada por el usuario
        if message_body == '1':
            # Opción 1: Horario de reuniones
            client.messages.create(
                body=f'*Estos son los enlaces a la plataforma zoom:*\
                    \n \n 🖥️ *1. Reunión entre semana | Jueves 7 pm*\
                    \n 📌 https://jworg.zoom.us/j/99106008401\
                    \n *Codigo de acceso:* 1234.\
                    \n \n 🖥️ *2. Reunión fin de semana | Domingo 5 pm*\
                    \n 📌 https://jworg.zoom.us/j/91928746645\
                    \n *Codigo de acceso:* 1234.\
                    \n \n 📍 *3. Direccion:* Cl. 76 # 7B - 45, El Bosque, Barranquilla, Atlántico.\
                    \n 📌 https://maps.app.goo.gl/gteL23tYX32KUeb79\
                    \n \n 🌐 *4. Sitio oficial:*\
                    \n 📌 https://www.jw.org/es/\
                    \n \n 📢 *Recuerda:* Puedes volver a ingresar, si lo deseas, la palabra *"menu"* , *"menú"* o *"Menú"*, para regresar al menú principal.',
                from_=TWILIO_PHONE,
                to=from_number
            )
            # Cambia al estado de validar solicitud
            user_state[from_number]['state'] = 'validar_solicitud'

        elif message_body == '2':
            # Opción 2: Lugares de predicación
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
                    \n \n 📢 *Recuerda:* Puedes volver a ingresar, si lo deseas, la palabra *"menu"* , *"menú"* o *"Menú"*, para regresar al menú principal.',
                from_=TWILIO_PHONE,
                to=from_number
            )
        # (Aquí irían las opciones 3, 4 y 5 cuando se implementen)

    # Retorna respuesta exitosa
    return jsonify({'status': 'success'}), 200

# Punto de entrada principal
if __name__ == '__main__':
    # Inicia el servidor Flask en todas las interfaces (0.0.0.0) en el puerto 5000
    # debug=True proporciona mensajes de error detallados (solo para desarrollo)
    app.run(host='0.0.0.0', port=5000, debug=True)