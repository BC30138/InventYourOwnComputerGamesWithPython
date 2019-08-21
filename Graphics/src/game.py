"""game module"""
import pygame
import random
from pygame.locals import NOFRAME

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'
UPLEFT = 'upleft'
UPRIGHT = 'upright'
MOVESPEED = 1

BOX_1 = {'rect': pygame.Rect(300, 80, 50, 100), 'color': RED, 'dir': UPRIGHT}
BOX_2 = {'rect': pygame.Rect(200, 200, 20, 20), 'color': GREEN, 'dir': UPLEFT}
BOX_3 = {'rect': pygame.Rect(100, 150, 60, 60), 'color': BLACK, 'dir': DOWNLEFT}

class Game():
    """Game module"""
    def __init__(self):
        self.width: int = 600
        self.height: int = 400
        self.window_surface: pygame.Surface = \
            pygame.display.set_mode(size=(self.width, self.height),
                                    flags=NOFRAME,
                                    display=0)
        self.center_x: int = self.window_surface.get_rect().centerx
        self.centet_y: int = self.window_surface.get_rect().centery
        pygame.display.set_caption("Graphics")
        self.font = pygame.font.SysFont(None, 48)
        self.text_rect: pygame.Rect
        self.text: pygame.Surface
        self.boxes = [BOX_1, BOX_2, BOX_3]

    def draw_text_rect(self, text_str: str):
        """Text rendering"""
        self.text = self.font.render(text_str, True, WHITE, BLUE)
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.center_x
        self.text_rect.centery = self.centet_y
        self.window_surface.blit(self.text, self.text_rect)

    def draw_background(self, color):
        """Render background"""
        if not color:
            color = WHITE
        self.window_surface.fill(color)

    def draw_polygon(self, color):
        """draw polygon"""
        if not color:
            color = RED
        pygame.draw.polygon(self.window_surface, color, (
            (self.center_x - 0.02 * self.width, self.centet_y + 0.4 * self.height),
            (self.center_x + 0.02 * self.width, self.centet_y + 0.4 * self.height),
            (self.center_x + 0.02 * self.width, self.centet_y + 0.2 * self.height),
            (self.center_x + 0.15 * self.width, self.centet_y + 0.2 * self.height),
            (self.center_x + 0.15 * self.width, self.centet_y + 0.1 * self.width),
            (self.center_x + 0.02 * self.width, self.centet_y + 0.1 * self.width),
            (self.center_x + 0.02 * self.width, self.centet_y - 0.4 * self.height),
            (self.center_x - 0.02 * self.width, self.centet_y - 0.4 * self.height),
            (self.center_x - 0.02 * self.width, self.centet_y + 0.1 * self.width),
            (self.center_x - 0.15 * self.width, self.centet_y + 0.1 * self.width),
            (self.center_x - 0.15 * self.width, self.centet_y + 0.2 * self.height),
            (self.center_x - 0.02 * self.width, self.centet_y + 0.2 * self.height),
            ), 2)

    def draw_lines(self):
        """draw lines of course"""
        color = (201, 196, 195)
        left = (0.0, 0.01 * self.width)
        right = (0.01 * self.height, 0.0)
        for it in range(120):
            pygame.draw.line(self.window_surface, color, left, right, 3)
            left = (0.0, left[1] + 0.02 * self.width)
            right = (right[0] + 0.02 * self.height, 0.0)

    def draw_circle(self):
        """draw circle"""
        color = (235, 182, 178)
        pygame.draw.circle(self.window_surface, color,
                           (self.center_x, self.centet_y + int(0.15 * self.height)),
                           int(0.1 * self.width), 0)

    def dot_work(self):
        """change one pixel"""
        pix_array = pygame.PixelArray(self.window_surface)
        pix_array[400][133] = BLACK
        pix_array[400][134] = BLACK
        pix_array[400][135] = BLACK

    def move_boxes(self):
        """Moving boxes"""
        for box in self.boxes:
            if box['dir'] == DOWNLEFT:
                box['rect'].left -= MOVESPEED
                box['rect'].top += MOVESPEED
            elif box['dir'] == DOWNRIGHT:
                box['rect'].left += MOVESPEED
                box['rect'].top += MOVESPEED
            elif box['dir'] == UPLEFT:
                box['rect'].left -= MOVESPEED
                box['rect'].top -= MOVESPEED
            else:
                box['rect'].left += MOVESPEED
                box['rect'].top -= MOVESPEED

            if box['rect'].top < 0:
                if box['dir'] == UPLEFT:
                    box['dir'] = DOWNLEFT
                else:
                    box['dir'] = DOWNRIGHT
            elif box['rect'].bottom > self.height:
                if box['dir'] == DOWNLEFT:
                    box['dir'] = UPLEFT
                else:
                    box['dir'] = UPRIGHT
            elif box['rect'].left < 0:
                if box['dir'] == DOWNLEFT:
                    box['dir'] = DOWNRIGHT
                else:
                    box['dir'] = UPRIGHT
            elif box['rect'].right > self.width:
                if box['dir'] == UPRIGHT:
                    box['dir'] = UPLEFT
                else:
                    box['dir'] = DOWNLEFT

            pygame.draw.rect(self.window_surface, box['color'], box['rect'], 2)
