import json
import os
import discord
from discord.ext import commands


class Webhook(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member.guild.name} | {member} has joined a server.')


def setup(bot):
    bot.add_cog(Webhook(bot))
