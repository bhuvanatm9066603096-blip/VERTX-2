import datetime
import html


def build(case_id, manifest, results, correlation):
    overall = correlation["overall"]
    flagged = []
    for item in results:
        for finding in item["flags"]:
            kind = finding["type"]
            if kind == "region":
                location = f"region x{finding['where']['x'] * 100:.0f}% y{finding['where']['y'] * 100:.0f}%"
            elif kind == "frame":
                location = f"{finding['timestamp']}s"
            elif kind == "text":
                location = f"chars {finding['span'][0]}-{finding['span'][1]}"
            else:
                location = "file metadata"
            flagged.append({
                "file": item["name"],
                "kind": item["kind"],
                "location": location,
                "indicator": finding["indicator"],
                "why": finding["why"],
                "score": finding["score"],
            })
    flagged.sort(key=lambda finding: -finding["score"])
    highest = sorted(results, key=lambda item: -item["risk"])[:1]
    summary = (
        f"Overall indicator level is {overall['level'].upper()} (score {overall['risk']}/100). "
        f"Based on {overall['basis']}. "
        + (f"Highest-scoring item: {highest[0]['name']} ({highest[0]['risk']}/100). " if highest else "")
        + f"{len(flagged)} flagged item(s) and {len(correlation['findings'])} cross-modal observation(s). "
        + "This is an indicator, not a verdict."
    )
    return {
        "case": {"id": case_id, "created": manifest["created"], "generated": datetime.datetime.now().isoformat(timespec="seconds")},
        "summary": {"text": summary, "overall": overall},
        "flagged": flagged,
        "cross_modal": correlation["findings"],
        "trace": [{
            "name": item["name"], "kind": item["kind"], "sha256": item["sha256"],
            "size": item["size"], "risk": item["risk"], "level": item["level"],
            "confidence": item["confidence"]["label"],
            "signals": [f"{signal['label']}: {signal['value']}" for signal in item["signals"]],
        } for item in results],
        "limitations": sorted({limit for item in results for limit in item["limitations"]}),
        "checks": [
            "Obtain the original file from its source.",
            "Have a trained examiner review every finding.",
            "Verify the sender through an independent channel.",
            "Do not act on payment or pressure requests until verified.",
        ],
    }


def to_html(report):
    escape = html.escape
    rows = "".join(
        f"<tr><td>{escape(finding['file'])}</td><td>{escape(finding['location'])}</td>"
        f"<td>{escape(finding['indicator'])}</td><td>{finding['score']}</td>"
        f"<td>{escape(finding['why'])}</td></tr>"
        for finding in report["flagged"]
    )
    cross_modal = "".join(
        f"<li><b>{escape(finding['title'])}</b>: {escape(finding['detail'])}</li>"
        for finding in report["cross_modal"]
    )
    trace = "".join(
        f"<li>{escape(item['name'])} [{item['kind']}] SHA-256 <code>{item['sha256']}</code></li>"
        for item in report["trace"]
    )
    limitations = "".join(f"<li>{escape(limit)}</li>" for limit in report["limitations"])
    return f"""<!doctype html><meta charset="utf-8"><title>VERTX report {escape(report['case']['id'])}</title>
<style>body{{font:14px/1.6 sans-serif;max-width:900px;margin:30px auto;padding:0 16px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:6px;text-align:left}}</style>
<h1>VERTX Forensic Report {escape(report['case']['id'])}</h1>
<h2>Summary</h2><p>{escape(report['summary']['text'])}</p>
<h2>Flagged evidence</h2><table><tr><th>File</th><th>Location</th><th>Indicator</th><th>Score</th><th>Why</th></tr>{rows}</table>
<h2>Cross-modal context</h2><ul>{cross_modal}</ul>
<h2>Source trace</h2><ul>{trace}</ul>
<h2>Limitations</h2><ul>{limitations}</ul>"""
