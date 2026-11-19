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
import datetime
from flask import Blueprint, jsonify, request
from config import EXT, MAX_CONTENT_LENGTH
from utils import file_handler as fh
from supabase_client import create_case, upload_file, write_manifest

bp = Blueprint("upload", __name__, url_prefix="/api/upload")

def kind_from_filename(filename: str) -> str | None:
    ext = filename.rsplit(".", 1)[-1].lower()
    for kind, allowed in EXT.items():
        if ext in allowed:
            return kind
    return None

@bp.post("/")
def upload():
    # 1️⃣ Create a new case in Supabase
    case_id = create_case()
    files = []

    # 2️⃣ Process uploaded binary files
    for uploaded in request.files.getlist("files"):
        kind = kind_from_filename(uploaded.filename)
        if not kind:
            continue
        record = upload_file(case_id, uploaded, kind)
        files.append(record)

    # 3️⃣ Process plain‑text fields (sent as separate form fields)
    for idx, txt in enumerate(request.form.getlist("texts")):
        txt = txt.strip()
        if not txt:
            continue
        # store raw text as a tiny “file” in Supabase storage (optional)
        # For simplicity we embed it directly in the manifest
        files.append({
            "filename": f"text_{idx}.txt",
            "url": None,
            "size": len(txt.encode()),
            "kind": "text",
            "content": txt,
            "uploaded_at": datetime.datetime.utcnow().isoformat()
        })

    if not files:
        return jsonify(error="No supported files or text were supplied"), 400

    manifest = {
        "id": case_id,
        "created": datetime.datetime.utcnow().isoformat(timespec="seconds"),
        "files": files,
    }

    # 4️⃣ Store manifest in Supabase
    write_manifest(case_id, manifest)

    return jsonify(case=manifest), 201
