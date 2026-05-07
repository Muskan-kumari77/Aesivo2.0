from flask import request, jsonify
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash


# ✅ Signup
def register():
    data = request.json

    name = data["name"]
    email = data["email"]
    password = generate_password_hash(data["password"])

    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password))

        conn.commit()
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        conn.close()

    return jsonify({"message": "User registered successfully"}), 201


# ✅ Login
def login():
    data = request.json

    email = data["email"]
    password = data["password"]

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        })

    return jsonify({"error": "Invalid email or password"}), 401