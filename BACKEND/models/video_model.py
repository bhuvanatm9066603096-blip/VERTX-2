import numpy as np

def lerp(v, a, b):
    return float(np.clip((v - a) / (b - a) * 100, 0, 100))

def level(risk):
    return "high" if risk >= 65 else "medium" if risk >= 35 else "low"

def confidence(risk, n_signals, limited=False):
    score = 50 + abs(risk - 50) * 0.6 + min(n_signals, 6) * 2 - (20 if limited else 0)
    score = int(max(25, min(85, score)))
    return {
        "score": score,
        "label": "high" if score >= 70 else "moderate" if score >= 50 else "low",
        "note": "Heuristic estimate of how consistent the signals are. Not a measured accuracy.",
    }

def signal(identifier, label, susp, detail):
    return {"id": identifier, "label": label, "value": int(round(susp)), "detail": detail}

def result(kind, name, risk, signals, flags, limits, meta, **extra):
    risk = int(round(risk))
    data = {
        "kind": kind,
        "name": name,
        "risk": risk,
        "level": level(risk),
        "confidence": confidence(risk, len(signals), bool(limits)),
        "signals": signals,
        "flags": flags,
        "limitations": limits,
        "meta": meta,
    }
    data.update(extra)
    return data

def score(tempo, blur, meta_risk, ai_tags):
    risk = .25 * tempo + .25 * blur + .5 * meta_risk
    return max(risk, 90) if ai_tags else risk
