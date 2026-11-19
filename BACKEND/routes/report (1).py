import os
from flask import Blueprint, jsonify
from utils import file_handler as fh
from services import image_analyzer, video_analyzer, audio_analyzer, text_analyzer, correlation_engine, report_generator
from models import result

bp = Blueprint("analyze", __name__)
RUN = {"image": image_analyzer.analyze, "video": video_analyzer.analyze, "audio": audio_analyzer.analyze, "text": text_analyzer.analyze}

@bp.post("/api/analyze/<cid>")
def analyze(cid):
    man = fh.read_manifest(cid)
    if not man:
        return jsonify(error="Unknown case"), 404
    results = []
    for i, f in enumerate(man["files"]):
        path = os.path.join(fh.case_dir(cid), f["stored"])
        try:
            r = RUN[f["kind"]](path, f["name"], cid, i)
        except Exception as ex:
            r = result(f["kind"], f["name"], 0, [], [], [f"Analysis failed: {ex}"], {})
            r["error"] = True
        r.update(file=f["stored"], sha256=f["sha256"], size=f["size"], index=i)
        results.append(r)
    corr = correlation_engine.correlate(results)
    rep = report_generator.build(cid, man, results, corr)
    data = {"case": man, "results": results, "correlation": corr, "report": rep}
    fh.save_result(cid, data)
    return jsonify(data)

@bp.get("/api/results/<cid>")
def results(cid):
    d = fh.load_result(cid)
    return (jsonify(d), 200) if d else (jsonify(error="No results for this case"), 404)
