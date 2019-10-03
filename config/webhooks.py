import os
import json
import discord
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

        r = requests.get(os.environ['TWITCH_URL'], headers={'Client-ID': os.environ['TWITCH_TOKEN']})
        data = r.json()
        with open('data.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)



def setup(bot):
    bot.add_cog(Webhook(bot))
