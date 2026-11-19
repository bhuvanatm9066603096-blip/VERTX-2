import os, json
from flask import Blueprint, jsonify, request, send_file
from config import REPORTS_DIR
from utils import file_handler as fh
from services import report_generator

bp = Blueprint("report", __name__)

@bp.get("/api/report/<cid>")
def report(cid):
    d = fh.load_result(cid)
    return (jsonify(d["report"]), 200) if d else (jsonify(error="No report for this case"), 404)

@bp.get("/api/report/<cid>/download")
def download(cid):
    d = fh.load_result(cid)
    if not d:
        return jsonify(error="No report for this case"), 404
    fmt = "json" if request.args.get("format") == "json" else "html"
    path = os.path.join(REPORTS_DIR, f"{cid}.{fmt}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(d["report"], indent=1) if fmt == "json" else report_generator.to_html(d["report"]))
    return send_file(path, as_attachment=True, download_name=f"truthlens_{cid}.{fmt}")
