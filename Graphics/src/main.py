"""main module"""
import pygame
from game import Game

def main():
    """main func"""
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    main_clock = pygame.time.Clock()
    game_object = Game()
    while True:
        game_object.event_handler()
        game_object.draw_background()
        game_object.spaun_enemy()
        game_object.move_player()
        game_object.move_enemies()
        game_object.draw_score()
        pygame.display.update()
        main_clock.tick(30)

if __name__ == "__main__":
    main()
