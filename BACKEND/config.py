import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
BASE = BASE_DIR
load_dotenv(BASE_DIR / ".env")

FRONTEND_DIR = (BASE_DIR.parent / "FRONTEND").resolve()

if os.getenv("VERCEL") == "1":
    STORAGE_DIR = Path(os.getenv("TMPDIR", "/tmp")) / "vertx"
    UPLOAD_DIR = STORAGE_DIR / "uploads"
    RESULTS_DIR = STORAGE_DIR / "results"
    REPORTS_DIR = STORAGE_DIR / "reports"
else:
    UPLOAD_DIR = BASE_DIR / "uploads"
    RESULTS_DIR = BASE_DIR / "data" / "results"
    REPORTS_DIR = BASE_DIR / "data" / "reports"

for directory in (UPLOAD_DIR, RESULTS_DIR, REPORTS_DIR):
    directory.mkdir(parents=True, exist_ok=True)

MAX_MB = 50
MAX_CONTENT_LENGTH = MAX_MB * 1024 * 1024

EXT = {
    "image": {"jpg", "jpeg", "png", "webp", "bmp", "gif"},
    "video": {"mp4", "mov", "avi", "webm", "mkv"},
    "audio": {"wav", "mp3", "m4a", "ogg", "flac"},
    "text": {"txt", "md", "eml", "csv", "log"},
}

PUBLIC_FILES = {"login.html"}

SECRET_KEY = os.getenv(
    "VERTX_SESSION_SECRET",
    "local-development-only-change-before-deployment",
)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = os.getenv("VERTX_COOKIE_SECURE", "False").lower() == "true"
PERMANENT_SESSION_LIFETIME = 8 * 60 * 60
