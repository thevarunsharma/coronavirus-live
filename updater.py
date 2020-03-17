import requests
from pickle import dump
import time
from threading import Thread
import datetime

def fetch_req(country, code, URL, header, data):
    while True:
        try:
            req = requests.get(f"{URL}/api/countries/{code}", headers=header)
            break
        except requests.ConnectionError:
            pass
        time.sleep(2)

    if req.status_code != 200:
        return
    c_data = req.json()
    data[country] = {
        "confirmed" : c_data['confirmed']['value'],
        "deaths" : c_data['deaths']['value'],
        "recovered" : c_data['recovered']['value']
    }
    # print(f"{country} fetched...")

def get_update():
    URL = "https://covid19.mathdro.id"
    header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-IN;q=0.5",
    "cache-control": "no-cache",
    "upgrade-insecure-requests": "1",
    "sec-fetch-user": "?1",
    "sec-fetch-site": "cross-site",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate"
    }
    while True:
        try:
            req = requests.get(f"{URL}/api", headers=header)
            break
        except requests.ConnectionError:
            pass
        time.sleep(2)
    print("Fetched world data...")
    d = req.json()
    world = {
    "confirmed" : d['confirmed']['value'],
    "deaths"    : d['deaths']['value'],
    "recovered" : d['recovered']['value']
    }
    with open("stats/world.pickle", "wb") as fh:
        dump(world, fh)

    while True:
        try:
            req = requests.get(f"{URL}/api/countries/", headers=header)
            break
        except requests.ConnectionError:
            pass
        time.sleep(2)
    print("countries' codes fetched...")

    countries = req.json().get("countries")
    data = {}
    threads = []
    for country, code in countries.items():
        threads.append(Thread(target=fetch_req, args=(country, code, URL, header, data)))
        threads[-1].start()

    for th in threads:
        th.join()
    print("all countries fetched...")

    with open("stats/data.pickle", "wb") as fh:
        dump(data, fh)

    with open("stats/up-date.txt", "w") as fh:
        fh.write(str(datetime.datetime.utcnow().strftime("%d %B, %Y at %H:%M:%S UTC")))
