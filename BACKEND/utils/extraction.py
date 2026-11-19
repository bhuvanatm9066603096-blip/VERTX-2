import os, json, uuid, hashlib
from werkzeug.utils import secure_filename
from config import UPLOAD_DIR, RESULTS_DIR

def head_bytes(path, limit=262144):
    with open(path, "rb") as file:
        return file.read(limit)

def read_text(path, limit=20000):
    with open(path, "rb") as file:
        return file.read(limit).decode("utf-8", errors="replace")

def new_case():
    return "VX-" + uuid.uuid4().hex[:8].upper()

def case_dir(cid):
    p = os.path.join(UPLOAD_DIR, secure_filename(cid))
    os.makedirs(p, exist_ok=True)
    return p

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def save_upload(cid, fs, idx):
    stored = f"{idx}_{secure_filename(fs.filename) or 'file'}"
    path = os.path.join(case_dir(cid), stored)
    fs.save(path)  # original evidence is stored once and never modified
    return {"name": fs.filename, "stored": stored, "size": os.path.getsize(path), "sha256": sha256(path)}

def save_text(cid, text, idx):
    stored = f"{idx}_pasted_text.txt"
    path = os.path.join(case_dir(cid), stored)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return {"name": "pasted_text.txt", "stored": stored, "size": os.path.getsize(path), "sha256": sha256(path)}

def write_manifest(cid, man):
    with open(os.path.join(case_dir(cid), "manifest.json"), "w") as f:
        json.dump(man, f, indent=1)

def read_manifest(cid):
    p = os.path.join(case_dir(cid), "manifest.json")
    return json.load(open(p)) if os.path.exists(p) else None

def save_result(cid, data):
    with open(os.path.join(RESULTS_DIR, f"{secure_filename(cid)}.json"), "w") as f:
        json.dump(data, f)

def load_result(cid):
    p = os.path.join(RESULTS_DIR, f"{secure_filename(cid)}.json")
    return json.load(open(p)) if os.path.exists(p) else None

def list_cases():
    out = []
    for fn in os.listdir(RESULTS_DIR):
        if fn.endswith(".json"):
            d = json.load(open(os.path.join(RESULTS_DIR, fn)))
            o = d["correlation"]["overall"]
            out.append({"id": d["case"]["id"], "created": d["case"]["created"], "files": len(d["results"]), "risk": o["risk"], "level": o["level"]})
    return sorted(out, key=lambda c: c["created"], reverse=True)[:12]
