import os

from flask import Blueprint, jsonify
from utils import file_handler as fh
from services import image_analyzer, video_analyzer, audio_analyzer, text_analyzer, correlation_engine, report_generator
from models import result


bp = Blueprint("analyze", __name__)
RUN = {"image": image_analyzer.analyze, "video": video_analyzer.analyze, "audio": audio_analyzer.analyze, "text": text_analyzer.analyze}


@bp.post("/api/analyze/<case_id>")
def analyze(case_id):
    manifest = fh.read_manifest(case_id)
    if manifest is None:
        return jsonify(error="Unknown case"), 404

    results = []
    for index, file_record in enumerate(manifest["files"]):
        path = os.path.join(fh.case_dir(case_id), file_record["stored"])
        try:
            item = RUN[file_record["kind"]](path, file_record["name"], case_id, index)
        except Exception as error:
            item = result(file_record["kind"], file_record["name"], 0, [], [], [f"Analysis failed: {error}"], {})
            item["error"] = True
        item.update(file=file_record["stored"], sha256=file_record["sha256"], size=file_record["size"], index=index)
        results.append(item)

    correlation = correlation_engine.correlate(results)
    report = report_generator.build(case_id, manifest, results, correlation)
    data = {"case": manifest, "results": results, "correlation": correlation, "report": report}
    fh.save_result(case_id, data)
    return jsonify(data)


@bp.get("/api/results/<case_id>")
def results(case_id):
    data = fh.load_result(case_id)
    return (jsonify(data), 200) if data else (jsonify(error="No results for this case"), 404)
