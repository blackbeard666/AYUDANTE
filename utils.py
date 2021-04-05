import discord

#: store miscellaneous stuff here
SUCCESS_GREEN  = 0x20c20e
WARNING_YELLOW = 0xeed202
ERROR_RED      = 0xff0f0f
DARK_GREEN     = 0x06170e
CTF_ROLE_COLOR = 0x051094

#: maybe add parameter to include titles
def bot_message(msg, level):

	color_levels = {'success' : SUCCESS_GREEN,
					'warning' : WARNING_YELLOW,
					'error' : ERROR_RED,
					'army' : DARK_GREEN}

	return discord.Embed(description = msg, colour = color_levels[level])

#: just something to make channel comparisons cleaner
def is_from_channel(name, channel):

	return name == channel