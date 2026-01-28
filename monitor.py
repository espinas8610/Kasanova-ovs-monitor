import feedparser
import requests
from datetime import datetime, timezone
import os
 
KEYWORD = "kasanova ovs"
RSS_URL = fhttps://news.google.com/rss/search?q={KEYWORD.replace(' ', '+')}&hl=it&gl=IT&ceid=IT:it
 
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
 
FILE_URL_INVIATI = "url_inviati.txt"
 
def invia_telegram(testo):
    url = fhttps://api.telegram.org/bot{BOT_TOKEN}/sendMessage
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": testo,
        "disable_web_page_preview": True
    })
 
# carica url già inviati
with open(FILE_URL_INVIATI, "r", encoding="utf-8") as f:
    url_inviati = set(line.strip() for line in f if line.strip())
 
feed = feedparser.parse(RSS_URL)
oggi = datetime.now(timezone.utc).date()
 
nuovi = []
 
for entry in feed.entries:
    if hasattr(entry, "published_parsed"):
        data = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).date()
        if data == oggi and entry.link not in url_inviati:
            nuovi.append(f"• {entry.title}\n{entry.link}")
            url_inviati.add(entry.link)
 
if nuovi:
    messaggio = (
        "📰 Nuove pubblicazioni OGGI – kasanova ovs\n\n"
        + "\n\n".join(nuovi)
    )
    invia_telegram(messaggio)
 
    # aggiorna il file anti-duplicati
    with open(FILE_URL_INVIATI, "w", encoding="utf-8") as f:
        for url in url_inviati:
            f.write(url + "\n")