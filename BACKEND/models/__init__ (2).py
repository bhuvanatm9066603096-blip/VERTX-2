# Replace score() with a trained detector later; the rest of the pipeline stays the same.
W = {"noise": .22, "sensor": .16, "ela": .14, "edge": .12, "color": .08, "meta": .28}

def score(auth_sub, ai_tags):
    auth = sum(auth_sub[k] * w for k, w in W.items())
    risk = min(97, max(3, 100 - auth))
    return max(risk, 92) if ai_tags else risk
