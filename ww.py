import os
import discord
import json
import requests
from discord.ext import commands, tasks



class Webhook(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check_status.start()

    def cog_unload(self):
        self.check_status.cancel()

    @tasks.loop(seconds=5)
    async def check_status(self):
        class JSONObject:
            def __init__(self, d):
                self.__dict__ = d

        r = requests.get('https://api.twitch.tv/helix/streams?user_login=gueigotv',
                         headers={'Client-ID': 'g3v9rj6v0t5cuthn57g3s9sd1sngmz'})
        g = r.json()
        with open('data.json', 'w', encoding='utf8') as f:
            json.dump(g, f, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
        with open('data.json', 'r', encoding='utf8')as f:
            twitch = json.loads(f.read(), object_hook=JSONObject)
        print('user_name:', str(twitch.data[0].title))


def setup(bot):
    bot.add_cog(Webhook(bot))
