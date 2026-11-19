import hashlib
import json
import os
import uuid

from werkzeug.utils import secure_filename
from config import UPLOAD_DIR, RESULTS_DIR


def new_case():
    return "VX-" + uuid.uuid4().hex[:8].upper()


def case_dir(case_id):
    path = os.path.join(UPLOAD_DIR, secure_filename(case_id))
    os.makedirs(path, exist_ok=True)
    return path


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_upload(case_id, uploaded_file, index):
    stored = f"{index}_{secure_filename(uploaded_file.filename) or 'file'}"
    path = os.path.join(case_dir(case_id), stored)
    uploaded_file.save(path)
    return {"name": uploaded_file.filename, "stored": stored, "size": os.path.getsize(path), "sha256": sha256(path)}


def save_text(case_id, text, index):
    stored = f"{index}_pasted_text.txt"
    path = os.path.join(case_dir(case_id), stored)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
    return {"name": "pasted_text.txt", "stored": stored, "size": os.path.getsize(path), "sha256": sha256(path)}


def write_manifest(case_id, manifest):
    with open(os.path.join(case_dir(case_id), "manifest.json"), "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=1)


def read_manifest(case_id):
    path = os.path.join(case_dir(case_id), "manifest.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_result(case_id, data):
    path = os.path.join(RESULTS_DIR, f"{secure_filename(case_id)}.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_result(case_id):
    path = os.path.join(RESULTS_DIR, f"{secure_filename(case_id)}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def list_cases():
    cases = []
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(RESULTS_DIR, filename), "r", encoding="utf-8") as file:
                data = json.load(file)
            overall = data["correlation"]["overall"]
            cases.append({"id": data["case"]["id"], "created": data["case"]["created"], "files": len(data["results"]), "risk": overall["risk"], "level": overall["level"]})
    return sorted(cases, key=lambda case: case["created"], reverse=True)[:12]