"""HANGMAN main module"""
import pickle
import random
import os

class HangmanMainModule:
    """main class of game"""
    def __init__(self):
        self.__pve_mode: bool
        self.__secret_word: str
        self.__hangman_state: int = 0
        self.__word_current: str
        self.__game_over: bool
        self.__alredy_guessed: list = []
        self.__hangman_states: list = ['''
 +---+
     |
     |
     |
    ===''', '''
 +---+
 O   |
     |
     |
    ===''', '''
 +---+
 O   |
 |   |
     |
    ===''', '''
 +---+
 O   |
/|\\  |
     |
    ===''', '''
 +---+
 O   |
/|\\  |
/    |
    ===''', '''
 +---+
 O   |
/|\\  |
/ \\  |
    ===''']

    def choose_mode(self):
        """choose mode: PvP or PvE"""
        while True:
            print('Choose mode (PvP or PvE):', end=' ')
            choosen_mode: str = input().lower().rstrip()
            if choosen_mode == 'pvp':
                self.__pve_mode = False
                while True:
                    print("Type secret word:", end=' ')
                    secret_word: str = input().lower()
                    if secret_word.isalpha():
                        break
                    print("Word shouldn't contain numbers or symbols")
                self.__secret_word = secret_word
                break
            if choosen_mode == 'pve':
                self.__pve_mode = True
                with open('data/words.dictionary', 'rb') as load_obj_file:
                    dictionary: dict = pickle.load(load_obj_file)
                    self.__secret_word = random.choice(dictionary['prod'])
                break
            print('Try again, mode should be "PvE" or "PvP"')
        self.__word_current = '_' * len(self.__secret_word)
        self.update_screen()

    def guess_letter(self):
        """Player guessing the letter"""
        def fail():
            self.__hangman_state += 1
            self.update_screen()
            return False
        while True:
            print("Guess the letter of the secret word: ", end=' ')
            guess: str = input().lower()
            if len(guess) != 1:
                print('Please enter a single letter!')
            elif not guess.isalpha():
                print('Please enter a letter, not number or symbol')
            else: break
        for it, _ in enumerate(self.__secret_word):
            if guess == self.__secret_word[it]:
                if it not in self.__alredy_guessed:
                    self.__alredy_guessed.append(it)
                    self.__word_current = self.__word_current[:it] + guess + self.__word_current[it + 1:]
                    self.update_screen()
                    return True
        return fail()

    def check_end(self):
        """Check if this is the end of game"""
        if len(self.__alredy_guessed) == len(self.__secret_word):
            print('Congratulations! You won!')
            return True
        if self.__hangman_state == len(self.__hangman_states) - 1:
            print('Sorry, you lose!')
            print('Secret word:', end=' ')
            print(self.__secret_word)
            return True
        return False

    def update_screen(self):
        """Clearing console, typing name of game, draw status of hangman"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("H A N G M A N")
        print(self.__hangman_states[self.__hangman_state])
        print("Current state of word: ", end=' ')
        print(' '.join(self.__word_current))

    def try_again(self):
        """Try again?"""
        while True:
            print('Try again? (yes or no):', end=' ')
            answer: str = input().lower().rstrip()
            if answer == 'y' or answer == 'yes':
                return True
            elif answer == 'n' or answer == 'no':
                return False
            else:
                print('YES OF F** NO!!!')

    def start_screen(self):
        """Run start screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print('''Welcome to
H A N G M A N
This is awesome game, just belive me''')

    def show_properties(self):
        """Show all properties of object"""
        print('\n'.join("%s: %s" % item for item in vars(self).items()))
