from flask import Flask
import requests
import random
import time
from threading import Thread

app = Flask(__name__)

PROXY_JSON_URL = "https://raw.githubusercontent.com/mishableskineetudiant-stack/proxylistfiltered/refs/heads/main/proxies_elite.json"
proxies_list = []

def update_loop():
    global proxies_list
    while True:
        try:
            r = requests.get(PROXY_JSON_URL, timeout=10)
            data = r.json()
            # On stocke juste l'adresse IP:PORT
            proxies_list = [f"http://{p['ip']}:{p['port']}" for p in data.get('proxies', [])]
            print(f"Update: {len(proxies_list)} proxies loaded")
        except Exception as e:
            print(f"Update failed: {e}")
        time.sleep(300)

Thread(target=update_loop, daemon=True).start()

@app.route('/')
def get_random_proxy():
    if not proxies_list:
        return "http://1.1.1.1:80", 200 # Fallback si vide
    return random.choice(proxies_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
