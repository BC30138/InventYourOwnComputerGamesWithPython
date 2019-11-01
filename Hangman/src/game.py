"""Main file of game"""
from pynput.keyboard import Key, Listener, KeyCode
from hangman_main_module import HangmanMainModule
from tools import y_or_n

CURRENT_INPUT = set()
QUIT_COMBINATION: list = [{Key.ctrl, KeyCode(char='q')},
                          {Key.ctrl_l, KeyCode(char='q')},
                          {Key.ctrl_r, KeyCode(char='q')}]

def on_press(key: Key):
    """Activity on press hotkey"""
    if any(key in comb for comb in QUIT_COMBINATION):
        CURRENT_INPUT.add(key)
        if any(all(k in CURRENT_INPUT for k in comb) for comb in QUIT_COMBINATION):
            if y_or_n('You sure, that you want to quit?'):
                quit()

def on_release(key: Key):
    """Activity on release hotkey"""
    try:
        CURRENT_INPUT.remove(key)
    except KeyError:
        pass

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    # listener.join()
    TRY_AGAIN = True
    while TRY_AGAIN:
        GAME_OBJECT = HangmanMainModule()
        GAME_OBJECT.start_screen()
        GAME_OBJECT.choose_mode()
        GAME_END = False
        while not GAME_END:
            GAME_OBJECT.guess_letter()
            GAME_END = GAME_OBJECT.check_end()
        TRY_AGAIN = GAME_OBJECT.try_again()
    #
