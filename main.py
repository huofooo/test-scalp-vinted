import requests
import time
import hashlib

WEBHOOK_URL = "https://discord.com/api/webhooks/1375552352010109040/ASAptOz6NiXR6eWPLvjUl6Vsx-SgGRJyIjx3KeRuUOtZiknHvokvP73e0nWGm1hyTvIP"
SEARCH_URL = "https://www.vinted.fr/catalog?search_text=steelbook%204k&order=newest_first"

SENT_ADS = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_ads():
    try:
        response = requests.get(SEARCH_URL, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ Erreur HTTP : {response.status_code}")
            print("Contenu reçu :", response.text[:200])
            return []

        json_data = response.json()
        return json_data.get("items", [])

    except Exception as e:
        print("❌ Erreur pendant la récupération :", e)
        return []

def send_discord_notification(ad):
    title = ad["title"]
    price = ad["price"]
    url = f'https://www.vinted.fr{ad["url"]}'
    image_url = ad["photo"]["url"]

    content = f"**{title}**\n💰 {price} €\n🔗 {url}\n📸 {image_url}"

    if len(content) > 2000:
        content = content[:1997] + "..."

    data = {
        "content": content
    }

    r = requests.post(WEBHOOK_URL, json=data)
    if r.status_code != 204 and r.status_code != 200:
        print("❌ Échec de l'envoi Discord :", r.status_code, r.text)

def hash_ad(ad):
    return hashlib.md5(ad["url"].encode()).hexdigest()

print("✅ Scraper Vinted démarré...")

while True:
    print("🔎 Vérification des annonces Vinted...")
    ads = fetch_ads()
    if ads:
        for ad in ads:
            ad_id = hash_ad(ad)
            if ad_id not in SENT_ADS:
                send_discord_notification(ad)
                SENT_ADS.add(ad_id)
                print(f"✅ Nouvelle annonce envoyée : {ad['title']}")
            else:
                print(f"⏩ Annonce déjà envoyée : {ad['title']}")
    else:
        print("⚠️ Aucune annonce détectée.")

    time.sleep(60)
