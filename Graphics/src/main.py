"""main module"""
import sys
import pygame
import time
from pygame.locals import QUIT
from game import Game


def main():
    """main func"""
    pygame.init()
    game_object = Game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        game_object.draw_background(None)
        game_object.draw_lines()
        # game_object.dot_work()
        game_object.move_boxes()
        game_object.draw_circle()
        game_object.draw_polygon(None)
        game_object.draw_text_rect("I am not satanist")
        pygame.display.update()
        time.sleep(0.01)

if __name__ == "__main__":
    main()
