# BACKEND/routes/upload.py
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from config import UPLOAD_DIR, EXT, MAX_CONTENT_LENGTH

bp = Blueprint('upload', __name__, url_prefix='/api/upload')

def allowed_file(filename: str) -> bool:
    """Return True if the file extension is in the whitelist."""
    ext = filename.rsplit(".", 1)[-1].lower()
    # flatten all extension sets into a single allowed set
    allowed = set().union(*EXT.values())
    return ext in allowed

@bp.post("/")
def upload():
    # ---------------------------------------------------------
    # Size check – Flask already blocks > MAX_CONTENT_LENGTH,
    # but we double‑check for a friendly error message.
    # ---------------------------------------------------------
    if request.content_length is not None and request.content_length > MAX_CONTENT_LENGTH:
        return jsonify(error="File exceeds maximum allowed size (50 MiB)."), 413

    if "file" not in request.files:
        return jsonify(error="No file part in the request."), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify(error="No selected file."), 400

    if not allowed_file(file.filename):
        return jsonify(error="File type not allowed."), 400

    # ---------------------------------------------------------
    # Save the file safely
    # ---------------------------------------------------------
    filename = secure_filename(file.filename)
    dest = os.path.join(UPLOAD_DIR, filename)

    # Prevent overwriting existing uploads (optional)
    if os.path.exists(dest):
        return jsonify(error="File with that name already exists."), 409

    file.save(dest)
    return jsonify(ok=True, filename=filename)