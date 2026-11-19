import os
BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE, "uploads")
RESULTS_DIR = os.path.join(BASE, "data", "results")
REPORTS_DIR = os.path.join(BASE, "data", "reports")
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(BASE), "FRONTEND"))
MAX_MB = 50
EXT = {
    "image": {"jpg", "jpeg", "png", "webp", "bmp", "gif"},
    "video": {"mp4", "mov", "avi", "webm", "mkv"},
    "audio": {"wav", "mp3", "m4a", "ogg", "flac"},
    "text": {"txt", "md", "eml", "csv", "log"},
}
for _d in (UPLOAD_DIR, RESULTS_DIR, REPORTS_DIR):
    os.makedirs(_d, exist_ok=True)
