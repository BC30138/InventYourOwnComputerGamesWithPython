"""Tools for development"""
import pickle
import platform
import subprocess

def save_dictionary():
    """creating dictionaty file with words"""
    words = {}
    words['dev'] = 'cat dog development'.split()
    with open("data/words.txt") as f:
        words['prod'] = []
        for line in f:
            words['prod'].append(line.rstrip())
    with open('data/words.dictionary', 'wb') as dictionary_obj_file:
        pickle.dump(words, dictionary_obj_file)

def open_new_window(filename: str):
    """Open program in new window"""
    system = platform.system()
    if system == "Linux":
        subprocess.call(['gnome-terminal', '--', 'python3', filename])
    elif system == "Darwin":
        subprocess.call(['open', '-W', '-a', 'Terminal.app', 'python3', '--args', filename])
    elif system == "Windows":
        subprocess.call('start /wait python3 ' + filename, shell=True)
    else: print("Required OS: Linux (with gnome-terminal), Windows or OSX")
