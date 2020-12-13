import discord
from discord.ext import commands

class Management(commands.Cog):

	def __init__(self, bot):

		self.bot = bot

	@commands.command(name = 'info')
	async def info(self, ctx, *args):
		await ctx.send(f'`[i] Channel: {ctx.channel}`')
		
		#: test to create an Embed object
		await ctx.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = 0x2ecc71))

	#: todo: add error messages
	@commands.command(name = 'add-ctf')
	async def add_ctf(self, ctx, ctf_name):

		#: check if command was sent from CTF category
		if ctx.channel.name != 'ctf-main':
			await ctx.send('`[-] Use this command on the #ctf-main channel only`')
			return

		await ctx.channel.category.create_text_channel(ctf_name)

	#: todo: add archiving logic here
	@commands.command(name = 'end-ctf')
	async def end_ctf(self, ctx):

		#: check if channel is in CTF category before deletion
		if ctx.channel.category.name == 'CTF' and ctx.channel.name != 'ctf-main':
			print('[-] Deleting channel: ' + ctx.channel.name)
			await ctx.channel.delete()