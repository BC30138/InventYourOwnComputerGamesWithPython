"""Tools for development"""
import pickle

def save_dictionary():
    """creating dictionaty file with words"""
    words = {}
    words['dev'] = 'cat dog delelopment'.split()
    with open("data/words.txt") as f:
        words['prod'] = []
        for line in f:
            words['prod'].append(line.rstrip())
    with open('data/words.dictionary', 'wb') as dictionary_obj_file:
        pickle.dump(words, dictionary_obj_file)
