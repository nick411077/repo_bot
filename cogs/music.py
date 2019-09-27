import discord
import youtube_dl
from discord.ext import commands

TOKEN= 'MzcyNjE2ODExNzM0MzY4MjU3.XYyzcA.rwHRkRTCbycC3eC9001CLJjnol0'
bot = commands.Bot(command_prefix = '$')

players = {}

@bot.event
async def on_ready():
	print('Bot online.')


@bot.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.channel
	await channel.connect()


@bot.command(pass_context=True)
async def leave(ctx):
	server = ctx.guild.voice_client
	await server.disconnect()

@bot.command(pass_context=True)
async def play(self, ctx, *, url):
	ctx.guild.voice_client.play(discord.FFmpegPCMAudio(url))


bot.run(TOKEN)
