import discord
from discord.ext import commands


class Example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(type=0, name="$help"))
        print('Bot is Online{0}!'.format(self.bot.user))
        print(self.bot.user.id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member.guild.name} | {member} has joined a server.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member.guild.name} | {member} has left a server.')

    # Commands

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')
        await ctx.message.delete(delay=3)

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)
        embed.add_field(name="Author", value="nickcan")
        embed.add_field(name="Server count", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="Invite",
                        value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=372616811734368257"
                              "&permissions=8&scope=bot)")
        await ctx.message.delete()
        await ctx.send(embed=embed)
        await ctx.message.delete(delay=3)

    @commands.command()
    async def clear(self, ctx, amount=50):
        await ctx.channel.purge(limit=amount+1)


def setup(bot):
    bot.add_cog(Example(bot))
