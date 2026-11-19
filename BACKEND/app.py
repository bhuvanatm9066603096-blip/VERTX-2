# BACKEND/app.py
import os
import re
from datetime import timedelta
from functools import wraps

from flask import (
    Flask, jsonify, redirect, request,
    send_from_directory, session, abort
)
from werkzeug.utils import safe_join   # <-- safe path join
from routes.upload import bp as upload_bp
from routes.analyze import bp as analyze_bp
from routes.evidence import bp as evidence_bp
from routes.report import bp as report_bp

# ----------------------------------------------------------------------
# Load central config
# ----------------------------------------------------------------------
from config import (
    SECRET_KEY, SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE,
    SESSION_COOKIE_SECURE, PERMANENT_SESSION_LIFETIME,
    MAX_CONTENT_LENGTH, FRONTEND_DIR, PUBLIC_FILES
)

# ----------------------------------------------------------------------
# Flask app bootstrap
# ----------------------------------------------------------------------
app = Flask(__name__, static_folder=None)   # we serve static files manually
app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=SESSION_COOKIE_HTTPONLY,
    SESSION_COOKIE_SAMESITE=SESSION_COOKIE_SAMESITE,
    SESSION_COOKIE_SECURE=SESSION_COOKIE_SECURE,
    PERMANENT_SESSION_LIFETIME=timedelta(seconds=PERMANENT_SESSION_LIFETIME),
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
)

# Register blueprints (upload, analysis, …)
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)
app.register_blueprint(evidence_bp)
app.register_blueprint(report_bp)

# ----------------------------------------------------------------------
# Helper: authentication utilities
# ----------------------------------------------------------------------
def is_authenticated() -> bool:
    """Return True if a session contains a validated user."""
    return bool(session.get("authenticated") and session.get("email"))

def login_required(view):
    @wraps(view)
    def protected(*args, **kwargs):
        if not is_authenticated():
            # API callers receive JSON, browsers are redirected.
            if request.path.startswith("/api/"):
                return jsonify(error="Authentication required"), 401
            return redirect("/login.html")
        return view(*args, **kwargs)
    return protected

# ----------------------------------------------------------------------
# Public routes
# ----------------------------------------------------------------------
@app.get("/")
@login_required
def root():
    """Serve the main UI entry point."""
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.get("/login.html")
def login_page():
    """Login UI – redirect authenticated users to the app."""
    if is_authenticated():
        return redirect("/")
    return send_from_directory(FRONTEND_DIR, "login.html")

# ----------------------------------------------------------------------
# Login handling (passwords are **hashed** in .env)
# ----------------------------------------------------------------------
from passlib.hash import bcrypt   # pip install passlib[bcrypt]

@app.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))

    # ---- basic validation -------------------------------------------------
    if not re.fullmatch(r"[^@\s]+@gmail\.com", email):
        return jsonify(error="Enter a valid Gmail address."), 400

    # Expect a bcrypt hash stored in the env for each allowed user.
    # Example env entry: VERTX_USER_john@gmail.com=$2b$12$...
    stored_hash = os.getenv(f"VERTX_USER_{email.upper().replace('@', '_')}")
    if not stored_hash or not bcrypt.verify(password, stored_hash):
        return jsonify(error="Invalid credentials."), 401

    # ---- session creation ------------------------------------------------
    session.clear()
    session["authenticated"] = True
    session["email"] = email
    session["display_name"] = email.split("@", 1)[0]
    session.permanent = bool(payload.get("remember"))
    return jsonify(ok=True)

# ----------------------------------------------------------------------
# Logout
# ----------------------------------------------------------------------
@app.post("/logout")
def logout():
    session.clear()
    return jsonify(ok=True)

# ----------------------------------------------------------------------
# Secure static file serving
# ----------------------------------------------------------------------
@app.get("/<path:path>")
@login_required
def protected_files(path):
    """Serve only files inside FRONTEND_DIR and never allow directory traversal."""
    if path in PUBLIC_FILES:
        return send_from_directory(FRONTEND_DIR, path)

    # safe_join prevents "../" attacks
    full_path = safe_join(FRONTEND_DIR, path)
    if not full_path or not full_path.is_file():
        return "Not found", 404

    resp = send_from_directory(FRONTEND_DIR, path)
    # Prevent caching of protected resources
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp

# ----------------------------------------------------------------------
# Global security headers
# ----------------------------------------------------------------------
@app.after_request
def security_headers(response):
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    # Content‑Security‑Policy (only allow assets from our own origin)
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    )
    return response

# ----------------------------------------------------------------------
# Optional: enforce HTTPS & HSTS (only enable in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # In production run behind a proper web server (nginx, Cloud Run, etc.)
    # Set debug=False and bind to 0.0.0.0 for container use.
    app.run(host="0.0.0.0", port=8000, debug=False)
    from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "project": "TruthLens"
    })

@app.route("/api/analyze", methods=["POST"])
def analyze():
    return jsonify({
        "status": "success",
        "message": "Image analysis endpoint working"
    })
    from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "TruthLens backend is working"

if __name__ == "__main__":
    app.run()
    