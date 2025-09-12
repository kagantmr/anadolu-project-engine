from pygame.math import Vector2
from sound_engine import play_sound
from constants import *
from random import uniform


def decide_rotation(image: pg.Surface, vector: Vector2) -> pg.Surface:
    """
    Decides the rotation of a bullet image based on its vector angle.
    """
    if image in circular_bullet_images:
        return image
    else:
        angle = int(vector.as_polar()[1])
        return pg.transform.rotozoom(image, -angle - 90, 1).convert_alpha()


class Bullet(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, speed: float, x: float, y: float, angle: float,
                 do_rotate: bool = False, do_accel: bool = False, do_curve: bool = False, curve: float = 0.25) -> None:
        """
        Projectile class used by bullet generator.
        """
        pg.sprite.Sprite.__init__(self)  # Initializes sprite class.
        self.angle = angle
        self.x_speed = 5
        self.y_speed = 5
        self.orig_image = image
        self.velocity = Vector2(1, 0).rotate(angle) * speed
        self.image = decide_rotation(image, self.velocity)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.radius = self.orig_image.get_rect().width * .40  # hitbox
        self.pos = Vector2(self.rect.center)
        self.do_rotate = do_rotate
        self.last_update = pg.time.get_ticks()
        self.last_curve = pg.time.get_ticks()
        self.last_accel = pg.time.get_ticks()
        self.rotation = 0
        self.rotation_speed = 0
        self.do_curve = do_curve
        self.curve_amount = curve
        self.do_accel = do_accel
        self.constant_speed = speed
        self.accel_amount = 0.05
        self.home_once = 0
        self.desired = 5

    def curve(self):
        if self.do_curve:
            if pg.time.get_ticks() - self.last_curve > 10:
                self.last_curve = pg.time.get_ticks()
                self.velocity.rotate_ip(self.curve_amount)

    def accel(self):
        if self.do_accel:
            if pg.time.get_ticks() - self.last_accel > 10:
                self.constant_speed += self.accel_amount
                self.velocity.scale_to_length(self.constant_speed)

    def rotate(self) -> None:
        """
        Basic rotation function.
        """
        now = pg.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.orig_image, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self) -> None:
        """
        Updates the sprite.
        """
        # pg.draw.circle(screen, red, self.rect.center, self.radius)
        self.accel()
        self.curve()
        if self.do_rotate:
            self.rotate()
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom or \
                self.rect.bottom < game_area.top:
            self.kill()
        self.pos += self.velocity
        self.rect.center = self.pos


class BulletGroup(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, bulletImage: pg.Surface, speed: float, angleIncrease: float,
                 fire_rate: int = 100, start_angle: int = 0, pattern_amount: int = 1, pattern_spread: int = 1,
                 sound_to_play: str = "pop", do_random: bool = False, do_curve: bool = False, curve: float = 0.25,
                 do_accel: bool = False, do_rotate: bool = False) -> None:
        """
        Bullet spawner class.
        """
        pg.sprite.Sprite.__init__(self)
        self.image = load_image(0, 0, projectile_folder, 'mask')
        self.rect = self.image.get_rect()
        self.bullet_image = bulletImage
        self.speed = speed
        self.rect.center = (x, y)
        self.increase = angleIncrease
        self.start_angle = start_angle
        self.last = pg.time.get_ticks()
        self.fire_rate = fire_rate
        self.angle = 0
        self.pattern_amount = pattern_amount
        self.pattern_spread = pattern_spread
        self.sound = sound_to_play
        self.do_curve = do_curve
        self.do_accel = do_accel
        self.curve = curve
        self.do_random = do_random
        self.do_rotate = do_rotate

    def update(self) -> None:
        if self.rect.right > width or self.rect.left < 0 or self.rect.bottom > height or self.rect.top < 0:
            self.kill()

    def shoot(self) -> None:
        """
        Shoots the bullets.
        """
        if pg.time.get_ticks() - self.last > self.fire_rate:
            self.last = pg.time.get_ticks()  # Set time
            for i in range(self.pattern_amount):
                if self.do_random:
                    bullet = Bullet(self.bullet_image, self.speed, self.rect.centerx, self.rect.centery,
                                    uniform(0, 360), do_rotate=self.do_rotate, do_accel=self.do_accel, do_curve=self.do_curve,
                                    curve=self.curve)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

                else:
                    bullet = Bullet(self.bullet_image, self.speed, self.rect.centerx, self.rect.centery,
                                    self.angle, do_rotate=self.do_rotate, do_accel=self.do_accel, do_curve=self.do_curve,
                                    curve=self.curve)
                    self.angle += self.pattern_spread
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    self.angle += self.increase
            play_sound(self.sound)  # Plays a sound
