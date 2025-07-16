# Usar una imagen base de Python con Alpine Linux
FROM python:3.9-alpine

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias (si las hay)
# Por ejemplo, si usas bibliotecas que requieren compilación, necesitarás build-base
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copiar los archivos de requisitos
COPY . .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5000
EXPOSE 5000

ENV PYTHONPATH=/app

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]