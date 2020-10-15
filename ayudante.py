import emoji

import discord
from discord.ext import commands

intent = discord.Intent.default()
bot = commands.Bot(command_prefix = '--', intents = intent)

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

@bot.event
async def on_message(message):

	#: if message is made by bot
    if message.author == bot.user:
    	return

    if message.content.startswith('--hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('--test'):
    	await message.channel.send('This is a test')
    else:
    	pass


#: create test command
#: status: doesn't run, continue another time
@bot.command()
async def info(ctx):
	print('[+] Calling info')
	await ctx.send('[i] Channel: {}'.format(ctx.channel))
	await ctx.send('[i] Resource used: https://medium.com/better-programming/how-to-make-discord-bot-commands-in-python-2cae39cbfd55')

#: place token here
bot.run(token)
