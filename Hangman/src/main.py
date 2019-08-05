"""Main file of game"""
from hangman_main_module import HangmanMainModule

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
