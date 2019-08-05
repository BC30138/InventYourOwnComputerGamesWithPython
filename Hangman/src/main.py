"""Main file of game"""
import pickle

with open('data/words.dictionary', 'rb') as load_obj_file:
    WORDS_LOAD = pickle.load(load_obj_file)

def choose_mode():
    while True:
        choosen_mode = input()
        if choosen_mode == 'PvP':
            mode = 'PvP'

print('''Welcome to
H A N G M A N
This is awesome game, just belive''')
