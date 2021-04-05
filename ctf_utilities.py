import discord
import utils
from discord.ext import commands

class ctf_utils(commands.Cog):

	def _init(self, bot):

		self.bot = bot

	def check_chall_name(self, name):

		#: naming convention
		#: must begin with mnemonics of common ctf categories
		categories = ('pwn', 'rev', 'web', 'for', 'msc', 'cry')
		return name.startswith(categories)

	@commands.command(name = 'add-chall')
	async def add_chall(self, ctx, *chall_name):

		#: check if command was sent from _init channel
		if not utils.is_from_channel(ctx.channel.name, '_init'):
			await ctx.channel.send(embed = utils.bot_message('[!] only add challenges on #_init channels', 'error'))
			return

		#: check if chall_name conforms to naming conventions
		chall_name = '-'.join(chall_name).lower()

		if self.check_chall_name(chall_name):
			#: create a channel in that certain ctf category
			await ctx.channel.category.create_text_channel(chall_name)
			await ctx.channel.send(embed = utils.bot_message(f'challenge {chall_name} added. flag it!', 'success'))
		else:
			await ctx.channel.send(embed = utils.bot_message('challenge name must start with any of the ff mnemonics: pwn, rev, web, for, msc, cry', 'warning'))

	@commands.command(name = 'solve-chall')
	async def solve_chall(self, ctx):

		#: determine if ctx.channel is part of a ctf category by checking with naming conventions
		if self.check_chall_name(ctx.channel.name):
			
			#: find the _init channel to notify people of the solve
			try:
				target = [x for x in ctx.channel.category.channels if x.name == '_init'][0]
				await target.send(embed = utils.bot_message(f'{ctx.message.author} solved {ctx.channel.name}!', 'success'))
				await ctx.channel.send(embed = utils.bot_message('GG!', 'success'))
			except:
				await ctx.channel.send(embed = utils.bot_message('could not find #_init channel', 'warning'))
				return
			#: todo: mark channel/chall as solved
		else:
			await ctx.channel.send(embed = utils.bot_message('what are you trying to solve?', 'error'))