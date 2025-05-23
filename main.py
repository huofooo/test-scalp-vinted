import requests
from bs4 import BeautifulSoup
import time
import hashlib

WEBHOOK_URL = "https://discord.com/api/webhooks/1375552352010109040/ASAptOz6NiXR6eWPLvjUl6Vsx-SgGRJyIjx3KeRuUOtZiknHvokvP73e0nWGm1hyTvIP"
SEARCH_URL = "https://www.vinted.fr/vetements?search_text=steelbook+4k&order=newest_first"
HEADERS = {"User-Agent": "Mozilla/5.0"}

SENT_ADS = set()

def hash_ad(url):
    return hashlib.md5(url.encode()).hexdigest()

def get_ads():
    try:
        response = requests.get(SEARCH_URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select("a[href^='/items/']")
        ads = []
        for item in items:
            url = "https://www.vinted.fr" + item["href"]
            title = item.get_text(strip=True)
            ad_hash = hash_ad(url)

            if ad_hash not in SENT_ADS:
                ads.append((url, title, ad_hash))

        return ads
    except Exception as e:
        print("❌ Erreur pendant la récupération :", e)
        return []

def send_discord_message(url, title):
    message = f"🆕 **{title}**\n🔗 {url}"
    if len(message) > 2000:
        message = message[:1997] + "..."

    r = requests.post(WEBHOOK_URL, json={"content": message})
    if r.status_code not in (200, 204):
        print("❌ Erreur Discord :", r.status_code, r.text)

print("✅ Scraper HTML lancé...")

while True:
    print("🔄 Vérification en cours...")
    ads = get_ads()
    for url, title, ad_hash in ads:
        send_discord_message(url, title)
        SENT_ADS.add(ad_hash)
        print(f"✅ Nouvelle annonce envoyée : {title}")
    time.sleep(60)
