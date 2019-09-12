import discord
import datetime
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Events
    commands.has_permissions(add_reactions=True, embed_links=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        t = datetime.datetime.now()
        if message.guild:
            print(f"{t} | " + message.guild.name + " | " + message.channel.name + " | " + message.author.name + ": " + message.content)

        else:
            print(f"{t} | " + message.author.name + ": " + message.content)

    # Commands
    @commands.command()
    async def help(self, ctx, *cog):
        """Gets all cogs and commands of mine."""
        try:
            if not cog:
                halp = discord.Embed(title='Help Listing Commands',
                                     description='Use `$help *command*` to find out more about them!\n(BTW, '
                                                 'the Command Name Must Be in Title Case, Just Like this Sentence.)')

                for x in self.bot.cogs:
                    cogs_desc = ''
                    for c in self.bot.get_cog(x).get_commands():
                        if not c.hidden:
                            cogs_desc += f'**{c.name}** - {c.help}\n'
                    halp.add_field(name=x, value=f'{self.bot.cogs[x].__doc__}\n\n{cogs_desc}', inline=False)
                await ctx.send('', embed=halp)
            else:
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!', description='That is way too many cogs!',
                                         color=discord.Color.red())
                    await ctx.send('', embed=halp)
                else:
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp = discord.Embed(title=cog[0] + ' Command Listing',
                                                     description=self.bot.cogs[cog[0]].__doc__)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name, value=c.help, inline=False)
                                found = True
                    if not found:
                        halp = discord.Embed(title='Error!', description='How do you even use "' + cog[0] + '"?',
                                             color=discord.Color.red())
                    await ctx.send('', embed=halp)
        except:
            pass


def setup(bot):
    bot.add_cog(Help(bot))
