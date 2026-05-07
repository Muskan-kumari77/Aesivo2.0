from flask import Blueprint, jsonify, request
from db import get_db

# IMPORT SECURITY DECORATORS
from routes.auth_routes import token_required, admin_required

admin_bp = Blueprint("admin", __name__)


# =========================
# GET CONTACTS (ADMIN ONLY)
# =========================
@admin_bp.route("/contacts", methods=["GET"])
@token_required
@admin_required
def get_contacts():
    conn = get_db()

    data = conn.execute(
        "SELECT * FROM contact ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(x) for x in data])


# =========================
# GET ORDERS
# =========================
@admin_bp.route("/orders", methods=["GET"])
@token_required
@admin_required
def get_orders():
    conn = get_db()

    data = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(x) for x in data])


# =========================
# BASIC STATS
# =========================
@admin_bp.route("/stats", methods=["GET"])
@token_required
@admin_required
def stats():
    conn = get_db()

    users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    contacts = conn.execute("SELECT COUNT(*) FROM contact").fetchone()[0]

    conn.close()

    return jsonify({
        "users": users,
        "orders": orders,
        "contacts": contacts
    })


# =========================
# UPDATE ORDER STATUS
# =========================
@admin_bp.route("/orders/update/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_order(id):
    data = request.get_json()
    status = data.get("status")

    conn = get_db()

    conn.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Order updated"})


# =========================
# DELETE CONTACT
# =========================
@admin_bp.route("/contacts/delete/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_contact(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM contact WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Contact deleted"})


# =========================
# SALES DATA
# =========================
@admin_bp.route("/sales", methods=["GET"])
@token_required
@admin_required
def sales_data():
    conn = get_db()

    data = conn.execute("""
        SELECT DATE(created_at) as date, SUM(total_price) as total
        FROM orders
        GROUP BY DATE(created_at)
        ORDER BY date
    """).fetchall()

    conn.close()

    return jsonify([dict(x) for x in data])