from flask import request, jsonify
from db import get_db

# =========================
# PLACE ORDER
# =========================
def place_order():
    conn = get_db()

    user_id = request.user_id  # ✅ JWT

    data = request.json
    payment_method = data.get("payment_method", "COD")
    total_price = data.get("total_price", 0)

    # GET CART ITEMS
    cart_items = conn.execute("""
        SELECT cart.product_id, cart.quantity, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id=?
    """, (user_id,)).fetchall()

    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    # CREATE ORDER
    cursor = conn.execute("""
        INSERT INTO orders (user_id, total_price, status, payment_method)
        VALUES (?, ?, ?, ?)
    """, (user_id, total_price, "Placed", payment_method))

    order_id = cursor.lastrowid

    # INSERT ITEMS
    for item in cart_items:
        conn.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            item["product_id"],
            item["quantity"],
            item["price"]
        ))

    # CLEAR CART
    conn.execute("DELETE FROM cart WHERE user_id=?", (user_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Order placed",
        "order_id": order_id
    })


# =========================
# GET ORDERS
# =========================
def get_orders():
    conn = get_db()

    user_id = request.user_id  # ✅ JWT

    orders = conn.execute("""
        SELECT * FROM orders WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()

    result = []

    for order in orders:
        items = conn.execute("""
            SELECT products.name, order_items.quantity, order_items.price
            FROM order_items
            JOIN products ON order_items.product_id = products.id
            WHERE order_items.order_id=?
        """, (order["id"],)).fetchall()

        result.append({
            "order_id": order["id"],
            "total_price": order["total_price"],
            "status": order["status"],
            "items": [dict(i) for i in items],
            "created_at": order["created_at"]
        })

    conn.close()

    return jsonify(result)