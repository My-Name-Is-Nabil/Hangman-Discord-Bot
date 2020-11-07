import discord
import random
import asyncio
import Games
from Classes import Game,ChannelGame
from discord.ext import commands 

class Bot_Commands(commands.Cog):
    def __init__(self,client):
        self.client=client
    @commands.command()
    async def start(self,ctx):
        channel=ctx.message.channel
        if channel not in Games.gamesmap:
            await ctx.send(f'Hangman is not bound to {channel.mention}. To bind hangman use the command $bind.')
        elif len(Games.gamesmap[channel].queue)==0:
            await ctx.send('No words are queued.')
        else:
            game=Games.gamesmap[channel].queue[0]
            if game.running:
                await ctx.send('A game is already in progress.')
            else:
                game.running=True
                await ctx.send(f'Game created by {game.player} and started by {ctx.author}.')
                await ctx.send('Guess the word!')
                x=''
                for i in game.word:
                    if i.lower() in game.guessedletters:
                        x+=i
                    elif i==' ':
                        x+='  '
                    else:
                        x+=' _ '
                await ctx.send('```'+x+'```')
                await ctx.send('```'+Games.HANGMAN_PICS[0]+'```')

    @commands.command()
    async def bind(self,ctx):
        if ctx.message.channel in Games.gamesmap:
            await ctx.send(f'Hangman is already bound to {ctx.message.channel.mention}.')
        else:
            code=random.randint(1,1000)
            while code in Games.codesmap:
                code=random.randint(1,1000)
            Games.gamesmap[ctx.message.channel]=ChannelGame(code)
            Games.codesmap[code]=ctx.message.channel
            await ctx.send(f'Hangman is bound to {ctx.message.channel.mention} with code {Games.gamesmap[ctx.message.channel].code}. DM me the word you want!')
            Games.n+=1
            await asyncio.sleep(60*60)
            await ctx.send(f'Hangman is unbound.')
            Games.n-=1
            Games.gamesmap.pop(ctx.message.channel,None)
            Games.codesmap.pop(code,None)
    @commands.command()
    async def unbind(self,ctx):
        if ctx.message.channel in Games.gamesmap:
            await ctx.send(f'Hangman is unbounded.')
            Games.n-=1
            code=Games.gamesmap[ctx.message.channel].code
            Games.gamesmap.pop(ctx.message.channel,None)
            Games.codesmap.pop(code,None)
        else:
            await ctx.send(f"Hangman isn't bound to {ctx.message.channel.mention}. To bind hangman use the command $bind.")
    @commands.command(aliases=['next'])
    async def skip(self,ctx):
        if ctx.message.channel not in Games.gamesmap:
            await ctx.send(f'Hangman is not bound to {ctx.message.channel.mention}. To bind hangman use the command $bind.')
        elif len(Games.gamesmap[ctx.message.channel].queue)==0:
            await ctx.send('No game is running.')
        elif not Games.gamesmap[ctx.message.channel].queue[0].running: 
            await ctx.send('No game is running.')
        elif Games.gamesmap[ctx.message.channel].queue[0].player==ctx.author:
            word=Games.gamesmap[ctx.message.channel].queue[0].word
            Games.gamesmap[ctx.message.channel].queue.popleft()
            await ctx.send(f'This game is skipped. The word was {word}.')
        elif Games.gamesmap[ctx.message.channel].queue[0].player!=ctx.author:
            await ctx.send(f'Only the user who started the game can skip it.')
    @commands.command()
    async def code(self,ctx):
        if ctx.message.channel not in Games.gamesmap:
            await ctx.send(f"Hangman isn't bound to {ctx.message.channel.mention}. To bind hangman use the command $bind.")
        else:
            await ctx.send(f'The code of this channel is {Games.gamesmap[ctx.message.channel].code}.')

def setup(client):
    client.add_cog(Bot_Commands(client))
