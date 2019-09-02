"""game module"""
import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LCTRL, \
                          K_RCTRL, K_q, MOUSEBUTTONUP, \
                          K_LEFT, K_RIGHT, K_UP, K_DOWN, \
                          K_w, K_a, K_s, K_d, K_e
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

WINDOW_WIDTH: int = 600
WINDOW_HEIGHT: int = 400

class _Unit():
    """Parent class for as player, as enemies"""
    def __init__(self, position: tuple, size: int,
                 sprite_name: str, speed: int, frames_num: int,
                 main_sprite_timer: int, collision_frame_num: int,
                 collision_sprite_timer: int):
        self.obj: pygame.Rect = pygame.Rect(position[0],
                                            position[1],
                                            size, size)
        self.size: int = size
        self.speed: int = speed
        self.collision = False

        self.time_it: int = 0

        self.frames_num = frames_num
        self.current_frame: int = 0
        self.main_sprite_timer: int = main_sprite_timer

        self.sprites: list = []
        for sprite_it in range(frames_num):
            sprite = pygame.image.load(sprite_name + "_" + str(sprite_it) + ".png")
            self.sprites.append(pygame.transform.scale(sprite, (size, size)))
        self.sprite = self.sprites[0]

        self.collision_anim_it: int
        self.collision_sprite_timer: int
        self.collision_frame_num: int = collision_frame_num
        self.coll_sprites: list = []
        for col_it in range(collision_frame_num):
            sprite = pygame.image.load(sprite_name + "_collision_" + str(col_it) + ".png")
            self.coll_sprites.append(pygame.transform.scale(sprite, (size, size)))
        if collision_sprite_timer:
            self.collision_sprite_timer = collision_sprite_timer
        else:
            self.collision_sprite_timer = self.main_sprite_timer

    def update_animation(self):
        """Giffy"""
        self.time_it += 1
        if self.time_it >= self.main_sprite_timer:
            self.time_it = 0
            self.current_frame += 1
            if self.current_frame >= self.frames_num:
                self.current_frame = 0
            self.sprite = self.sprites[self.current_frame]

    def set_collision(self):
        """init collision"""
        self.sprite = self.coll_sprites[0]
        self.collision = True
        self.collision_anim_it = 0
        self.time_it = 0

    def animate_collision(self) -> bool:
        """collision animation"""
        self.time_it += 1
        if self.time_it >= self.collision_sprite_timer:
            self.time_it = 0
            self.collision_anim_it += 1
            if self.collision_anim_it >= self.collision_frame_num:
                self.collision_anim_it = 0
                self.collision = False
            else:
                self.sprite = self.coll_sprites[self.collision_anim_it]

    def draw(self):
        """draw unit"""
        # print(self.collision)
        if self.collision:
            self.animate_collision()
        else:
            self.update_animation()


class _Enemy(_Unit):
    """Class represents food"""
    def __init__(self, size: int, sprite_name: str, speed: int = None,
                 position: tuple = None, frames_num: int = 1,
                 main_sprite_timer: int = 1, collision_frame_num: int = 0,
                 collision_sprite_timer: int = None):
        if not position:
            position = (random.randint(0, WINDOW_WIDTH - size),
                        random.randint(0, WINDOW_HEIGHT - size))
        if not speed:
            speed = random.randint(1, 6)
        super().__init__(position=position, size=size,
                         sprite_name=sprite_name, speed=speed,
                         frames_num=frames_num, main_sprite_timer=main_sprite_timer,
                         collision_frame_num=collision_frame_num,
                         collision_sprite_timer=collision_sprite_timer)
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


class _Player(_Unit):
    """Class represents player"""
    def __init__(self, size: int, sprite_name: str,
                 speed: int, frames_num: int = 1,
                 main_sprite_timer: int = 1,
                 collision_frame_num: int = 0,
                 collision_sprite_timer: int = None):
        super().__init__(position=(int(WINDOW_WIDTH / 2),
                                   int(WINDOW_HEIGHT / 2)),
                         size=size, sprite_name=sprite_name, speed=speed,
                         frames_num=frames_num, main_sprite_timer=main_sprite_timer,
                         collision_frame_num=collision_frame_num,
                         collision_sprite_timer=collision_sprite_timer)
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
            self.obj.top = random.randint(0, WINDOW_HEIGHT - self.size)
            self.obj.left = random.randint(0, WINDOW_WIDTH - self.size)

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


class Game():
    """Game module"""
    def __init__(self):
        self.window_surface: pygame.Surface = \
            pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT),
                                    # flags=NOFRAME,
                                    display=0)
        pygame.display.set_caption("Graphics")
        self.center_x: int = self.window_surface.get_rect().centerx
        self.center_y: int = self.window_surface.get_rect().centery

        self.enemy_specs: dict = {
            'size': 30,
            'sprite_name': SPRITES_PATH + "burger",
        }
        enemies_number: int = 10
        self.enemies: list = [_Enemy(**self.enemy_specs)
                              for _ in range(enemies_number)]
        self.enemies_spaun_time: int = 40
        self.spaun_timer: int = 0

        self.player = _Player(size=50,
                              sprite_name=SPRITES_PATH + "firehead",
                              speed=5,
                              frames_num=4,
                              main_sprite_timer=3,
                              collision_frame_num=1,
                              collision_sprite_timer=5)

    def draw_background(self, color):
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
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                self.player.handle_key_down(event.key)
            if event.type == KEYUP:
                self.player.handle_key_up(event.key)
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
                self.enemies.remove(enemy)
                self.player.set_collision()

        self.player.draw()
        self.window_surface.blit(self.player.sprite, self.player.obj)

    def spaun_enemy(self):
        """Spaun new enemy by timer"""
        self.spaun_timer += 1
        if self.spaun_timer >= self.enemies_spaun_time:
            self.spaun_timer = 0
            self.enemies.append(_Enemy(**self.enemy_specs))
