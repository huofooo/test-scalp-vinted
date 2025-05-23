
import requests
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/1375552352010109040/ASAptOz6NiXR6eWPLvjUl6Vsx-SgGRJyIjx3KeRuUOtZiknHvokvP73e0nWGm1hyTvIP"
SEARCH_URL = "https://www.vinted.fr/vetements?search_text=Steelbook%204k&order=newest_first"

def send_discord_notification(item):
    data = {
        "content": f"📦 Nouvelle annonce Vinted : {item['title']}\n💶 Prix : {item['price']} €\n🔗 Lien : {item['url']}"
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print("❌ Échec de l'envoi Discord :", response.status_code, response.text)

def fetch_new_items():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(SEARCH_URL, headers=headers)
        if response.status_code != 200:
            print(f"❌ Erreur HTTP : {response.status_code}")
            return []

        # Recherche basique des données
        items = []
        for match in response.text.split('data-testid="item-box"'):
            if 'href="' in match and '€' in match:
                try:
                    url = "https://www.vinted.fr" + match.split('href="')[1].split('"')[0]
                    title = match.split('title="')[1].split('"')[0]
                    price = match.split("€")[0].split(">")[-1].strip()
                    item_id = url.split("-")[-1]
                    items.append({
                        "id": item_id,
                        "title": title,
                        "price": price,
                        "url": url
                    })
                except Exception as e:
                    continue
        return items
    except Exception as e:
        print("❌ Erreur :", e)
        return []

seen_ids = set()

while True:
    print("🔍 Vérification des nouvelles annonces...")
    items = fetch_new_items()
    for item in items:
        if item["id"] not in seen_ids:
            send_discord_notification(item)
            seen_ids.add(item["id"])
    print("⏳ Nouvelle vérification dans 60 secondes...")
    time.sleep(60)
