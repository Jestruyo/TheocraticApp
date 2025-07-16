from flask import Flask
from twilio.rest import Client
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from .config import SCOPES, CREDENTIALS_FILE, SPREADSHEET
from .utils import ACCOUNT_SID, AUTH_TOKEN

app = Flask(__name__)
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

def get_gspread_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    client = gspread.authorize(creds)
    spreadsheet = client.open(SPREADSHEET)
    return spreadsheet.sheet1
