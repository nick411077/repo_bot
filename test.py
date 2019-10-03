import os
import discord
import json
import requests
from discord.ext import commands, tasks
r = requests.get('https://api.twitch.tv/helix/streams?user_login=gueigotv',
                 headers={'Client-ID': 'g3v9rj6v0t5cuthn57g3s9sd1sngmz'})
g = r.json()
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(g, f, ensure_ascii=False)
with open('data.json', 'r', encoding='utf8') as rf:
    twitch = json.loads(rf.read())
print(twitch['data'])
