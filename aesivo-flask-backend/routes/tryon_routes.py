from flask import Blueprint
from controllers.tryon_controller import (
    upload_image,
    capture_frame,
    save_result,
    get_history,
    delete_result,
)

tryon_bp = Blueprint("tryon", __name__)

# POST  /tryon/upload          — user uploads a photo (multipart/form-data, field: "photo")
tryon_bp.route("/upload",   methods=["POST"])(upload_image)

# POST  /tryon/capture         — save a single webcam frame (JSON, field: "frame" base64)
tryon_bp.route("/capture",  methods=["POST"])(capture_frame)

# POST  /tryon/save            — save the final composited try-on result (JSON, field: "result" base64)
tryon_bp.route("/save",     methods=["POST"])(save_result)

# GET   /tryon/history         — retrieve saved try-on results (?limit=20&offset=0)
tryon_bp.route("/history",  methods=["GET"])(get_history)

# DELETE /tryon/result/<id>    — delete a saved try-on result
tryon_bp.route("/result/<string:result_id>", methods=["DELETE"])(delete_result)