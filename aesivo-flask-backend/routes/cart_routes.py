from flask import Blueprint

from controllers.cart_controller import (
    add_to_cart,
    get_cart,
    remove_from_cart,
    update_cart,
    clear_cart
)

cart_bp = Blueprint("cart", __name__)

# ADD
@cart_bp.route("/", methods=["POST"])
def add_cart():
    return add_to_cart()

# GET
@cart_bp.route("/", methods=["GET"])
def fetch_cart():
    return get_cart()

# UPDATE
@cart_bp.route("/update/<int:cart_id>", methods=["PUT"])
def update_item(cart_id):
    return update_cart(cart_id)

# REMOVE
@cart_bp.route("/remove/<int:cart_id>", methods=["DELETE"])
def remove_item(cart_id):
    return remove_from_cart(cart_id)

# CLEAR
@cart_bp.route("/clear", methods=["DELETE"])
def clear_items():
    return clear_cart()