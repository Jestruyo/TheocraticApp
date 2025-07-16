import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Scopes path de google
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SPREADSHEET = os.getenv('GOOGLE_SPREADSHEET')
CREDENTIALS_FILE = "credentials_googlesheets.json"