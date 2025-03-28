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
USER_ADMIN = {
    'name': os.getenv('USER_ADMIN_NAME'), # Nombre del administrador
    'number': os.getenv('USER_ADMIN_NUMBER'),  # Número del administrador (formato WhatsApp)
    'password': os.getenv('USER_ADMIN_PASSWORD')  # Contraseña del administrador
}