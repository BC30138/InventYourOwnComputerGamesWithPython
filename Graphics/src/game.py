"""game module"""
import sys
import random
from PIL import Image, ImageFilter
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LCTRL, \
                          K_RCTRL, K_q, K_m, MOUSEBUTTONUP, \
                          K_LEFT, K_RIGHT, K_UP, K_DOWN, \
                          K_w, K_a, K_s, K_d, K_e, \
                          FULLSCREEN, RESIZABLE
# from pygame.locals import NOFRAME

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SPRITES_PATH = "data/sprites/"

DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'
UPLEFT = 'upleft'
UPRIGHT = 'upright'

WINDOW_WIDTH: int
WINDOW_HEIGHT: int

def terminate():
    """Quit game"""
    pygame.quit()
    sys.exit()

def draw_text(text: str, font, color, surface, coord: tuple):
    """Draw text"""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = coord
    surface.blit(text_obj, text_rect)

def text_hollow(font, message, fontcolor, basecolor):
    """Hollow font"""
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, basecolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

class _Unit():
    """Parent class for as player, as enemies"""
    def __init__(self, sprites: dict,
                 sprite_set_times: dict,
                 position: tuple, size: int,
                 speed: int):
        self.speed: int = speed

        self.time_it: int = 0
        self.current_frame: int = 0
        self.sprite_set_times = sprite_set_times

        self.sprites: dict = {}

        if size != 1.0:
            for key, sprite_set in sprites.items():
                self.sprites[key] = []
                for sprite in sprite_set:
                    self.sprites[key].append(pygame.transform.rotozoom(sprite, 0, size))
        else:
            self.sprites = sprites

        self.sprite = self.sprites['main'][0]

        self.obj: pygame.Rect = self.sprite.get_rect()
        if not position:
            position = (random.randint(0, WINDOW_WIDTH - self.obj.width),
                        random.randint(0, WINDOW_HEIGHT - self.obj.height))
        self.obj.left = position[0]
        self.obj.top = position[1]

    def update_animation(self, animation_set: str) -> bool:
        """Giffy"""
        self.time_it += 1
        if self.time_it >= self.sprite_set_times[animation_set]:
            self.time_it = 0
            self.current_frame += 1
            if self.current_frame >= len(self.sprites[animation_set]):
                self.current_frame = 0
                return True
            return False
        return False


class _Enemy(_Unit):
    """Class represents food"""
    def __init__(self, sprites: dict,
                 sprite_set_times: dict,
                 position: tuple = None,
                 size: float = 1, speed: int = None):
        if not speed:
            speed = random.randint(1, 6)
        super().__init__(sprites=sprites,
                         sprite_set_times=sprite_set_times,
                         position=position, size=size,
                         speed=speed)
        self.dir = random.choice([DOWNLEFT, DOWNRIGHT, UPLEFT, UPRIGHT])

    def move(self):
        """Enemy movement"""
        if self.dir == DOWNLEFT:
            self.obj.left -= self.speed
            self.obj.top += self.speed
        elif self.dir == DOWNRIGHT:
            self.obj.left += self.speed
            self.obj.top += self.speed
        elif self.dir == UPLEFT:
            self.obj.left -= self.speed
            self.obj.top -= self.speed
        else:
            self.obj.left += self.speed
            self.obj.top -= self.speed

        if self.obj.top < 0:
            if self.dir == UPLEFT:
                self.dir = DOWNLEFT
            else:
                self.dir = DOWNRIGHT
        elif self.obj.bottom > WINDOW_HEIGHT:
            if self.dir == DOWNLEFT:
                self.dir = UPLEFT
            else:
                self.dir = UPRIGHT
        elif self.obj.left < 0:
            if self.dir == DOWNLEFT:
                self.dir = DOWNRIGHT
            else:
                self.dir = UPRIGHT
        elif self.obj.right > WINDOW_WIDTH:
            if self.dir == UPRIGHT:
                self.dir = UPLEFT
            else:
                self.dir = DOWNLEFT

    def draw(self):
        """draw unit"""
        self.update_animation("main")
        self.sprite = self.sprites['main'][self.current_frame]


class _Player(_Unit):
    """Class represents player"""
    def __init__(self, sprites: dict,
                 sprite_set_times: dict,
                 size: int,
                 speed: int):
        super().__init__(sprites=sprites,
                         sprite_set_times=sprite_set_times,
                         position=(int(WINDOW_WIDTH / 2),
                                   int(WINDOW_HEIGHT / 2)),
                         size=size,
                         speed=speed)
        self.collision = False

        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

    def handle_key_down(self, event_key: int):
        """Handle keys that controls player position are downed"""
        if event_key == K_LEFT or event_key == K_a:
            self.move_left = True
            self.move_right = False
        elif event_key == K_RIGHT or event_key == K_d:
            self.move_right = True
            self.move_left = False
        elif event_key == K_DOWN or event_key == K_s:
            self.move_down = True
            self.move_up = False
        elif event_key == K_UP or event_key == K_w:
            self.move_up = True
            self.move_down = False

    def handle_key_up(self, event_key: int):
        """Handle keys that controls player position are upped"""
        if event_key == K_LEFT or event_key == K_a:
            self.move_left = False
        elif event_key == K_RIGHT or event_key == K_d:
            self.move_right = False
        elif event_key == K_DOWN or event_key == K_s:
            self.move_down = False
        elif event_key == K_UP or event_key == K_w:
            self.move_up = False
        elif event_key == K_e:
            self.obj.top = random.randint(0, WINDOW_HEIGHT - self.obj.height)
            self.obj.left = random.randint(0, WINDOW_WIDTH - self.obj.width)

    def move(self):
        """Move player's unit"""
        if self.move_down and self.obj.bottom < WINDOW_HEIGHT:
            self.obj.top += self.speed
        if self.move_up and self.obj.top > 0:
            self.obj.bottom -= self.speed
        if self.move_right and self.obj.right < WINDOW_WIDTH:
            self.obj.right += self.speed
        if self.move_left and self.obj.left > 0:
            self.obj.left -= self.speed

    def set_collision(self):
        """init collision"""
        self.sprite = self.sprites['collision'][0]
        self.collision = True
        self.current_frame = 0
        self.time_it = 0

    def draw(self):
        """draw unit"""
        if self.collision:
            if not self.update_animation('collision'):
                self.sprite = self.sprites['collision'][self.current_frame]
            else:
                self.collision = False
                self.current_frame = 0
        else:
            self.update_animation('main')
            self.sprite = self.sprites['main'][self.current_frame]


class Game():
    """Game module"""
    def __init__(self):
        self.window_surface: pygame.Surface = \
            pygame.display.set_mode(size=(860, 540),
                                    # flags=RESIZABLE,
                                    display=0)

        global WINDOW_WIDTH, WINDOW_HEIGHT
        WINDOW_WIDTH, WINDOW_HEIGHT = self.window_surface.get_size()

        self.fps = 60

        pygame.display.set_caption("Graphics")
        self.center_x: int = self.window_surface.get_rect().centerx
        self.center_y: int = self.window_surface.get_rect().centery

        self.font = pygame.font.Font("data/DoubleFeature20.ttf", 30)

        background = Image.open("data/sprites/background.jpg")\
            .filter(ImageFilter.GaussianBlur(radius=4))
        background = pygame.image.fromstring(background.tobytes("raw", "RGB"),
                                             background.size, "RGB")
        background = pygame.transform.scale(background,
                                            [WINDOW_WIDTH,
                                             WINDOW_HEIGHT])
        self.background = background.convert()

        pygame.mixer.music.load('data/sounds/background.wav')
        pygame.mixer.music.play(-1, 0.0)

        self.pickup_sound = pygame.mixer.Sound('data/sounds/pickup_0.wav')
        self.music_mute = False

        enemy_sprites = {
            'main' : [pygame.image.load(SPRITES_PATH + "burger_0.png")]
        }
        enemy_sprites_time = {
            'main': 1
        }
        self.enemy_specs: dict = {
            'size': 1,
            'sprites': enemy_sprites,
            'sprite_set_times': enemy_sprites_time
        }
        enemies_number: int = 10
        self.enemies_spaun_time: int = 40
        self.spaun_timer: int = 0

        player_sprites = {
            'main' : [pygame.image.load(SPRITES_PATH + "firehead_" + str(it) + ".png")
                      for it in range(4)],
            'collision': [pygame.image.load(SPRITES_PATH + "firehead_collision_0.png")]
        }
        player_sprites_time = {
            'main': 3,
            'collision': 5
        }
        player_specs = {
            'sprites': player_sprites,
            'sprite_set_times': player_sprites_time,
            'size': 1,
            'speed': 5
        }


        self.enemies: list = [_Enemy(**self.enemy_specs)
                              for _ in range(enemies_number)]
        self.player = _Player(**player_specs)

        self.score: int = 0
        self.top_score: int = 0

    def draw_background(self):
        """Render background"""
        self.window_surface.blit(self.background, [0, 0])

    def draw_score(self):
        """Draw score"""
        text = text_hollow(self.font, "Score: " + str(self.score), RED, GREEN)
        rect = text.get_rect()
        rect.center = (WINDOW_WIDTH / 2, 40)
        self.window_surface.blit(text, rect)
        text = text_hollow(self.font, "Top score: " + str(self.top_score), RED, GREEN)
        self.window_surface.blit(text, (10, 50))
        # draw_text("Score: " + str(self.score), self.font,
        #           RED, self.window_surface, (10, 10))

    def draw_background_lines(self, color):
        """Render background"""
        if not color:
            color = WHITE
        self.window_surface.fill(color)

        color = (201, 196, 195)
        left = (0.0, 0.01 * WINDOW_WIDTH)
        right = (0.01 * WINDOW_HEIGHT, 0.0)
        for _ in range(120):
            pygame.draw.line(self.window_surface, color, left, right, 3)
            left = (0.0, left[1] + 0.02 * WINDOW_WIDTH)
            right = (right[0] + 0.02 * WINDOW_HEIGHT, 0.0)

    def draw_logo(self):
        """draw polygon"""
        scale_logo = 0.3
        center_x_logo = 0.93 * WINDOW_WIDTH
        center_y_logo = 0.08 * WINDOW_HEIGHT
        width_logo = WINDOW_WIDTH * scale_logo
        height_logo = WINDOW_HEIGHT * scale_logo

        circle_color = (235, 182, 178)
        pygame.draw.circle(self.window_surface, circle_color,
                           (int(center_x_logo), int(center_y_logo) +
                            int(0.15 * height_logo)),
                           int(0.1 * width_logo), 0)

        cross_color = RED
        pygame.draw.polygon(self.window_surface, cross_color, (
            (center_x_logo - 0.02 * width_logo,
             center_y_logo + 0.4 * height_logo),
            (center_x_logo + 0.02 * width_logo,
             center_y_logo + 0.4 * height_logo),
            (center_x_logo + 0.02 * width_logo,
             center_y_logo + 0.2 * height_logo),
            (center_x_logo + 0.15 * width_logo,
             center_y_logo + 0.2 * height_logo),
            (center_x_logo + 0.15 * width_logo,
             center_y_logo + 0.1 * width_logo),
            (center_x_logo + 0.02 * width_logo,
             center_y_logo + 0.1 * width_logo),
            (center_x_logo + 0.02 * width_logo,
             center_y_logo - 0.2 * height_logo),
            (center_x_logo - 0.02 * width_logo,
             center_y_logo - 0.2 * height_logo),
            (center_x_logo - 0.02 * width_logo,
             center_y_logo + 0.1 * width_logo),
            (center_x_logo - 0.15 * width_logo,
             center_y_logo + 0.1 * width_logo),
            (center_x_logo - 0.15 * width_logo,
             center_y_logo + 0.2 * height_logo),
            (center_x_logo - 0.02 * width_logo,
             center_y_logo + 0.2 * height_logo),
            ), 2)


        font = pygame.font.SysFont(None, int(48 * scale_logo))
        text_rect: pygame.Rect
        text: pygame.Surface

        text = font.render("I am not satanist", True, WHITE, BLUE)
        text_rect = text.get_rect()
        text_rect.centerx = center_x_logo
        text_rect.centery = center_y_logo + 0.05 * height_logo
        self.window_surface.blit(text, text_rect)

    def event_handler(self):
        """Event handler"""
        pressed = pygame.key.get_pressed()
        if (pressed[K_LCTRL] or pressed[K_RCTRL]) and pressed[K_q]:
            terminate()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                self.player.handle_key_down(event.key)
            if event.type == KEYUP:
                self.player.handle_key_up(event.key)
                if event.key == K_m:
                    if self.music_mute:
                        pygame.mixer.music.play(-1, 0.0)
                    else:
                        pygame.mixer.music.stop()
                    self.music_mute = not self.music_mute
            if event.type == MOUSEBUTTONUP:
                self.enemies.append(_Enemy(**self.enemy_specs,
                                           position=event.pos))

    def move_enemies(self):
        """Move enemies"""
        for enemy in self.enemies:
            enemy.move()
            enemy.draw()
            self.window_surface.blit(enemy.sprite, enemy.obj)

    def move_player(self):
        """Move player"""
        self.player.move()

        for enemy in self.enemies:
            if self.player.obj.colliderect(enemy.obj):
                if not self.music_mute:
                    self.pickup_sound.play()
                self.enemies.remove(enemy)
                self.player.set_collision()
                self.score += 1

        self.player.draw()
        self.window_surface.blit(self.player.sprite, self.player.obj)

    def spaun_enemy(self):
        """Spaun new enemy by timer"""
        self.spaun_timer += 1
        if self.spaun_timer >= self.enemies_spaun_time:
            self.spaun_timer = 0
            self.enemies.append(_Enemy(**self.enemy_specs))
