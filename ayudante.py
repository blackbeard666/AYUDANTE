import discord
import ctf_manager
import ctf_utilities
from discord.ext import commands

bot = commands.Bot(command_prefix = '--')

#: some variables here, description update later
server_id = 760398919636877313

#: main bot functions
@bot.event
async def on_ready():

    print(f'[i] Logged in as: {bot.user}')

    #: todo: add category permissions similar to LOBBY
    server = bot.get_guild(server_id)
    if 'robots.txt' not in [category.name for category in server.categories]:

    	ctf_category = await server.create_category('robots.txt')

    	if ctf_category:
    		print('[*] robots.txt category created')

    	ctf_main_channel = await ctf_category.create_text_channel('cc-server')
    	await ctf_main_channel.edit(topic = 'command and control channel for the AYUDANTE CTF bot')

    #: Change bot presence, just for fanciness. 
    #: Might need to change this later to something more suitable
    print('[*] Changing bot presence')
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(name = "send @BLACKBEARD anime tiddies UwU"))

#: register cogs here
bot.add_cog(ctf_manager.ctf_commands(bot))
bot.add_cog(ctf_utilities.ctf_utils(bot))

#: instead of manually removing tokens in each commit
token = open('../Desktop/token').read()
bot.run(token)
