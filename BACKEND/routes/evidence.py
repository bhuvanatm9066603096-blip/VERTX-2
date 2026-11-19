import os

from flask import Blueprint, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from config import RESULTS_DIR
from utils import file_handler as fh


bp = Blueprint("evidence", __name__)


@bp.get("/api/evidence/<case_id>/original/<path:name>")
def original(case_id, name):
    safe_name = secure_filename(name)
    return send_from_directory(fh.case_dir(case_id), safe_name)


@bp.get("/api/evidence/<case_id>/ela/<name>")
def ela(case_id, name):
    return send_from_directory(RESULTS_DIR, f"{secure_filename(case_id)}_{secure_filename(name)}")


@bp.get("/api/cases")
def cases():
    return jsonify(fh.list_cases())
