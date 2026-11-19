import numpy as np

def lerp(v, a, b):
    return float(np.clip((v - a) / (b - a) * 100, 0, 100))

def level(r):
    return "high" if r >= 65 else "medium" if r >= 35 else "low"

def confidence(risk, n_signals, limited=False):
    s = 50 + abs(risk - 50) * 0.6 + min(n_signals, 6) * 2 - (20 if limited else 0)
    s = int(max(25, min(85, s)))
    return {"score": s, "label": "high" if s >= 70 else "moderate" if s >= 50 else "low",
            "note": "Heuristic estimate of how consistent the signals are. Not a measured accuracy."}

def signal(id, label, susp, detail):
    return {"id": id, "label": label, "value": int(round(susp)), "detail": detail}

def result(kind, name, risk, signals, flags, limits, meta, **extra):
    risk = int(round(risk))
    r = {"kind": kind, "name": name, "risk": risk, "level": level(risk),
         "confidence": confidence(risk, len(signals), bool(limits)), "signals": signals,
         "flags": flags, "limitations": limits, "meta": meta}
    r.update(extra)
    return r
