import requests
import time
import hashlib

WEBHOOK_URL = "https://discord.com/api/webhooks/1375552352010109040/ASAptOz6NiXR6eWPLvjUl6Vsx-SgGRJyIjx3KeRuUOtZiknHvokvP73e0nWGm1hyTvIP"
KEYWORD = "Steelbook 4k"
CHECK_INTERVAL = 60  # secondes

def fetch_vinted_results(keyword):
    url = f"https://www.vinted.fr/catalog?search_text={keyword.replace(' ', '%20')}&order=newest_first"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Erreur HTTP : {response.status_code}")
            print(f"Contenu reçu : {response.text[:100]}")
            return None
        html = response.text
        return html
    except Exception as e:
        print(f"❌ Exception : {e}")
        return None

def parse_dummy_ads(html):
    # ⚠️ Remplacer cette fonction par un vrai parseur si on a une vraie API ou HTML parser
    # Ici c'est un test simulé
    return [{
        "title": "Steelbook 4k test",
        "price": "15€",
        "url": "https://www.vinted.fr/items/000000-steelbook-4k-test"
    }]

def send_to_discord(ad):
    content = f"**{ad['title']}**\nPrix : {ad['price']}\nLien : {ad['url']}"
    if len(content) > 2000:
        content = content[:1990] + "..."

    payload = {"content": content}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        if response.status_code != 204:
            print(f"❌ Échec de l'envoi Discord : {response.status_code} {response.text}")
        else:
            print(f"✅ Nouvelle annonce envoyée : {ad['title']}")
    except Exception as e:
        print(f"❌ Exception lors de l'envoi : {e}")

def main():
    print("🚀 Démarrage du scalper Vinted...")
    seen = set()
    while True:
        print("🔍 Vérification des annonces...")
        html = fetch_vinted_results(KEYWORD)
        if html:
            ads = parse_dummy_ads(html)
            for ad in ads:
                ad_id = hashlib.md5(ad['url'].encode()).hexdigest()
                if ad_id not in seen:
                    seen.add(ad_id)
                    send_to_discord(ad)
                else:
                    print("🔁 Annonce déjà vue.")
        else:
            print("⚠️ Aucun contenu reçu.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
