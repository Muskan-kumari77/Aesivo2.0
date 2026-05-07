from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import get_db
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)


# =========================
# JWT PROTECT DECORATOR
# =========================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

            request.user_id = data["user_id"]
            request.role = data["role"]

        except Exception as e:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


# =========================
# ADMIN PROTECTION
# =========================
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if request.role != "admin":
            return jsonify({"error": "Admin only"}), 403

        return f(*args, **kwargs)

    return decorated


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = get_db()

    hashed_password = generate_password_hash(data["password"])

    try:
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (data["name"], data["email"], hashed_password, "user")
        )
        conn.commit()
    except:
        return jsonify({"error": "User already exists"}), 400

    return jsonify({"message": "Registered successfully"}), 201


# =========================
# LOGIN (JWT)
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (data["email"],)
    ).fetchone()

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })


# =========================
# GET PROFILE
# =========================
@auth_bp.route("/me", methods=["GET"])
@token_required
def get_profile():
    conn = get_db()

    user = conn.execute(
        "SELECT id, name, email, role FROM users WHERE id=?",
        (request.user_id,)
    ).fetchone()

    return jsonify(dict(user))


# =========================
# UPDATE PROFILE
# =========================
@auth_bp.route("/update", methods=["PUT"])
@token_required
def update_profile():
    data = request.json
    conn = get_db()

    conn.execute(
        "UPDATE users SET name=?, email=? WHERE id=?",
        (data["name"], data["email"], request.user_id)
    )
    conn.commit()

    return jsonify({"message": "Profile updated"})


# =========================
# CHANGE PASSWORD
# =========================
@auth_bp.route("/password", methods=["PUT"])
@token_required
def change_password():
    data = request.json
    conn = get_db()

    hashed_password = generate_password_hash(data["password"])

    conn.execute(
        "UPDATE users SET password=? WHERE id=?",
        (hashed_password, request.user_id)
    )
    conn.commit()

    return jsonify({"message": "Password updated"})


# =========================
# ADMIN ONLY TEST ROUTE
# =========================
@auth_bp.route("/admin-test", methods=["GET"])
@token_required
@admin_required
def admin_test():
    return jsonify({"message": "Welcome Admin!"})