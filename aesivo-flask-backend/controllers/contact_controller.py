from flask import request, jsonify
from db import get_db

def save_contact():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")
        category = data.get("category", "general")

        if not name or not email or not message:
            return jsonify({"error": "All fields required"}), 400

        conn = get_db()

        conn.execute(
            "INSERT INTO contact (name, email, message, category) VALUES (?, ?, ?, ?)",
            (name, email, message, category)
        )

        conn.commit()
        conn.close()

        return jsonify({"message": "Message saved successfully"}), 200

    except Exception as e:
        print("CONTACT ERROR:", e)
        return jsonify({"error": "Server error"}), 500