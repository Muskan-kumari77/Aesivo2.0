from flask import request, jsonify, current_app
from db import get_db
import jwt


# =========================================
# GET USER ID FROM TOKEN
# =========================================

def get_user_id():

    token = request.headers.get("Authorization")

    if not token:
        return None

    try:

        token = token.split(" ")[1]

        decoded = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )

        return decoded["user_id"]

    except:
        return None


# =========================================
# ADD TO CART
# =========================================

def add_to_cart():

    user_id = get_user_id()

    if not user_id:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    data = request.get_json()

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    conn = get_db()

    existing = conn.execute("""

        SELECT *
        FROM cart
        WHERE user_id=? AND product_id=?

    """, (user_id, product_id)).fetchone()

    if existing:

        conn.execute("""

            UPDATE cart
            SET quantity = quantity + ?
            WHERE id=?

        """, (quantity, existing["id"]))

    else:

        conn.execute("""

            INSERT INTO cart
            (user_id, product_id, quantity)

            VALUES (?, ?, ?)

        """, (user_id, product_id, quantity))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Added to cart"
    })


# =========================================
# GET CART
# =========================================

def get_cart():

    user_id = get_user_id()

    if not user_id:
        return jsonify([])

    conn = get_db()

    items = conn.execute("""

        SELECT

            cart.id,
            cart.quantity,

            products.name,
            products.price,
            products.image

        FROM cart

        JOIN products
        ON cart.product_id = products.id

        WHERE cart.user_id=?

        ORDER BY cart.id DESC

    """, (user_id,)).fetchall()

    conn.close()

    return jsonify([
        dict(item)
        for item in items
    ])


# =========================================
# UPDATE CART
# =========================================

def update_cart(cart_id):

    data = request.get_json()

    quantity = data.get("quantity")

    conn = get_db()

    if quantity <= 0:

        conn.execute("""

            DELETE FROM cart
            WHERE id=?

        """, (cart_id,))

    else:

        conn.execute("""

            UPDATE cart
            SET quantity=?
            WHERE id=?

        """, (quantity, cart_id))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Updated"
    })


# =========================================
# REMOVE
# =========================================

def remove_from_cart(cart_id):

    conn = get_db()

    conn.execute("""

        DELETE FROM cart
        WHERE id=?

    """, (cart_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Removed"
    })


# =========================================
# CLEAR
# =========================================

def clear_cart():

    user_id = get_user_id()

    conn = get_db()

    conn.execute("""

        DELETE FROM cart
        WHERE user_id=?

    """, (user_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Cleared"
    })