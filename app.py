from flask import Flask, request
import requests
import random
import time
from threading import Thread

app = Flask(__name__)

# Config
PROXY_JSON_URL = "https://raw.githubusercontent.com/mishableskineetudiant-stack/proxylistfiltered/refs/heads/main/proxies_elite.json"
proxies_list = []

def update_loop():
    global proxies_list
    while True:
        try:
            r = requests.get(PROXY_JSON_URL)
            data = r.json()
            proxies_list = [f"{p['ip']}:{p['port']}" for p in data.get('proxies', [])]
            print(f"Updated: {len(proxies_list)} proxies")
        except Exception as e:
            print(f"Update failed: {e}")
        time.sleep(300) # 5 minutes

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    if not proxies_list:
        return "No proxies available", 502
    
    target_proxy = random.choice(proxies_list)
    # On renvoie simplement l'adresse du proxy choisi
    # SearXNG s'occupera du reste si configuré en tant que proxy HTTP
    return f"Proxy choisi: {target_proxy}", 200

# Lancer l'update en arrière-plan
Thread(target=update_loop, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
