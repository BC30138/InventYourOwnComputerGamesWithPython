"""game module"""
import pygame
from pygame.locals import NOFRAME, RESIZABLE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Game():
    """Game module"""
    def __init__(self):
        self.window_surface: pygame.Surface = \
            pygame.display.set_mode(size=(600, 400),
                                    flags=NOFRAME|RESIZABLE,
                                    display=0)
        pygame.display.set_caption("Graphics")
        self.font = pygame.font.SysFont(None, 48)
        self.text_rect: pygame.Rect
        self.text: pygame.Surface

    def draw_text_rect(self, text_str: str):
        """Text rendering"""
        self.text = self.font.render(text_str, True, WHITE, BLUE)
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.window_surface.get_rect().centerx
        self.text_rect.centery = self.window_surface.get_rect().centery

    def draw_background(self, color):
        """Render background"""
        if color is None:
            color = WHITE
        self.window_surface.fill(color)

    def on_screen(self):
        """necessary"""
        self.window_surface.blit(self.text, self.text_rect)
        pygame.display.update()
