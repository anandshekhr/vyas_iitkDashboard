import requests
import json
import pandas as pd

url = "http://127.0.0.1:8000/inhouseInventoryInfo/"

def get_data(url):
    r = requests.get(url=url)
    data = json.loads(r.text)
    return data

