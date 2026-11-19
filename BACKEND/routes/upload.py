import datetime
import os

from flask import Blueprint, jsonify, request
from config import EXT, MAX_MB
from utils import file_handler as fh


bp = Blueprint("upload", __name__)


def kind_from_filename(filename):
    extension = os.path.splitext(filename)[1].lower().lstrip(".")
    for kind, extensions in EXT.items():
        if extension in extensions:
            return kind
    return None


@bp.post("/api/upload")
def upload():
    case_id = fh.new_case()
    files = []

    for index, uploaded in enumerate(request.files.getlist("files")):
        kind = kind_from_filename(uploaded.filename)
        if kind is None:
            continue
        record = fh.save_upload(case_id, uploaded, index)
        record["kind"] = kind
        files.append(record)

    for index, text in enumerate(request.form.getlist("texts")):
        if text.strip():
            record = fh.save_text(case_id, text, len(files) + index)
            record["kind"] = "text"
            files.append(record)

    if not files:
        return jsonify(error="No supported files or text were supplied"), 400

    manifest = {"id": case_id, "created": datetime.datetime.now().isoformat(timespec="seconds"), "files": files}
    fh.write_manifest(case_id, manifest)
    return jsonify(case=manifest), 201
