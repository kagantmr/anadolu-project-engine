from constants import *
import random as rnd
from bullet import BulletGroup


def self(args):
    pass


class Enemy(pg.sprite.Sprite):
    def __init__(self, image, shot_type, x, y, x_speed, y_speed, do_shoot=True, do_rotate=False, health=10):
        pg.sprite.Sprite.__init__(self)
        self.orig_image = image
        self.image = self.orig_image.copy()
        self.type = "enemy"
        self.rect = self.image.get_rect()
        self.radius = 10
        self.do_shoot = do_shoot
        self.rect.x = x
        self.rect.y = y
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.shot_time = 100
        self.last = pg.time.get_ticks()
        self.shot_type = shot_type
        self.shots = [
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[0], 2, 100, 200, pattern_amount=1,
                        pattern_spread=0),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[2], 2, 10, 500, pattern_amount=2,
                        pattern_spread=180),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[3], 2, 3, 800, pattern_amount=3,
                        pattern_spread=30),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[4], 3, 3, 800, pattern_amount=6,
                        pattern_spread=60),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[5], 6, 3, 300, pattern_amount=6,
                        pattern_spread=60),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[2], 6, 3, 300, pattern_amount=10,
                        pattern_spread=36),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[6], 4, 5, 200, pattern_amount=5,
                        pattern_spread=72, sound_to_play="throw"),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[6], 4, -5, 200, pattern_amount=5,
                        pattern_spread=72, sound_to_play="throw"),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[7], 6, 1, 150, pattern_amount=4,
                        pattern_spread=90, start_angle=90),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[8], 7, randint(-3, 3), 90,
                        pattern_amount=3, pattern_spread=120, sound_to_play="throw"),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[2], 4, 5, 500, pattern_amount=5,
                        pattern_spread=72),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[3], 2, 5, 1000, pattern_amount=4,
                        pattern_spread=20),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[10], 6, 5, 300, pattern_amount=20,
                        pattern_spread=18),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[7], 2, 5, 600, pattern_amount=10,
                        pattern_spread=36),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[5], 3, 2, 500, pattern_amount=15,
                        pattern_spread=24),
            BulletGroup(self.rect.centerx, self.rect.centery, choice(pointed_bullet_images[0:5]), 3, 2, 500,
                        pattern_amount=6, pattern_spread=60),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[5], 3, 2, 800,
                        pattern_amount=30, pattern_spread=12, do_accel=True),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[12], 1, 2, 400, pattern_spread=20,
                        pattern_amount=18, do_accel=True),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[7], 3, 5, 200, pattern_spread=120,
                        pattern_amount=3),
            BulletGroup(self.rect.centerx, self.rect.centery, choice(pointed_bullet_images[6:9]), 4, 4, 300, pattern_spread=72,
                        pattern_amount=5),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[9], 4, 3, 500,
                        pattern_spread=60, pattern_amount=6),
            BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[2], 0.1, 1, 200,
                        pattern_spread=60, pattern_amount=6, do_accel=True),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[2], 5, 3, 150,
                        pattern_spread=36, pattern_amount=10, do_curve=True),
            BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[4], 2, 3, 600,
                        pattern_spread=24, pattern_amount=15)

        ]
        self.thread = self.shots[self.shot_type]
        self.health = health
        self.do_rotate = do_rotate
        self.last_update = pg.time.get_ticks()
        self.rotation = 0
        self.rotation_speed = 20

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotozoom(self.orig_image, self.rotation, 1).convert_alpha()
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        if self.do_rotate:
            self.rotate()
        self.thread.rect.center = self.rect.center
        if not self.rect.centery > 384 and self.do_shoot:
            self.thread.shoot()
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.top > game_area.bottom + 50 or self.rect.left < -25 or self.rect.right > width + 25:
            self.rect.x = rnd.randrange(-20, width)
            self.rect.y = height + 20
            self.y_speed = rnd.randrange(-10, 10)
        if self.rect.top > game_area.bottom or self.health < 0:
            self.kill()


def spawn_enemy_randomly(image: pg.Surface, shot: int, times: int, health=20):
    for i in range(times):
        e = Enemy(image, shot, rnd.randint(game_area.left, game_area.right), -25, 0, rnd.uniform(1, 5), health=health)
        all_sprites.add(e)
        enemies.add(e)


def spawn_enemy(image: pg.Surface, shot: int, times: int):
    for i in range(times):
        e = Enemy(image, shot, rnd.randint(game_area.left, game_area.right), -25, 0, rnd.uniform(1, 5))
        all_sprites.add(e)
        enemies.add(e)
