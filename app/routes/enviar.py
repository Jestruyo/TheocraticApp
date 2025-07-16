from flask import Blueprint, request, jsonify
from ..extensions import get_gspread_sheet

enviar_bp = Blueprint('enviar', __name__)

@enviar_bp.route('/enviar', methods=['POST'])
def enviar_datos():
    sheet = get_gspread_sheet()
    data = request.get_json()

    if not all(k in data for k in ("nombre", "email", "mensaje")):
        return jsonify({"error": "Faltan campos"}), 400

    sheet.append_row([data['nombre'], data['email'], data['mensaje']])
    return jsonify({"mensaje": "Datos agregados correctamente"}), 201
