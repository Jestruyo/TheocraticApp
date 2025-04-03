# @file: utils.py.
# @description: Este archivo carga las credenciales de Twilio y la configuración de usuarios desde el environment.

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Credenciales de Twilio
ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')  # Número de Twilio Sandbox

# Configuración de usuarios
USERS = {
    'admin': {
        'name': os.getenv('USER_ADMIN_NAME'),  # Nombre del administrador
        'number': os.getenv('USER_ADMIN_NUMBER'),  # Número del administrador (formato WhatsApp)
        'password': os.getenv('USER_ADMIN_PASSWORD')  # Contraseña del administrador
    },
    'yurleydis': {
        'name': os.getenv('USER_YURLEYDIS_NAME'), 
        'number': os.getenv('USER_YURLEYDIS_NUMBER'),  
        'password': os.getenv('USER_YURLEYDIS_PASSWORD')  
    },
    'etilvia': {
        'name': os.getenv('USER_ETILVIA_NAME'), 
        'number': os.getenv('USER_ETILVIA_NUMBER'),  
        'password': os.getenv('USER_ETILVIA_PASSWORD') 
    }
}

def validate_user_number(number):
    """
    Valida si un número está registrado en los usuarios.
    
    Args:
        number (str): Número de teléfono a validar (en formato WhatsApp)
    
    Returns:
        dict or None: Diccionario con los datos del usuario si existe, None si no
    """
    for username, user_data in USERS.items():
        if user_data.get('number') == number:
            return {
                'username': username,
                'name': user_data['name'],
                'number': user_data['number'],
                'password': user_data['password']
            }
    return None