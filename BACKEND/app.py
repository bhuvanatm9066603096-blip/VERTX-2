import os
import re
from datetime import timedelta
from functools import wraps

from flask import Flask, jsonify, redirect, request, send_from_directory, session
from routes.upload import bp as upload_bp
from routes.analyze import bp as analyze_bp
from routes.evidence import bp as evidence_bp
from routes.report import bp as report_bp


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "FRONTEND"))
PUBLIC_FILES = {"login.html"}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "VERTX_SESSION_SECRET",
    "local-development-only-change-before-deployment",
)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)
app.register_blueprint(evidence_bp)
app.register_blueprint(report_bp)


def is_authenticated():
    return bool(session.get("authenticated") and session.get("email"))


def login_required(view):
    @wraps(view)
    def protected(*args, **kwargs):
        if not is_authenticated():
            if request.path.startswith("/api/"):
                return jsonify(error="Authentication required"), 401
            return redirect("/login.html")
        return view(*args, **kwargs)

    return protected


@app.get("/")
@login_required
def root():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/login.html")
def login_page():
    if is_authenticated():
        return redirect("/")
    return send_from_directory(FRONTEND_DIR, "login.html")


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not re.fullmatch(r"[^\s@]+@gmail\.com", email):
        return jsonify(error="Enter a valid Gmail address."), 400
    if not password.endswith("@123") or len(password) < 4:
        return jsonify(error="Password must end with @123."), 400

    session.clear()
    session["authenticated"] = True
    session["email"] = email
    session["display_name"] = email.split("@", 1)[0]
    session.permanent = bool(data.get("remember"))

    return jsonify(ok=True)


@app.post("/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/<path:path>")
@login_required
def protected_files(path):
    if path in PUBLIC_FILES:
        return send_from_directory(FRONTEND_DIR, path)

    if not os.path.isfile(os.path.join(FRONTEND_DIR, path)):
        return "Not found", 404

    response = send_from_directory(FRONTEND_DIR, path)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
