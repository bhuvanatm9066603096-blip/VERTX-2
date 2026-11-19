def score(tempo, blur, meta_risk, ai_tags):
    r = .25 * tempo + .25 * blur + .5 * meta_risk
    return max(r, 90) if ai_tags else r
