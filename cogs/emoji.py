import discord,pymongo
from discord.ext import commands


class Emoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(Emoji(bot))