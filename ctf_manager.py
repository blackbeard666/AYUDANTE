import discord
import utils
from discord.ext import commands

class ctf_commands(commands.Cog):

	def __init__(self, bot):

		self.bot = bot

	@commands.command(name = 'debug')
	async def debug(self, ctx, *args):

		await ctx.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = utils.HACKER_GREEN))
		await ctx.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = utils.WARNING_YELLOW))
		await ctx.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = utils.ERROR_RED))

	#: todo: add error messages
	@commands.command(name = 'add-ctf')
	async def add_ctf(self, ctx, *ctf_name):

		#: check if command was sent from CTF category
		if ctx.channel.name != 'cc-server':
			await ctx.send(embed = utils.bot_message('[-] Use this command on the #cc-server channel only', 'warning'))
			return

		#: allows for spaces in the ctf name, joins using - as delimiter
		ctf_name = '-'.join(ctf_name)
		created = await ctx.guild.create_category(ctf_name)

		#: check if a category has been created
		if created:
			await ctx.send(embed = utils.bot_message(f'CTF room {ctf_name} has been created.', 'success'))
			await created.create_text_channel('__init__')
		else:
			await ctx.send(embed = utils.bot_message(f'CTF room {ctf_name} creation failed.', 'error'))

	@commands.command(name = 'set-creds')
	async def set_creds(self, ctx, *credentials):

		#: check if command was sent from __init__ channel
		if ctx.channel.name != '__init__':
			await ctx.send(embed = utils.bot_message('[!] Only set credentials for __init__ channels', 'error'))
			return

		link, user, passwd = credentials
		creds_msg = await ctx.send(embed = utils.bot_message(f'Link: {link}\nUsername: {user}\nPassword: {passwd}', 'success'))
		await creds_msg.pin()

	#: todo: add archiving logic here
	@commands.command(name = 'end-ctf')
	async def end_ctf(self, ctx):

		pass
