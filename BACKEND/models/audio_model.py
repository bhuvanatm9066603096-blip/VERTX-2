def score(tempo, blur, meta_risk, ai_tags):
    risk = .25 * tempo + .25 * blur + .5 * meta_risk
    return max(risk, 90) if ai_tags else risk
