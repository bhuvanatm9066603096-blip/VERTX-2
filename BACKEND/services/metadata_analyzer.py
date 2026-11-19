import re
from models import signal, result
from utils.extraction import read_text

CATS = {
 "urg": ("Urgency and pressure", 22, r"\b(urgent(ly)?|immediately|right now|act now|within \d+ (hours?|minutes?)|last chance|final notice|asap|limited time|do not tell|keep (this )?(secret|confidential))\b", "Pressure stops people from checking."),
 "lure": ("Money or prize lure", 26, r"\b(you'?ve won|winner|lottery|prize|jackpot|claim your|free gift|guaranteed (returns?|profit)|double your|crypto|bitcoin|congratulations)\b", "Unexpected rewards are bait for fees or data."),
 "cred": ("Credential request", 30, r"\b(otp|one[- ]time (password|code)|password|cvv|verify your (account|identity|kyc)|kyc|aadhaar|card number|bank details|pin)\b", "Real companies do not ask for OTPs or passwords by message."),
 "imp": ("Impersonation", 12, r"\b(bank|paypal|amazon|netflix|income tax|customs|fedex|dhl|police|microsoft support|sbi|hdfc|icici|official)\b", "Trusted names are borrowed. Contact the organisation via its official channel."),
 "thr": ("Threats", 24, r"\b(suspended|blocked|locked|legal action|arrest|warrant|penalty|deactivated|unauthori[sz]ed (login|transaction))\b", "Fear is used to force quick action."),
 "link": ("Suspicious links", 22, r"(?:https?://\S+|www\.\S+|\b(?:bit\.ly|tinyurl\.com|cutt\.ly)/\S*)", "Links in unsolicited messages often lead to fake login pages."),
 "pay": ("Unusual payment demand", 32, r"\b(gift ?cards?|wire transfer|western union|processing fee|advance fee|registration fee|send (money|payment))\b", "Hard-to-reverse payment methods favoured by scammers."),
}
MEDIA = {"video": r"\b(video|clip|footage|reel)\b", "audio": r"\b(audio|voice (note|message|call)|recording|phone call)\b", "image": r"\b(photo|image|picture|screenshot|selfie)\b"}

def analyze(path, name, cid, idx):
    text = read_text(path)
    flags, sigs, total = [], [], 0
    for k, (label, w, rx, why) in CATS.items():
        hits = list(re.finditer(rx, text, re.I))
        if hits:
            total += w
            sigs.append(signal(k, label, min(100, w * 3), f"{len(hits)} match(es)"))
            for h in hits[:4]:
                flags.append({"type": "text", "span": [h.start(), h.end()], "snippet": h.group(0)[:60], "score": min(95, w * 3),
                              "indicator": label, "why": why})
    risk = min(97, total * .8) if total else 5
    words = len(text.split())
    limits = ["Rule-based phrase matching; it cannot judge context, sarcasm or genuine messages that use these words.",
              "Text analysis says nothing about whether attached media is real."]
    if words < 15:
        limits.append("Very short text gives little to analyse.")
    meta = {"words": words, "urls": re.findall(CATS["link"][2], text, re.I)[:10],
            "dates": re.findall(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)[:10],
            "mentions": [k for k, rx in MEDIA.items() if re.search(rx, text, re.I)]}
    return result("text", name, risk, sigs, flags, limits, meta, text=text)
