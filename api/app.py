from flask import Flask, request, jsonify
from flask_cors import CORS
from validators import validate_phone_rules
from db import execute
import os
from functools import lru_cache

app = Flask(__name__)
CORS(app)

@app.route('/api/phone/validate', methods=['POST'])
def phone_validate():
    data = request.get_json(force=True, silent=True) or {}
    number = data.get('number', '')
    rules = validate_phone_rules(number)
    
    if not rules["format_ok"]:
        return jsonify({"error": "Format must be 6 digits"}), 400
    
    return jsonify({
        "number": number,
        "rules": rules,
        "isValid": rules["is_valid"]
    })

@app.route('/api/registration', methods=['POST'])
def register():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get('name', '')
    email = data.get('email', '')
    phone = data.get('phone', '')

    rules = validate_phone_rules(phone)

    # Format minimum 6 hane kontrolü
    if not rules["format_ok"]:
        return jsonify({
            "status": "denied",
            "message": "Format hatası",
            "isValid": False
        }), 400

    # Geçerli numara kontrolü
    if not rules["is_valid"]:
        return jsonify({
            "status": "denied",
            "message": "Geçersiz telefon numarası",
            "isValid": False
        }), 422

    try:
        query = "INSERT INTO registrations (name, email, phone) VALUES (%s, %s, %s)"
        execute(query, (name, email, phone))

        return jsonify({
            "status": "accepted",
            "message": "Kayıt oluşturuldu.",
            "data": {
                "name": name,
                "email": email,
                "phone": phone
            }
        }), 201

    except Exception as e:
        msg = str(e)
        if "Duplicate" in msg or "ER_DUP_ENTRY" in msg:
            return jsonify({"status": "denied", "message": "Numara zaten kayıtlı."}), 409

        return jsonify({"status": "error", "message": "Server error", "detail": msg}), 500


@app.route('/api/phone/count', methods=['GET'])
def phone_count():
    cnt = _count_valid_phones()
    return jsonify({"count": cnt})


@lru_cache(maxsize=1)
def _count_valid_phones():
    def ok(num):
        return validate_phone_rules(num)["is_valid"]
    count = 0
    for n in range(1000000):
        if ok(str(n).zfill(6)):
            count += 1
    return count


@app.route('/api/registrations', methods=['GET'])
def registrations():
    rows = execute("SELECT * FROM registrations ORDER BY created_at DESC", fetch=True)
    return jsonify({"rows": rows})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

