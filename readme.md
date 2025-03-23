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

## Licencia 📜
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
¡Gracias por usar este proyecto! Si tienes alguna pregunta, no dudes en abrir un issue o contactarme. 🚀
Este README.md proporciona una guía completa para configurar, ejecutar y probar tu proyecto. Puedes personalizarlo según tus necesidades. ¡Buena suerte! 😊

     
