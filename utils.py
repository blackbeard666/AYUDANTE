import discord

#: store miscellaneous stuff here
HACKER_GREEN = 0x20c20e
WARNING_YELLOW = 0xeed202
ERROR_RED = 0xff0f0f

#: option to add titles
def bot_message(msg, level):

	color_levels = {'success' : HACKER_GREEN,
					'warning' : WARNING_YELLOW,
					'error' : ERROR_RED}

	return discord.Embed(description = msg, colour = color_levels[level])