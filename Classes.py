from collections import deque
class Game():
    def __init__(self,word,player):
        self.word=word
        self.player=player
        self.trials=0
        self.guessedletters=set()
        self.letters=set(word.lower())
        self.letters.discard(' ')
        self.running=False
        self.badguesses=set()
    def __eq__(self,game):
        return self.word==game.word and self.player==game.player
class ChannelGame():
    def __init__(self,code):
        self.queue=deque()
        self.code=code