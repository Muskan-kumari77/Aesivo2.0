from flask import Blueprint, jsonify, session
from db import get_db

order_bp = Blueprint("orders", __name__)

@order_bp.route("/my-orders", methods=["GET"])
def my_orders():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()

    orders = conn.execute(
        "SELECT * FROM orders WHERE user_id=? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()

    return jsonify([dict(o) for o in orders])
from routes.auth_routes import token_required

@order_bp.route("/", methods=["POST"])
@token_required
def place():
    return place_order()

@order_bp.route("/", methods=["GET"])
@token_required
def get():
    return get_orders()