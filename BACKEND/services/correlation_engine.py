from models import level


def correlate(results):
    findings = []

    def add(severity, title, detail, sources):
        findings.append({"severity": severity, "title": title, "detail": detail, "sources": sources})

    media = [item for item in results if item["kind"] != "text"]
    texts = [item for item in results if item["kind"] == "text"]
    high = [item for item in results if item["risk"] >= 60]
    low = [item for item in results if item["risk"] <= 30]

    if len(results) < 2:
        add("info", "Single input", "Only one item was supplied, so no cross-modal comparison was possible.",
            [item["name"] for item in results])
    if high and low:
        add("weakens", "Conflicting signals",
            "Some items look suspicious while others look ordinary. Treat the case as unresolved.",
            [item["name"] for item in high + low])

    for text in texts:
        if text["risk"] >= 50 and any(item["risk"] >= 50 for item in media):
            add("strengthens", "Pressure language accompanies suspicious media",
                "The text uses scam-style pressure while attached media also shows indicators.",
                [text["name"]] + [item["name"] for item in media if item["risk"] >= 50])

    seen = {}
    for item in results:
        seen.setdefault(item["sha256"], []).append(item["name"])
    for digest, names in seen.items():
        if len(names) > 1:
            add("info", "Duplicate files", "Files have identical SHA-256 hashes.", names)

    risks = [item["risk"] for item in results] or [0]
    risk = int(max(0, min(97, .6 * max(risks) + .4 * sum(risks) / len(risks)
                              + (5 if any(f["severity"] == "strengthens" for f in findings) else 0)
                              - (8 if any(f["severity"] == "weakens" for f in findings) else 0))))
    modality_count = len({item["kind"] for item in results})
    confidence = int(max(25, min(85, 45 + 8 * min(modality_count, 4)
                              + (8 if any(f["severity"] == "strengthens" for f in findings) else 0)
                              - (12 if any(f["severity"] == "weakens" for f in findings) else 0))))

    nodes = [{"id": i, "label": item["name"], "kind": item["kind"], "risk": item["risk"]}
             for i, item in enumerate(results)]
    edges = []
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            a = results[i]["risk"]
            b = results[j]["risk"]
            relation = "agree" if a >= 60 and b >= 60 else "conflict" if max(a, b) >= 70 and min(a, b) <= 30 else "weak"
            edges.append({"a": i, "b": j, "relation": relation})

    return {
        "findings": findings,
        "graph": {"nodes": nodes, "edges": edges},
        "overall": {
            "risk": risk,
            "level": level(risk),
            "confidence": {
                "score": confidence,
                "label": "high" if confidence >= 70 else "moderate" if confidence >= 50 else "low",
                "note": "Heuristic consistency estimate, not a measured accuracy.",
            },
            "basis": f"{len(results)} item(s) across {modality_count} modality type(s)",
        },
    }
