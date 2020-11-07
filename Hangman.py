import discord
import Games
import config
from collections import deque 
from discord.ext import commands
Games.init()
client=commands.Bot(command_prefix='$',status=discord.Status.online,activity=discord.Game('$help'))
client.load_extension('Cogs.GamePlay')
client.load_extension('Cogs.Bot_Commands')
client.run(config.token)