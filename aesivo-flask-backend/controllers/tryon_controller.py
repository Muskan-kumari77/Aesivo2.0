import os
import uuid
import base64
import json
from datetime import datetime

from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename

# ─── Allowed extensions ────────────────────────────────────────
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def _upload_root():
    return os.path.join(current_app.static_folder, "uploads", "tryon")

def _public_url(rel_path):
    """Convert a relative path under static/ to a URL the browser can fetch."""
    return "/static/" + rel_path.replace("\\", "/")


# ═══════════════════════════════════════════════════════════════
# POST /tryon/upload
# Accepts a multipart/form-data file upload (field name: "photo")
# Returns: { url, filename, width, height }
# ═══════════════════════════════════════════════════════════════

def upload_image():
    if "photo" not in request.files:
        return jsonify({"error": "No file field 'photo' in request"}), 400

    file = request.files["photo"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    ext      = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    folder   = _ensure_dir(os.path.join(_upload_root(), "photos"))
    filepath = os.path.join(folder, filename)
    file.save(filepath)

    rel = os.path.join("uploads", "tryon", "photos", filename)

    return jsonify({
        "success":  True,
        "url":      _public_url(rel),
        "filename": filename,
    }), 201


# ═══════════════════════════════════════════════════════════════
# POST /tryon/capture
# Accepts JSON: { "frame": "<base64 data-url>" }
# Saves a single webcam frame and returns its URL.
# Used when the user wants to "freeze" their camera for try-on.
# Returns: { url, filename }
# ═══════════════════════════════════════════════════════════════

def capture_frame():
    data = request.get_json(silent=True)
    if not data or "frame" not in data:
        return jsonify({"error": "Missing 'frame' field (base64 data-url)"}), 400

    frame_data = data["frame"]

    # Strip the data-url header if present  (e.g. "data:image/png;base64,...")
    if "," in frame_data:
        frame_data = frame_data.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(frame_data)
    except Exception:
        return jsonify({"error": "Invalid base64 data"}), 400

    filename = f"capture_{uuid.uuid4().hex}.png"
    folder   = _ensure_dir(os.path.join(_upload_root(), "captures"))
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    rel = os.path.join("uploads", "tryon", "captures", filename)

    return jsonify({
        "success":  True,
        "url":      _public_url(rel),
        "filename": filename,
    }), 201


# ═══════════════════════════════════════════════════════════════
# POST /tryon/save
# Accepts JSON: { "result": "<base64 data-url>", "product_id": 5 }
# Saves the final composited canvas image (person + garment).
# Returns: { url, filename, id }
# ═══════════════════════════════════════════════════════════════

def save_result():
    data = request.get_json(silent=True)
    if not data or "result" not in data:
        return jsonify({"error": "Missing 'result' field (base64 data-url)"}), 400

    result_data = data["result"]
    product_id  = data.get("product_id")

    if "," in result_data:
        result_data = result_data.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(result_data)
    except Exception:
        return jsonify({"error": "Invalid base64 data"}), 400

    result_id = uuid.uuid4().hex
    filename  = f"result_{result_id}.png"
    folder    = _ensure_dir(os.path.join(_upload_root(), "results"))
    filepath  = os.path.join(folder, filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # Persist metadata to a simple JSON log next to the images
    meta_path = os.path.join(folder, "index.json")
    history   = _load_json(meta_path)
    history.append({
        "id":         result_id,
        "filename":   filename,
        "product_id": product_id,
        "url":        _public_url(os.path.join("uploads", "tryon", "results", filename)),
        "created_at": datetime.utcnow().isoformat() + "Z",
    })
    _save_json(meta_path, history)

    rel = os.path.join("uploads", "tryon", "results", filename)

    return jsonify({
        "success":    True,
        "id":         result_id,
        "url":        _public_url(rel),
        "filename":   filename,
        "product_id": product_id,
    }), 201


# ═══════════════════════════════════════════════════════════════
# GET /tryon/history
# Returns the last N saved try-on results.
# Query params: ?limit=20&offset=0
# ═══════════════════════════════════════════════════════════════

def get_history():
    limit  = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))

    folder    = os.path.join(_upload_root(), "results")
    meta_path = os.path.join(folder, "index.json")
    history   = _load_json(meta_path)

    # Most recent first
    history = list(reversed(history))
    total   = len(history)
    page    = history[offset: offset + limit]

    return jsonify({
        "results": page,
        "total":   total,
        "limit":   limit,
        "offset":  offset,
    })


# ═══════════════════════════════════════════════════════════════
# DELETE /tryon/result/<result_id>
# Removes a saved try-on result by its ID.
# ═══════════════════════════════════════════════════════════════

def delete_result(result_id):
    folder    = os.path.join(_upload_root(), "results")
    meta_path = os.path.join(folder, "index.json")
    history   = _load_json(meta_path)

    entry = next((r for r in history if r["id"] == result_id), None)
    if not entry:
        return jsonify({"error": "Result not found"}), 404

    # Delete the image file
    filepath = os.path.join(folder, entry["filename"])
    if os.path.exists(filepath):
        os.remove(filepath)

    # Remove from index
    history = [r for r in history if r["id"] != result_id]
    _save_json(meta_path, history)

    return jsonify({"success": True, "deleted": result_id})


# ─── JSON helpers ───────────────────────────────────────────────

def _load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return []

def _save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)