import pymongo
import discord
from discord.ext import commands



class Mongo(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mydb = self.myclient["runoobdb"]

	@commands.command()
	async def say(self, ctx, name, *, content):
		self.mycol = self.mydb['{0}'.format(ctx.guild.id)]
		writeDocument = {}
		writeDocument['name'] = name
		writeDocument['content'] = content
		writeDocument['list.name'] = ctx.author.id
		x = self.mycol.update_one({'name': writeDocument['name']}, {'$set': writeDocument}, upsert=True)
		await ctx.send(f' {name} done')
		await ctx.message.delete(delay=10)
		print(f'{x} done')
		print(name)

	@commands.command()
	async def sayremove(self, ctx, name):
		self.mycol = self.mydb['{0}'.format(ctx.guild.id)]
		gg = name 
		y = self.mycol.delete_one({'name': gg})
		if y is not None:
			await ctx.send('{0} removed done'.format(name))
			print('{0} removed'.format(name))

	@commands.command()
	async def saylist(self, ctx, *name):
		self.mycol = self.mydb['{0}'.format(ctx.guild.id)]
		if name:
			embed = discord.Embed(title="詞彙查詢", description="內容", color=0x000000)
			for x in self.mycol.find({ 'name': name[0] }):
				embed.add_field(name="詞彙", value=f"{x['name']}")
				embed.add_field(name="回復", value=f"{x['content']}")
			await ctx.send(embed=embed)
			"""這上面是搜尋詞彙 我不知道為啥for裡面name要套入[0] 只打name就沒辦法讀"""
		else:
			embed = discord.Embed(title="詞彙查詢", description="內容", color=0xeee657)
			for y in self.mycol.find():
				embed.add_field(name="詞彙", value=f"{y['name']}", inline=False)
				embed.add_field(name="回復", value=f"{y['content']}")
			await ctx.message.author.send(embed=embed)
			"""這是全部的詞彙列表"""
			
			


	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot == False:
			self.mycol = self.mydb['{0}'.format(message.guild.id)]
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