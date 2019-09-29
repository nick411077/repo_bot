import json
import os

import requests

r = requests.get(os.environ['TWITCH_URL'], headers={'Client-ID': os.environ['TWITCH_TOKEN']})
data = r.json()
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
