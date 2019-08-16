"""main module"""
import sys
import pygame
from pygame.locals import QUIT
from game import Game
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

# pygame.init()
# screen = pygame.display.set_mode((400, 300))
# done = False

# while not done:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#     pygame.display.flip()


def main():
    """main func"""
    pygame.init()
    game_object = Game()
    game_object.draw_text_rect("Fuck")
    game_object.draw_background(None)
    game_object.on_screen()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
