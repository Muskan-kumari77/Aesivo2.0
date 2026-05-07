from flask import Blueprint
from controllers.contact_controller import save_contact

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/", methods=["POST"])
def contact():
    return save_contact()