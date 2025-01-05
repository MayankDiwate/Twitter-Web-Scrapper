import queue
import threading

import requests

q = queue.Queue()
valid_proxies = []

with open('proxies/proxy_list.txt', 'r') as f:
    proxies = f.read().split('\n')

    for proxy in proxies:
        q.put(proxy)

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get('http://ipinfo.io/json', proxies={'http': proxy, 'https': proxy}, timeout=5)
            print(f'Valid proxy: {proxy}')
            valid_proxies.append(proxy)
        except :
            continue

        if res.status_code == 200:
            with open('proxies/valid_proxy_list.txt', 'a') as f:
                f.write(proxy + '\n')

for _ in range(10):
    t = threading.Thread(target=check_proxies)
    t.start()

