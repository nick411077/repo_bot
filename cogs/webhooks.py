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
        print('test')


def setup(bot):
    bot.add_cog(Webhook(bot))
