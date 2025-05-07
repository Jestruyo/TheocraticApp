## Theocratic App - Backend para WhatsApp 📱

Este proyecto es un backend en Python que utiliza Flask y Twilio para manejar mensajes de WhatsApp basados en un flujo de conversación. El backend recibe mensajes de WhatsApp a través de un webhook, procesa el flujo de conversación y envía respuestas automáticas.

## Requisitos previos 📋 

Antes de comenzar, asegúrate de tener instalado lo siguiente:

-- Python 3.9 o superior: Descargar Python. 🐍
-- Docker 🐳 
-- Cuenta en Twilio: Regístrate en Twilio. 📦
-- (Opcional) Ngrok: Para exponer tu servidor local a Internet. Descargar Ngrok o usa un contenedor Docker como esta este proyecto. 🌐

## Configuración del proyecto ⚙️

* 1) # Clona
     - git clone git@github.com:Jestruyo/TheocraticApp.git
     - cd theocratic-app

* 2) # Configurar Twilio
     - Obtén tus credenciales de Twilio:
     - Ve al panel de Twilio.
     - Copia tu ACCOUNT_SID y AUTH_TOKEN.

     Configura el Sandbox de WhatsApp:
     - En el panel de Twilio, ve a la sección de WhatsApp Sandbox.
     - Conecta tu número de WhatsApp al Sandbox enviando un mensaje con el código join <sandbox name> al número de Twilio Sandbox (+1 415 523 8886).

     Configura el webhook:
     - En la sección de Sandbox Configuration, configura el webhook para que apunte a tu endpoint /webhook (por ejemplo, https://abc123.ngrok.io/webhook).

* 3) # Configurar las variables de entorno 🔧
     - En .env de la raíz del proyecto, agrega tus credenciales de Twilio:
        * ACCOUNT_SID=your_account_sid
        * AUTH_TOKEN=your_auth_token
        * TWILIO_PHONE=whatsapp:+14155238886
        * Recuerda agregar las configuraciones de los usuarios que usaran el bot:
           Ejemplo:
                    USER_ADMIN_NAME = "Jesus Trujillo" # Nombre del administrador.
                    USER_ADMIN_NUMBER = "whatsapp:+573003758315"  # Número de WhatsApp del administrador.
                    USER_ADMIN_PASSWORD = "jesus123"  # Contraseña del administrador.

* 4) # Construir y ejecutar el contenedor Docker 🛠️ 
     - Construir la imagen de Docker: docker compose build
     - Ejecutar los contenedores: docker compose up

     Esto levantará dos servicios:
     - web: El backend Flask en el puerto 5000. 🌐
     - ngrok: Expone el backend a Internet a través de ngrok. 🚀 

     Obtener la URL de ngrok: 🚀
     - Accede a la interfaz web de ngrok en http://localhost:4040, o el puerto configurado en tu contenedor.
     - Copia la URL generada (por ejemplo, https://abc123.ngrok.io).

     Configurar el webhook en Twilio: 🔧
     Entra en twilio, en Messaging > try it out > Send a Whatsapp message > Sandbox setting
     - Actualiza el webhook en Twilio para que apunte a la URL de ngrok (por ejemplo, https://abc123.ngrok.io/webhook).

* 5) # Probar el flujo de WhatsApp 🚀
     Envía un mensaje al Sandbox:
     - Envía un mensaje de WhatsApp al número de Twilio Sandbox (Ejemplo +1 415 523 8886), El mensaje puede ser algo simple como Hola.

     Respuesta automática:
     - El backend responderá con: ¡Hola! Bienvenido. ¿Cuál es tu nombre?.


-------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 📄 Integración con Google Sheets usando Flask y gspread

Esta API permite recibir datos vía POST y guardarlos directamente en una hoja de cálculo de Google Sheets.

# 🧰 Requisitos
     - Python 3.7+
     - Cuenta de Google
     - Proyecto en Google Cloud Platform
     - Habilitación de Google Sheets API y Google Drive API
     - Librerías: Flask, gspread, oauth2client

## 🛠️ Configuración paso a paso

* 1) # Crear un proyecto en Google Cloud
     - Ir a Google Cloud Console.
     - Crear un nuevo proyecto o usar uno existente.
     - Anota el Project ID para futuras referencias.

* 2) # Habilitar APIs necesarias
     - Habilita las siguientes APIs para tu proyecto:
     - Google Sheets API
     - Google Drive API

* 3) # Crear una cuenta de servicio
     En el panel izquierdo de GCP, ve a "IAM y administración" → "Cuentas de servicio".
     Haz clic en "Crear cuenta de servicio".
     Asigna un nombre y continúa.
     Da el rol Editor o Editor de hojas de cálculo.
     Finaliza y guarda.

     En la lista de cuentas, haz clic en la cuenta recién creada y selecciona "Agregar clave" → "Crear nueva clave".
     Selecciona JSON y descarga el archivo credenciales.json.
     Mueve este archivo a tu directorio del proyecto Flask (no lo subas a Git).

* 4) # Compartir tu hoja de cálculo con la cuenta de servicio
     - Crea una hoja de cálculo vacía en Google Sheets.
     - Copia el nombre exacto (por ejemplo: datos_api).
     - Comparte el documento con el email que aparece en el campo "client_email" del archivo credenciales.json. El nombre del archivo puede ser diferente.

## Licencia 📜
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
¡Gracias por usar este proyecto! Si tienes alguna pregunta, no dudes en abrir un issue o contactarme. 🚀
Este README.md proporciona una guía completa para configurar, ejecutar y probar tu proyecto. Puedes personalizarlo según tus necesidades. ¡Buena suerte! 😊

     
