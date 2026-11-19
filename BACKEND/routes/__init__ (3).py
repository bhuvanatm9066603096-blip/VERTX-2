from flask import Blueprint, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from config import RESULTS_DIR
from utils import file_handler as fh

bp = Blueprint("evidence", __name__)

@bp.get("/api/evidence/<cid>/original/<path:name>")
def original(cid, name):
    return send_from_directory(fh.case_dir(cid), secure_filename(name))  # read-only access to the preserved original

@bp.get("/api/evidence/<cid>/ela/<name>")
def ela(cid, name):
    return send_from_directory(RESULTS_DIR, f"{secure_filename(cid)}_{secure_filename(name)}")

@bp.get("/api/cases")
def cases():
    return jsonify(fh.list_cases())
