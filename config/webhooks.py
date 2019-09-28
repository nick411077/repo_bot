import os
import json
import requests
import discord
from discord.ext import commands


r = requests.get('https://api.twitch.tv/helix/users?login=latteda_', headers={'Client-ID': 'g3v9rj6v0t5cuthn57g3s9sd1sngmz'})
data = r.json()
with open('../config/data.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
