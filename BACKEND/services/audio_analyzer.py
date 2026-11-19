import wave
import os

from models import lerp, signal, result
from models.audio_model import score
from . import metadata_analyzer as meta


def analyze(path, name, cid, idx):
    metadata = meta.analyze(path, "audio")
    tempo = 0
    blur = 0
    flags = []
    limitations = ["Heuristic audio indicators only; no trained voice-cloning detector was used."]
    metadata_risk = 92 if metadata["ai_tags"] else 35

    if metadata["ai_tags"]:
        flags.append({"type": "metadata", "indicator": "AI tool tag: " + ", ".join(metadata["ai_tags"]),
                      "score": 95, "why": "Embedded metadata names a generator."})

    info = {"format": os.path.splitext(path)[1].lower().lstrip(".")}
    if info["format"] == "wav":
        try:
            with wave.open(path, "rb") as wav:
                info.update({
                    "channels": wav.getnchannels(),
                    "sample_rate": wav.getframerate(),
                    "duration": round(wav.getnframes() / wav.getframerate(), 2),
                })
        except wave.Error:
            limitations.append("The WAV container could not be decoded.")
    else:
        limitations.append("Deep format analysis is limited outside WAV files.")

    signals = [
        signal("meta", "Metadata trust", metadata_risk,
               "AI tag found" if metadata["ai_tags"] else "No AI tag found"),
        signal("format", "Container readability", 20 if info.get("duration") else 55,
               f"{info['format'].upper()} container")
    ]
    risk = score(tempo, blur, metadata_risk, metadata["ai_tags"])
    return result("audio", name, risk, signals, flags, limitations, {**metadata, **info})
