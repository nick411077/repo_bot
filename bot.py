import os
import logging
from discord.ext import commands


TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='$')

bot.remove_command('help')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


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
    try:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'reload {extension} done')
    except Exception as e:
        print(f"{extension} cannot be loaded:")
        raise e


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            print(f"{filename} cannot be loaded:")
            raise e


bot.run(TOKEN)
