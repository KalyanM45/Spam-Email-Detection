import re
from html import unescape
from email.utils import getaddresses
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------
# Function to extract email body content
# ----------------------------------------------------------------------------
def extract_body(msg):
    texts = []

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ("text/plain", "text/html"):
                payload = part.get_payload(decode=True)
                if payload:
                    text = payload.decode(errors="ignore")
                    text = unescape(text)
                    text = BeautifulSoup(text, "html.parser").get_text(" ")
                    texts.append(text)
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text = unescape(payload.decode(errors="ignore"))
            text = BeautifulSoup(text, "html.parser").get_text(" ")
            texts.append(text)

    clean = " ".join(texts)
    clean = re.sub(r'\\+', ' ', clean)
    clean = re.sub(r'[\r\n\t]+', ' ', clean)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

# ----------------------------------------------------------------------------
# Function to extract all recipients from email headers
# ----------------------------------------------------------------------------
def all_recipients(msg):
    fields = []
    for h in ["From", "To", "Cc", "Bcc"]:
        fields.extend(getaddresses([msg.get(h, "")]))
    return ", ".join(sorted(set(addr for _, addr in fields if addr)))

# ----------------------------------------------------------------------------
# Function to clean text for Excel compatibility
# ----------------------------------------------------------------------------
def clean_text(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\u200B\u200C\u200D\u200E\u200F\uFEFF]', '', text)
    text = text.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")
    text = text[:32767]
    if text.startswith(("=", "+", "-", "@")):
        text = "'" + text
    return text