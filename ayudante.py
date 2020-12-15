import emoji

import discord
import ctf_manager
from discord.ext import commands

bot = commands.Bot(command_prefix = '--')

#: some variables here, description update later
server_id = 760398919636877313

#: helper functions here
async def init_kartilya():

    kartilya_channel_id = 760413269059043359
    channel = bot.get_channel(kartilya_channel_id)

    #: purge the channel of past messages
    def is_bot_message(message):
    	return message.author == bot.user

    deleted_messages = await channel.purge(limit = 100, check = is_bot_message)
    print('[*] Deleted {} message/s'.format(len(deleted_messages)))

    #: send rules to #kartilya   
    rules = open('kartilya.md', 'r').read() 
    kartilya_rules = discord.Embed(title = 'KARTILYA', description = rules, colour = 0x1e002a)   
    rule_msg = await channel.send(embed = kartilya_rules)
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
    			print(f'[*] KATIPON role assigned to {user.name}')
    		except:
    			print(f'[-] Failed to assign KATIPON role to {user.name}')

#: main bot functions
@bot.event
async def on_ready():
    print(f'[i] Logged in as: {bot.user}')

    #: ISSUE: calling init_kartilya prevents further code from being interpreted
    #: await init_kartilya()
    
    #: todo: add category permissions similar to LOBBY
    #: I don't understand why placing this server variable outside of this function fails to get the server
    server = bot.get_guild(server_id)
    if 'WARZONE' not in [category.name for category in server.categories]:

    	ctf_category = await server.create_category('WARZONE')

    	if ctf_category:
    		print('[*] CTF WARZONE category created')

    	ctf_main_channel = await ctf_category.create_text_channel('ctf-barracks')
    	await ctf_main_channel.edit(topic = 'Main CTF Lobby')

    #: Change bot presence, just for fanciness. 
    #: Might need to change this later to something more suitable
    print('[*] Changing bot presence')
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(name = "send @BLACKBEARD smoll-medium anime tiddies uwu"))

#: register cogs here
bot.add_cog(ctf_manager.ctf_commands(bot))

#: instead of manually removing tokens in each commit
token = open('../Desktop/token').read()
bot.run(token)
