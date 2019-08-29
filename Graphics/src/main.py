"""main module"""
import pygame
from game import Game

def main():
    """main func"""
    pygame.init()
    main_clock = pygame.time.Clock()
    game_object = Game()
    while True:
        game_object.event_handler()
        game_object.draw_background(None)
        game_object.spaun_enemy()
        game_object.move_player()
        game_object.move_enemies()
        game_object.draw_logo()
        pygame.display.update()
        main_clock.tick(30)

if __name__ == "__main__":
    main()
