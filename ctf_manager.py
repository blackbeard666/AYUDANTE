import discord
import utils
from discord.ext import commands

class ctf_commands(commands.Cog):

	def _init(self, bot):

		self.bot = bot

	@commands.command(name = 'debug')
	async def debug(self, ctx, *args):

		await ctx.channel.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = utils.SUCCESS_GREEN))
		await ctx.channel.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = utils.WARNING_YELLOW))
		await ctx.channel.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = utils.ERROR_RED))

	#: todo: add error messages
	@commands.command(name = 'init-ctf', brief = 'create a private CTF category', usage = 'ctf-name')
	async def init_ctf(self, ctx, *ctf_name):

		#: check if command was sent from command channel
		if not utils.is_from_channel(ctx.channel.name, 'cc-server'):
			await ctx.channel.send(embed = utils.bot_message('[-] Use this command on the #cc-server channel only', 'warning'))
			return

		#: allows for spaces in the ctf name, joins using - as delimiter
		ctf_name = '-'.join(ctf_name).lower()
		created_category = await ctx.guild.create_category(ctf_name)

		#: check if a category has been created before proceeding with other operations
		if created_category:

			#: create _init channel which serves as general channel for the ctf
			await ctx.channel.send(embed = utils.bot_message(f'CTF room #{ctf_name} has been created.', 'success'))
			await created_category.create_text_channel('_init')

			#: having a voice-channel would be nice too
			await created_category.create_voice_channel('voice-comms', user_limit = 10)

			#: create a ctf-specific role, set category permissions to be accessible only by members with said role
			ctf_specific_role = await created_category.guild.create_role(name = ctf_name, colour = utils.CTF_ROLE_COLOR)
			await created_category.set_permissions(ctf_specific_role, add_reactions = True, read_messages = True, send_messages = True, embed_links = True, attach_files = True, read_message_history = True, external_emojis = True, connect = True, speak = True)
			await created_category.set_permissions(ctx.guild.default_role, read_messages = False, connect = False)
		else:
			await ctx.channel.send(embed = utils.bot_message(f'CTF room {ctf_name} creation failed.', 'error'))

	@commands.command(name = 'set-creds', brief = 'set credentials for a given CTF', usage = 'ctf-link username password')
	async def set_creds(self, ctx, *credentials):

		#: check if command was sent from _init channel
		if not utils.is_from_channel(ctx.channel.name, '_init'):
			await ctx.channel.send(embed = utils.bot_message('[!] Only set credentials on #_init channels', 'error'))
			return

		link, user, passwd = credentials
		creds_msg = await ctx.channel.send(embed = utils.bot_message(f'CTF LINK: {link}\nUSERNAME: {user}\nPASSWORD: {passwd}', 'army'))
		await creds_msg.pin() #: pin the message so that other members can see it

	#: todo: add archiving logic here
	@commands.command(name = 'end-ctf', brief = 'archives the CTF category')
	async def end_ctf(self, ctx):

		#: check if command was sent from _init channel
		if not utils.is_from_channel(ctx.channel.name, '_init'):
			await ctx.channel.send(embed = utils.bot_message('[!] Only end ctfs on #_init channels', 'error'))
			return

		#: TODO: make category + created channels public
		#: TODO: get list of users, remove the ctf role
		#: TODO: add a summary of challenges solved

	#: todo: add reaction/confimation.
	@commands.command(name = 'join-ctf', brief = 'join an ongoing ctf, grants temporary ctf role', usage = 'ctf-name')
	async def join_ctf(self, ctx, *ctf_name):

		#: check if command was sent from _init channel
		if not utils.is_from_channel(ctx.channel.name, 'cc-server'):
			await ctx.channel.send(embed = utils.bot_message('[!] join ctfs on #cc-server', 'error'))
			return

		#: get role and add it to member
		ctf_name = '-'.join(ctf_name).lower()
		try:
			target_role = [x for x in ctx.guild.roles if x.name == ctf_name][0]
			await ctx.author.add_roles(target_role)
		except:
			await ctx.channel.send(embed = utils.bot_message('no such ctf exists', 'error'))