from flask import Flask, send_from_directory, redirect
from flask_cors import CORS
import config

from routes.upload import bp as upload_bp
from routes.analyze import bp as analyze_bp
from routes.evidence import bp as evidence_bp
from routes.report import bp as report_bp
from routes.ai import bp as ai_bp


app = Flask(__name__, static_folder=None)


app.config["MAX_CONTENT_LENGTH"] = config.MAX_MB * 1024 * 1024 * 6

CORS(app)


# Register existing routes
for b in (
    upload_bp,
    analyze_bp,
    evidence_bp,
    report_bp,
    ai_bp
):
    app.register_blueprint(b)


@app.get("/")
def root():
    return redirect("/pages/home.html")


@app.get("/<path:p>")
def frontend(p):
    return send_from_directory(config.FRONTEND_DIR, p)


if __name__ == "__main__":
    print("TruthLens running at http://localhost:5000")
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )