import pymongo
import discord
from discord.ext import commands


class Mongo(commands.Cog):
    """This is a vocabulary reply commandlist."""

    def __init__(self, bot):
        self.bot = bot
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["guild_db"]

    @commands.command()
    async def say(self, ctx, name, *, content):
        """This is a vocabulary reply"""
        self.mycol = self.mydb[f'{ctx.guild.id}']
        writeDocument = {'name': name, 'content': content, 'author': ctx.author.name}
        x = self.mycol.update_one({'name': writeDocument['name']}, {'$set': writeDocument}, upsert=True)
        embed = discord.Embed(title="詞彙建立", description="內容", color=0xffffff)
        embed.add_field(name="詞彙", value=f"{name}")
        embed.add_field(name="回復", value=f"{content}")
        embed.add_field(name="建立者", value=f"{ctx.author.name}")
        await ctx.send(embed=embed)
        print(f'{x} done')
        print(name)

    @commands.command()
    async def sayremove(self, ctx, name):
        """This is a vocabulary reply remove."""
        self.mycol = self.mydb[f'{ctx.guild.id}']
        gg = name
        y = self.mycol.delete_one({'name': gg})
        if y is not None:
            await ctx.send(f'{name} removed done')
            print(f'{name} removed')

    @commands.command()
    async def saylist(self, ctx, *name):
        """Gets all saylist of mine."""
        self.mycol = self.mydb[f'{ctx.guild.id}']
        if name:
            embed = discord.Embed(title="詞彙查詢", description="內容", color=0xffffff)
            for x in self.mycol.find({'name': name[0]}):
                embed.add_field(name="詞彙", value=f"{x['name']}")
                embed.add_field(name="回復", value=f"{x['content']}")
                embed.add_field(name="建立者", value=f"{x['author']}")

            await ctx.send(embed=embed)
            """這上面是搜尋詞彙"""
        else:
            con_desc = ''
            for y in self.mycol.find():
                con_desc += f"{y['name']}\n"
            embed = discord.Embed(title="詞彙查詢", description=f"內容\n{con_desc}", color=0xeee657)
            await ctx.message.author.send(embed=embed)
            """這是全部的詞彙列表"""

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.guild:
                self.mycol = self.mydb[f'{message.guild.id}']
                name = message.content
                if message.content.startswith(name):
                    data = name
                    nick = {'name': data}
                    y = self.mycol.find_one(nick)
                    if y is not None:
                        await message.channel.send(y['content'])
                        print(y['_id'])


def setup(bot):
    bot.add_cog(Mongo(bot))
