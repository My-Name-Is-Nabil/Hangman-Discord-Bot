def init():
    global gamesmap
    gamesmap={}
    global codesmap
    codesmap={}
    global n
    n=0
    global HANGMAN_PICS
    HANGMAN_PICS=[
    r'''
      +---+
          |
          |
          |
         ===''', r'''
       +---+
       O   |
           |
           |
          ===''', r'''
       +---+
       O   |
       |   |
           |
          ===''', r'''
       +---+
       O   |
      /|   |
           |
          ===''', r'''
       +---+
       O   |
      /|\  |
           |
          ===''', r'''
       +---+
       O   |
      /|\  |
      /    |
          ===''', r'''
       +---+
       O   |
      /|\  |
      / \  |
          ===''']