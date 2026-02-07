from flask import Flask, request, Response
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
            r = requests.get(PROXY_JSON_URL)
            proxies_list = [f"http://{p['ip']}:{p['port']}" for p in r.json().get('proxies', [])]
            print(f"Updated: {len(proxies_list)} proxies")
        except: pass
        time.sleep(300)

Thread(target=update_loop, daemon=True).start()

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_engine(path):
    if not proxies_list: return "No Proxy", 502
    
    url = request.url.replace(request.host_url, "")
    if not url.startswith('http'): # Si SearXNG envoie une requête relative
        return f"Proxy Relay Active. List size: {len(proxies_list)}", 200

    proxy = {"http": random.choice(proxies_list), "https": random.choice(proxies_list)}
    
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            data=request.get_data(),
            proxies=proxy,
            timeout=10
        )
        return Response(resp.content, resp.status_code, resp.headers.items())
    except:
        return "Proxy Error", 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
