from flask import Blueprint

from controllers.product_controller import (
    get_products,
    get_product,
    related_products,
    get_products_by_category
)

product_bp = Blueprint("product", __name__)

# ALL PRODUCTS
product_bp.route("/", methods=["GET"])(get_products)

# SINGLE PRODUCT
product_bp.route("/<int:id>", methods=["GET"])(get_product)

# RELATED PRODUCTS
product_bp.route("/related/<int:id>", methods=["GET"])(related_products)

# CATEGORY
product_bp.route("/category/<string:category>", methods=["GET"])(get_products_by_category)