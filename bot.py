import os
from discord.ext import commands

TOKEN = 'TOKEN'

bot = commands.Bot(command_prefix = '$')

bot.remove_command('help')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'load {extension} done')
    print(f'load {extension} done')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unload {extension} done')
    print(f'unload {extension} done')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'reload {extension} done')
    print(f'reload {extension} done')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(TOKEN)
