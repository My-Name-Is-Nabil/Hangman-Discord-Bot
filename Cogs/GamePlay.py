import discord
import Games
from Classes import Game,ChannelGame
from discord.ext import commands 


async def gameplay(message):
    msg=message.content
    game=Games.gamesmap[message.channel].queue[0]
    word=game.word
    if len(msg)==3 and msg[0]=='#' and msg[-1]=='#' and msg[1].isalnum():   #One letter guess
        if msg[1].lower() in game.guessedletters or msg[1].lower() in game.badguesses:   #Already guessed
            await message.channel.send('Letter already guessed.')
        elif msg[1].lower() in word.lower():           #Correct letter             
            game.guessedletters.add(msg[1].lower())
            x=''
            for i in word:
                if i.lower() in game.guessedletters:
                    x+=i
                elif i==' ':
                    x+='  '
                else:
                    x+=' _ '
            await message.channel.send('```'+x+'```')
            if game.guessedletters==game.letters:
                await message.channel.send("Congratulations, you guessed the correct word!")
                Games.gamesmap[message.channel].queue.popleft()
        else:               #Incorrect letter
            game.trials+=1
            if game.trials>=6:
                await message.channel.send('```'+Games.HANGMAN_PICS[6]+'```')
                await message.channel.send(f'You failed to guess the word!\nThe word was {word}.')
                Games.gamesmap[message.channel].queue.popleft()
            else:
                game.badguesses.add(msg[1].lower())
                x=''
                for i in word:
                    if i.lower() in game.guessedletters:
                        x+=i
                    elif i==' ':
                        x+='  '
                    else:
                        x+=' _ '
                await message.channel.send('```'+Games.HANGMAN_PICS[game.trials]+'```')
                await message.channel.send('```'+x+'```')
    elif msg[0]=='#' and msg[-1]=='#' and (len(msg)-2)==len(word):          #Guess the whole word
        guessedword=msg[1:-1]
        if guessedword.lower() in game.badguesses:   #Already guessed
            await message.channel.send('Word already guessed.')
        elif guessedword.lower()==word.lower():               #Correct guess
            await message.channel.send('```'+word+'```')
            await message.channel.send("Congratulations, you guessed the correct word!")
            Games.gamesmap[message.channel].queue.popleft()
        else:
            game.trials+=1
            if game.trials>=6:
                await message.channel.send('```'+Games.HANGMAN_PICS[6]+'```')
                await message.channel.send(f'You failed to guess the word!\n The word was {word}.')
                Games.gamesmap[message.channel].queue.popleft()
            else:                       #Incorrect guess
                game.badguesses.add(guessedword.lower())
                x=''
                for i in word:
                    if i.lower() in game.guessedletters:
                        x+=i
                    elif i==' ':
                        x+='  '
                    else:
                        x+=' _ '
                await message.channel.send('```'+Games.HANGMAN_PICS[game.trials]+'```')        
                await message.channel.send('```'+x+'```')


class Gameplay(commands.Cog):
    def __init__(self,client):
        self.client=client
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            pass
        elif str(message.channel.type)=='private':
            msg=message.content
            msgcontents=msg.split()
            if len(msgcontents)>=3 and msgcontents[0].lower()=='queue':
                try:
                    code=int(msgcontents[1])
                except:
                    await message.channel.send(f'Invalid code.')
                    return 
                if code not in Games.codesmap:
                    await message.channel.send(f"This code doesn't exist. To get a code use $bind command in the text channel you want to play in.")
                else:
                    words=msgcontents[2:]
                    if not all(map(lambda word: word.isalnum(),words)):
                        await message.channel.send(f"Don't include symbols in your word.")    
                    else:
                        Games.gamesmap[Games.codesmap[code]].queue.append(Game(' '.join(words),message.author))
                        await message.channel.send(f"Your word is added to the queue!\nIt's position is {len(Games.gamesmap[Games.codesmap[code]].queue)}.")
            else:
                await message.channel.send("Unknown command! To queue a word type \"queue <code> <word>\" without the quotation makrs.")
        elif message.channel not in Games.gamesmap:
            pass
        elif len(Games.gamesmap[message.channel].queue)!=0 and Games.gamesmap[message.channel].queue[0].running: 
            await gameplay(message)
def setup(client):
    client.add_cog(Gameplay(client))
