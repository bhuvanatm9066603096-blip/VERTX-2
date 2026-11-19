# BACKEND/config.py
"""
Central configuration for the VERTX‑2 backend.
All paths are built relative to this file, making the project portable.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env (if present) – never commit secrets to source control.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")                     # <-- reads VERTX_SESSION_SECRET etc.

# ----------------------------------------------------------------------
# Directories
# ----------------------------------------------------------------------
UPLOAD_DIR   = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "data" / "results"
REPORTS_DIR  = BASE_DIR / "data" / "reports"
FRONTEND_DIR = (BASE_DIR.parent / "FRONTEND").resolve()

# Make sure the directories exist at import time.
for d in (UPLOAD_DIR, RESULTS_DIR, REPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# Security‑related constants
# ----------------------------------------------------------------------
# Size limit for a single upload (50 MiB)
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

# Allowed extensions per media type
EXT = {
    "image": {"jpg", "jpeg", "png", "webp", "bmp", "gif"},
    "video": {"mp4", "mov", "avi", "webm", "mkv"},
    "audio": {"wav", "mp3", "m4a", "ogg", "flac"},
    "text":  {"txt", "md", "eml", "csv", "log"},
}

# Public files that may be served without authentication
PUBLIC_FILES = {"login.html"}

# ----------------------------------------------------------------------
# Flask session / cookie configuration
# ----------------------------------------------------------------------
SECRET_KEY = os.getenv(
    "VERTX_SESSION_SECRET",
    "local-development-only-change-before-deployment"
)

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE   = os.getenv("VERTX_COOKIE_SECURE", "False") == "True"   # set True in prod
PERMANENT_SESSION_LIFETIME = 8 * 60 * 60   # seconds (8 h)