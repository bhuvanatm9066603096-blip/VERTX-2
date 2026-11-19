import os
from pathlib import Path

# Base directory of the backend package
BASE = Path(__file__).resolve().parent

# Directories (ensure they exist)
UPLOAD_DIR = BASE / "uploads"
RESULTS_DIR = BASE / "data" / "results"
REPORTS_DIR = BASE / "data" / "reports"
FRONTEND_DIR = (BASE.parent / "FRONTEND").resolve()

# Create directories if missing
for d in (UPLOAD_DIR, RESULTS_DIR, REPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Size limits (MiB)
MAX_MB = 50
MAX_CONTENT_LENGTH = MAX_MB * 1024 * 1024

# Allowed extensions per media type
EXT = {
    "image": {"jpg", "jpeg", "png", "webp", "bmp", "gif"},
    "video": {"mp4", "mov", "avi", "webm", "mkv"},
    "audio": {"wav", "mp3", "m4a", "ogg", "flac"},
    "text":  {"txt", "md", "eml", "csv", "log"},
}

# Public files that can be accessed without authentication
PUBLIC_FILES = {"login.html"}

# Flask session configuration
SECRET_KEY = os.getenv(
    "VERTX_SESSION_SECRET",
    "local-development-only-change-before-deployment",
)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
# In production set VERTX_COOKIE_SECURE=True in .env
SESSION_COOKIE_SECURE = os.getenv("VERTX_COOKIE_SECURE", "False").lower() == "true"
PERMANENT_SESSION_LIFETIME = 8 * 60 * 60  # seconds (8 h)

from pathlib import Path

# Load environment variables (if .env exists)
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# ----------------------------------------------------------------------
# Directories
# ----------------------------------------------------------------------
UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "data" / "results"
REPORTS_DIR = BASE_DIR / "data" / "reports"
FRONTEND_DIR = (BASE_DIR.parent / "FRONTEND").resolve()

# Ensure directories exist
for _d in (UPLOAD_DIR, RESULTS_DIR, REPORTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# Application limits & security settings
# ----------------------------------------------------------------------
MAX_MB = 50  # max upload size in megabytes
MAX_CONTENT_LENGTH = MAX_MB * 1024 * 1024

# Allowed extensions per media type
EXT = {
    "image": {"jpg", "jpeg", "png", "webp", "bmp", "gif"},
    "video": {"mp4", "mov", "avi", "webm", "mkv"},
    "audio": {"wav", "mp3", "m4a", "ogg", "flac"},
    "text": {"txt", "md", "eml", "csv", "log"},
}

# Public files that can be accessed without authentication (e.g., login page)
PUBLIC_FILES = {"login.html"}

# Flask session / cookie configuration (read from env, fallback for dev)
SECRET_KEY = os.getenv(
    "VERTX_SESSION_SECRET",
    "local-development-only-change-before-deployment",
)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = os.getenv("VERTX_COOKIE_SECURE", "False").lower() == "true"
PERMANENT_SESSION_LIFETIME = 8 * 60 * 60  # seconds (8 hours)
