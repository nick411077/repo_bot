import os
import discord
import json
import requests
from threading import Event, Thread
from time import sleep
from discord.ext import commands, tasks


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


user = {'user_login': ['muse_tw']}

r = requests.get('https://api.twitch.tv/helix/streams',
                 headers={'Client-ID': 'g3v9rj6v0t5cuthn57g3s9sd1sngmz'},
                 params=user)
print(r.url)
g = r.json()["data"]
print(g)
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(g, f, ensure_ascii=False, indent=4)
with open('data.json', 'r', encoding='utf8') as rf:
    twitch = json.loads(rf.read(), object_hook=JSONObject)
user_id = [x.id for x in twitch]

print(user_id)

