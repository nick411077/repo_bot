import discord,pymongo
from discord.ext import commands


class Emoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ww(self, ctx):
        await ctx.send('<@&428895842817277953>')




def setup(bot):
    bot.add_cog(Emoji(bot))