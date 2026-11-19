import re
from models import signal, result
from utils.extraction import read_text


CATEGORIES = {
    "urgency": ("Urgency and pressure", 22, r"\b(urgent(ly)?|immediately|right now|act now|within \d+ (hours?|minutes?)|final notice|asap|limited time)\b"),
    "lure": ("Money or prize lure", 26, r"\b(winner|lottery|prize|jackpot|claim your|free gift|guaranteed profit|double your|bitcoin|congratulations)\b"),
    "credentials": ("Credential request", 30, r"\b(otp|password|cvv|verify your account|verify your identity|kyc|aadhaar|card number|bank details|pin)\b"),
    "impersonation": ("Impersonation", 12, r"\b(bank|paypal|amazon|netflix|income tax|customs|fedex|dhl|police|microsoft support)\b"),
    "threat": ("Threats", 24, r"\b(suspended|blocked|locked|legal action|arrest|warrant|penalty|deactivated|unauthori[sz]ed login)\b"),
    "links": ("Suspicious links", 22, r"(?:https?://\S+|www\.\S+|\b(?:bit\.ly|tinyurl\.com|cutt\.ly)/\S*)"),
    "payment": ("Unusual payment demand", 32, r"\b(gift ?cards?|wire transfer|western union|processing fee|advance fee|registration fee|send money|send payment)\b"),
}


def analyze(path, name, cid, idx):
    text = read_text(path)
    signals = []
    flags = []
    total = 0
    for key, (label, weight, pattern) in CATEGORIES.items():
        matches = list(re.finditer(pattern, text, re.I))
        if matches:
            total += weight
            signals.append(signal(key, label, min(100, weight * 3), f"{len(matches)} match(es)"))
            for match in matches[:4]:
                flags.append({"type": "text", "span": [match.start(), match.end()],
                              "snippet": match.group(0)[:60], "score": min(95, weight * 3),
                              "indicator": label, "why": "This phrase is often used in pressure or fraud messages."})
    risk = min(97, total * .8) if total else 5
    words = len(text.split())
    limitations = ["Rule-based phrase matching; it cannot judge context or genuine messages.",
                   "Text analysis is not proof of fraud."]
    if words < 15:
        limitations.append("Very short text gives little evidence.")
    metadata = {
        "words": words,
        "urls": re.findall(CATEGORIES["links"][2], text, re.I)[:10],
        "dates": re.findall(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)[:10],
        "mentions": [],
    }
    return result("text", name, risk, signals, flags, limitations, metadata, text=text)
