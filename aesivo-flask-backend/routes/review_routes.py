from flask import Blueprint
from controllers.review_controller import add_review, get_reviews

review_bp = Blueprint("reviews", __name__)

review_bp.route("/", methods=["POST"])(add_review)
review_bp.route("/<int:product_id>", methods=["GET"])(get_reviews)