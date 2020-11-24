import emoji

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix = '--')

#: some variables here, description update later
server_id = 760398919636877313

@bot.event
async def on_ready():
    print('[i] Logged in as: {}'.format(bot.user))

    kartilya_channel_id = 760413269059043359
    channel = bot.get_channel(kartilya_channel_id)

    #: purge the channel of past messages
    def is_bot_message(message):
    	return message.author == bot.user

    deleted_messages = await channel.purge(limit = 100, check = is_bot_message)
    print('[*] Deleted {} message/s'.format(len(deleted_messages)))

    #: todo: add category permissions similar to LOBBY
    #: create a CTF category
    server = bot.get_guild(server_id)
    if 'CTF' not in [category.name for category in server.categories]:

    	ctf_category = await server.create_category('CTF')

    	if ctf_category:
    		print('[*] CTF category created')

    	ctf_main_channel = await ctf_category.create_text_channel('ctf-main')
    	await ctf_main_channel.edit(topic = 'Main CTF Lobby')

    #: send rules to #kartilya   
    kartilya_rules = open('kartilya.md', 'r').read()    
    rule_msg = await channel.send(kartilya_rules)
    await rule_msg.add_reaction(emoji.emojize(':drop_of_blood:'))

    #: reaction-based role assignment here
    while True:
    	reaction, user = await bot.wait_for('reaction_add')

    	#: only accept :blood:, continue loop otherwise
    	if emoji.demojize(reaction.emoji) != ':drop_of_blood:':
    		continue

    	#: retrieve katipon_role
    	katipon_role = discord.utils.get(user.guild.roles, name = 'KATIPON')

    	#: check if only role is @everyone
    	if len(user.roles) == 1:
    		#: assign KATIPON role
    		try:
    			await user.add_roles(katipon_role)
    			print('[*] KATIPON role assigned to {}'.format(user.name))
    		except:
    			print('[-] Failed to assign KATIPON role to {}'.format(user.name))

@bot.command(name = 'info')
async def info(ctx, *args):
	await ctx.send('`[i] Channel: {}`'.format(ctx.channel))
	
	#: test to create an Embed object
	await ctx.send(embed = discord.Embed(title = 'Test Title', description = 'Testing out how embeds work', colour = 0x2ecc71))

#: todo: add error messages
@bot.command(name = 'ctf-channel')
async def add_ctf(ctx, ctf_name):

	#: check if command was sent from CTF category
	if ctx.channel.name != 'ctf-main':
		await ctx.send('`[-] Use this command on the #ctf-main channel only`')
		return

	await ctx.channel.category.create_text_channel(ctf_name)

#: todo: add archiving logic here
@bot.command(name = 'end-ctf')
async def end_ctf(ctx):

	#: check if channel is in CTF category before deletion
	if ctx.channel.category.name == 'CTF' and ctx.channel.name != 'ctf-main':
		print('[-] Deleting channel: ' + ctx.channel.name)
		await ctx.channel.delete()

#: instead of manually removing tokens in each commit
token = open('../Desktop/token').read()
bot.run(token)
