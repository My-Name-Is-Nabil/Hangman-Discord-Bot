import discord
import Games
from collections import deque 
from discord.ext import commands
Games.init()
client=commands.Bot(command_prefix='$',status=discord.Status.online,activity=discord.Game('$help'))
client.load_extension('Cogs.GamePlay')
client.load_extension('Cogs.Bot_Commands')
client.run('NzY2NDczMDQ0NTE2MTQzMTQ0.X4j3pg.mr6AVfJ-2_41-ZI6sjcwO3BGoG0')