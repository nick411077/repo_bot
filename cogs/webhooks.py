import json
import os
import discord
from discord.ext import commands, tasks
import requests


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
        with open('../cog/data.json', 'w', encoding='utf8') as wf:
            json.dump(data, wf, ensure_ascii=False)

        with open('../cog/data.json', 'r') as rf:
            jf = json.loads(rf.read())
        print(jf['data']['display_name']['display_name'])
        print('test')


def setup(bot):
    bot.add_cog(Webhook(bot))
