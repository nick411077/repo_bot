import os
import discord
from discord.ext import commands, tasks
from twitch import TwitchHelix


class Webhook(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check_status.start()

    def cog_unload(self):
        self.check_status.cancel()

    @tasks.loop(seconds=5)
    async def check_status(self):
        client = TwitchHelix(client_id='g3v9rj6v0t5cuthn57g3s9sd1sngmz')
        stream = client.get_streams(user_logins='shroud')
        print(stream.id)


def setup(bot):
    bot.add_cog(Webhook(bot))
