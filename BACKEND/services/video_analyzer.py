import numpy as np
from models import lerp, signal, result
from models.video_model import score
from . import metadata_analyzer as meta

try:
    import cv2
except ImportError:
    cv2 = None


def analyze(path, name, cid, idx):
    metadata = meta.analyze(path, "video")
    metadata_risk = 92 if metadata["ai_tags"] else 30 if metadata["camera"] else 50
    signals = [signal("meta", "Metadata trust", metadata_risk,
                      "AI tag found" if metadata["ai_tags"] else "Camera make found" if metadata["camera"] else "No camera data")]
    flags = []
    limitations = ["Heuristic frame statistics only; no trained deepfake model was used."]
    tempo = 0
    blur = 0
    info = {}

    if metadata["ai_tags"]:
        flags.append({"type": "metadata", "indicator": "AI tool tag: " + ", ".join(metadata["ai_tags"]),
                      "score": 95, "why": "Embedded text names a generator."})

    capture = cv2.VideoCapture(path) if cv2 else None
    if capture is None or not capture.isOpened():
        limitations.append("Frame analysis skipped; only metadata was checked.")
        return result("video", name, metadata_risk, signals, flags, limitations, metadata)

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 25
    frames = []
    positions = np.linspace(0, max(frame_count - 1, 0), min(32, max(frame_count, 2))).astype(int)
    for position in positions:
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(position))
        ok, frame = capture.read()
        if ok:
            gray = cv2.cvtColor(cv2.resize(frame, (192, 108)), cv2.COLOR_BGR2GRAY)
            frames.append((position / fps, gray.astype(np.float32),
                           cv2.Laplacian(gray, cv2.CV_64F).var()))
    capture.release()

    info = {"frames": frame_count, "fps": round(fps, 1), "duration": round(frame_count / fps, 1)}
    if len(frames) >= 4:
        differences = np.array([
            np.abs(frames[i + 1][1] - frames[i][1]).mean()
            for i in range(len(frames) - 1)
        ])
        z_scores = (differences - differences.mean()) / (differences.std() + 1e-6)
        spikes = [i for i, z in enumerate(z_scores) if z > 2.2]
        for i in spikes[:6]:
            flags.append({"type": "frame", "timestamp": round(frames[i + 1][0], 2),
                          "score": int(min(95, 50 + z_scores[i] * 12)),
                          "indicator": "Abrupt change between sampled frames",
                          "why": "Could be a normal cut or a spliced or regenerated segment."})
        sharpness = np.array([frame[2] for frame in frames])
        blur_variation = float(sharpness.std() / (sharpness.mean() + 1e-6))
        tempo = min(100, len(spikes) / len(differences) * 350)
        blur = lerp(blur_variation, .15, .9)
        signals.extend([
            signal("tempo", "Temporal consistency", tempo,
                   f"{len(spikes)} abrupt change(s) in {len(differences)} steps"),
            signal("blur", "Sharpness variation", blur,
                   f"Variation index {blur_variation:.2f}")
        ])
        limitations.append("Only ~32 frames are sampled; normal scene cuts may appear abrupt.")
    else:
        limitations.append("Too few readable frames for temporal analysis.")

    return result("video", name, score(tempo, blur, metadata_risk, metadata["ai_tags"]),
                  signals, flags, limitations, {**metadata, **info})
