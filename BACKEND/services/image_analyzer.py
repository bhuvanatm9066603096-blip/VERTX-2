import numpy as np
from models import lerp, signal, result
from models.video_model import score
from . import metadata_analyzer as meta
try:
    import cv2
except ImportError:
    cv2 = None

def analyze(path, name, cid, idx):
    m = meta.analyze(path, "video")
    mrisk = 92 if m["ai_tags"] else 30 if m["camera"] else 50
    sigs = [signal("meta", "Metadata trust", mrisk, "AI tag found" if m["ai_tags"] else "Camera make found" if m["camera"] else "No camera data")]
    flags, limits, tempo, blur, info = [], ["Heuristic frame statistics only; no trained deepfake model was used."], 0, 0, {}
    if m["ai_tags"]:
        flags.append({"type": "metadata", "indicator": "AI tool tag: " + ", ".join(m["ai_tags"]), "score": 95, "why": "Embedded text names a generator."})
    cap = cv2.VideoCapture(path) if cv2 else None
    if cap is None or not cap.isOpened():
        limits.append("Frame analysis skipped (install opencv-python-headless or file not readable); only metadata was checked.")
        return result("video", name, mrisk, sigs, flags, limits, m)
    n = int(cap.get(7)); fps = cap.get(5) or 25
    frames = []
    for i in np.linspace(0, max(n - 1, 0), min(32, max(n, 2))).astype(int):
        cap.set(1, int(i)); ok, f = cap.read()
        if ok:
            g = cv2.cvtColor(cv2.resize(f, (192, 108)), cv2.COLOR_BGR2GRAY)
            frames.append((i / fps, g.astype(np.float32), cv2.Laplacian(g, cv2.CV_64F).var()))
    info = {"frames": n, "fps": round(fps, 1), "duration": round(n / fps, 1)}
    if len(frames) >= 4:
        d = np.array([np.abs(frames[k + 1][1] - frames[k][1]).mean() for k in range(len(frames) - 1)])
        z = (d - d.mean()) / (d.std() + 1e-6)
        spikes = [k for k in range(len(d)) if z[k] > 2.2]
        for k in spikes[:6]:
            flags.append({"type": "frame", "timestamp": round(frames[k + 1][0], 2), "score": int(min(95, 50 + z[k] * 12)),
                          "indicator": "Abrupt change between sampled frames",
                          "why": "Could be a normal cut, or a spliced / regenerated segment. Check the clip around this time."})
        lv = np.array([f[2] for f in frames]); bcv = float(lv.std() / (lv.mean() + 1e-6))
        tempo = min(100, len(spikes) / len(d) * 350); blur = lerp(bcv, .15, .9)
        sigs += [signal("tempo", "Temporal consistency", tempo, f"{len(spikes)} abrupt change(s) in {len(d)} steps"),
                 signal("blur", "Sharpness variation", blur, f"Variation index {bcv:.2f}")]
        limits.append("Only ~32 frames are sampled, so ordinary scene cuts also appear as abrupt changes.")
    else:
        limits.append("Too few readable frames for temporal analysis.")
    return result("video", name, score(tempo, blur, mrisk, m["ai_tags"]), sigs, flags, limits, {**m, **info})
