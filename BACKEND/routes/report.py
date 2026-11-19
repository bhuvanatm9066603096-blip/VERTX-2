import os

from flask import Blueprint, jsonify, request, send_file
from config import REPORTS_DIR
from utils import file_handler as fh
from services import report_generator


bp = Blueprint("report", __name__)


@bp.get("/api/report/<case_id>")
def report(case_id):
    data = fh.load_result(case_id)
    return (jsonify(data["report"]), 200) if data else (jsonify(error="No report for this case"), 404)


@bp.get("/api/report/<case_id>/download")
def download(case_id):
    data = fh.load_result(case_id)
    if not data:
        return jsonify(error="No report for this case"), 404

    output_format = "json" if request.args.get("format") == "json" else "html"
    path = os.path.join(REPORTS_DIR, f"{case_id}.{output_format}")
    content = data["report"]
    if output_format == "html":
        content = report_generator.to_html(content)
    else:
        import json
        content = json.dumps(content, indent=2)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)
    return send_file(path, as_attachment=True, download_name=f"vertx_{case_id}.{output_format}")
