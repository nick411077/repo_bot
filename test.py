import os
import discord
import json
import requests
from discord.ext import commands, tasks


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


user = {'login': ['summit1g', 'eleaguetv', 'gueigotv', 'chocotaco', 'latteda_', 'zrush']}

r = requests.get('https://api.twitch.tv/helix/users',
                 headers={'Client-ID': 'g3v9rj6v0t5cuthn57g3s9sd1sngmz'},
                 params=user)
print(r.url)
g = r.json()
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(g, f, ensure_ascii=False, indent=4)
with open('data.json', 'r', encoding='utf8') as rf:
    twitch = json.loads(rf.read(), object_hook=JSONObject)
print(str(twitch.data[1].id))
