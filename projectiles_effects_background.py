import math

from pygame.math import Vector2

from constants import *
from sound_engine import play_sound


class Background:
    def __init__(self, image, speed):
        self.background_image = image
        self.rect = self.background_image.get_rect()

        self.bgY1 = 0
        self.bgX1 = game_area.left

        self.bgY2 = self.rect.height
        self.bgX2 = game_area.left

        self.movingUpSpeed = speed

    def update(self):
        self.render()
        self.bgY1 += self.movingUpSpeed
        self.bgY2 += self.movingUpSpeed
        if self.bgY1 <= -self.rect.height:
            self.bgY1 = self.rect.height
        if self.bgY2 <= -self.rect.height:
            self.bgY2 = self.rect.height

    def render(self):
        screen.blit(self.background_image, (self.bgX1, -self.bgY1))
        screen.blit(self.background_image, (self.bgX2, -self.bgY2))


class HBackground:
    def __init__(self, image, speed):
        self.background_image = image
        self.rect = self.background_image.get_rect()

        self.bgY1 = 0
        self.bgX1 = game_area.left

        self.bgX2 = self.rect.height
        self.bgY2 = game_area.left

        self.movingUpSpeed = speed

    def update(self):
        self.render()
        self.bgX1 += self.movingUpSpeed
        self.bgX2 += self.movingUpSpeed
        if self.bgX1 <= -self.rect.height:
            self.bgX1 = self.rect.height
        if self.bgX2 <= -self.rect.height:
            self.bgX2 = self.rect.height

    def render(self):
        screen.blit(self.background_image, (self.bgX1, -self.bgY1))
        screen.blit(self.background_image, (self.bgX2, -self.bgY2))


class CoverImage(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = cover


class HomingShot(pg.sprite.Sprite):
    def __init__(self, image, x, y, x_speed_arg, y_speed_arg, damage, doRotation=False):
        pg.sprite.Sprite.__init__(self)
        self.last_update2 = pg.time.get_ticks()
        self.y_speed = y_speed_arg
        self.x_speed = x_speed_arg
        self.orig_image = image
        self.image = pg.transform.rotozoom(self.orig_image.copy(), 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = Vector2(self.rect.center)
        self.velocity = Vector2(5, 0).rotate(-90)
        self.damage = damage
        self.doRotation = doRotation
        self.angle = 1
        self.rotation = 0
        self.rotation_speed = 2
        self.last_update = pg.time.get_ticks()
        self.desired = 0
        self.count = 0

    def seek(self, target: Vector2):
        self.desired = (target - self.pos).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 5:
            steer.scale_to_length(5)
        return steer

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.orig_image, self.rotation).convert_alpha()
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        if self.count == 0:
            for sprite in all_sprites:
                if sprite in enemies or hasattr(sprite, 'is_boss'):
                    self.velocity += self.seek(Vector2(sprite.rect.center))
                    self.count += 1
        self.rect.center = self.pos
        self.pos += self.velocity
        if self.doRotation:
            self.rotate()
        now2 = pg.time.get_ticks()
        if now2 - self.last_update2 > 1000:
            self.last_update = now2

        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom or \
                self.rect.bottom < game_area.top:
            self.kill()


class Shot(pg.sprite.Sprite):
    def __init__(self, image, x, y, x_speed_arg, y_speed_arg, damage, doRotation=False):
        pg.sprite.Sprite.__init__(self)
        self.last_update2 = pg.time.get_ticks()
        self.y_speed = y_speed_arg
        self.x_speed = x_speed_arg
        self.orig_image = image
        self.image = pg.transform.rotozoom(self.orig_image.copy(), 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.damage = damage
        self.doRotation = doRotation
        self.angle = 1
        self.rotation = 0
        self.rotation_speed = 2
        self.last_update = pg.time.get_ticks()
        self.desired = 0

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.orig_image, self.rotation).convert_alpha()
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        if self.doRotation:
            self.rotate()
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom or \
                self.rect.bottom < game_area.top:
            self.kill()


class AnimatedShot(pg.sprite.Sprite):
    def __init__(self, images, x, y, x_speed_arg, y_speed_arg, damage):
        pg.sprite.Sprite.__init__(self)
        self.y_speed = y_speed_arg
        self.x_speed = x_speed_arg
        self.images = images
        self.index = 0
        self.index_timer = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.damage = damage
        self.angle = 1
        self.rotation = 0
        self.rotation_speed = 2
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.index_timer += 1
        if self.index_timer % 10 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom or \
                self.rect.bottom < game_area.top:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.images = explosion_sprite
        self.index = 0
        self.index_timer = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.angle = 1
        self.rotation = 0
        self.rotation_speed = 2
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.index_timer += 1
        if self.index_timer % 5 == 0:
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
            self.kill()
        self.image = self.images[self.index]
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom or \
                self.rect.bottom < game_area.top:
            self.kill()


class VectoredShot(pg.sprite.Sprite):
    def __init__(self, image, x_speed, y_speed, x, y, angle, damage, speed=5, do_home=False):
        pg.sprite.Sprite.__init__(self)
        self.angle = angle
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.orig_image = image
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = pg.math.Vector2(1, 0).rotate(angle) * speed
        self.pos = pg.math.Vector2(self.rect.center)
        self.rotation = 0
        self.rotation_speed = 2
        self.last_update = pg.time.get_ticks()
        self.last_update2 = pg.time.get_ticks()
        self.damage = damage
        self.jump_counter = 0
        self.desired = 0
        self.do_home = do_home

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pg.transform.rotate(self.orig_image, self.rotation).convert_alpha()
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.x_speed * math.cos(math.radians(self.angle))
        self.rect.y += self.y_speed * math.sin(math.radians(self.angle))
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom or \
                self.rect.bottom < game_area.top:
            self.kill()

        self.pos += self.velocity
        self.rect.center = self.pos


class VectoredShotGroup(pg.sprite.Sprite):
    def __init__(self, x, y, bulletImage, x_speed, y_speed, angleIncrease, damage, fire_rate=100, start_angle=0,
                 pattern_amount=1, pattern_spread=1, bomb=False, speed=5, do_home=False):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image(0, 0, projectile_folder, 'mask')
        self.rect = self.image.get_rect()
        self.bullet_image = bulletImage
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rect.center = (x, y)
        self.increase = angleIncrease
        self.start_angle = start_angle
        self.last = pg.time.get_ticks()
        self.fire_rate = fire_rate
        self.angle = 0
        self.pattern_amount = pattern_amount
        self.pattern_spread = pattern_spread
        self.damage = damage
        self.is_bomb = bomb
        self.speed = speed
        self.do_home = do_home

    def update(self):
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom or \
                self.rect.bottom < game_area.top:
            self.kill()

    def shoot(self):
        if pg.time.get_ticks() - self.last > self.fire_rate:
            self.last = pg.time.get_ticks()
            play_sound("shoot2")
            for i in range(self.pattern_amount):

                bullet = VectoredShot(self.bullet_image, self.x_speed, self.y_speed, self.rect.centerx,
                                      self.rect.centery, self.angle, self.damage, speed=self.speed,
                                      do_home=self.do_home)
                self.angle += self.pattern_spread

                all_sprites.add(bullet)
                if self.is_bomb:
                    bomb_shots.add(bullet)
                else:
                    shots.add(bullet)
                self.angle += self.increase


class PowerItem(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.image = item_sprites[0]
        self.type = "power"
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = -3
        self.radius = 10

    def update(self):
        if self.speedy < 3:
            self.speedy += 0.1
        self.rect.y += self.speedy
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom:
            self.kill()


class PointItem(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.image = item_sprites[1]
        self.type = "point"
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = -3
        self.radius = 10

    def update(self):
        if self.speedy < 3:
            self.speedy += 0.1
        self.rect.y += self.speedy
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom:
            self.kill()


class BombItem(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.image = item_sprites[4]
        self.type = "bomb"
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = -3
        self.radius = 10

    def update(self):
        if self.speedy < 3:
            self.speedy += 0.1
        self.rect.y += self.speedy
        if self.rect.left > game_area.right or self.rect.right < game_area.left or self.rect.top > game_area.bottom:
            self.kill()


def summon_shot(image, x, y, x_speed_arg, y_speed_arg, damage, do_rotation=False, bomb=False):
    shot = Shot(image, x, y, x_speed_arg, y_speed_arg, damage, do_rotation)
    all_sprites.add(shot)
    if bomb:
        bomb_shots.add(shot)
    else:
        shots.add(shot)


def summon_homing_shot(image, x, y, x_speed_arg, y_speed_arg, damage, do_rotation=False, bomb=False):
    shot = HomingShot(image, x, y, x_speed_arg, y_speed_arg, damage, do_rotation)
    all_sprites.add(shot)
    if bomb:
        bomb_shots.add(shot)
    else:
        shots.add(shot)


def summon_animated_shot(images, x, y, x_speed_arg, y_speed_arg, damage):
    shot = AnimatedShot(images, x, y, x_speed_arg, y_speed_arg, damage)
    all_sprites.add(shot)
    shots.add(shot)


def summon_explosion(center):
    explosion = Explosion(center)
    all_sprites.add(explosion)


def draw_centered_text(surface, text, center, font=font_1):
    text_surface = font.render(text, True, white).convert_alpha()
    text_rect = text_surface.get_rect()
    text_rect.center = center
    surface.blit(text_surface, text_rect)


def draw_text(surface, text, center, font=font_1):
    text_surface = font.render(text, True, white).convert_alpha()
    text_rect = text_surface.get_rect()
    text_rect.topleft = center
    surface.blit(text_surface, text_rect)


def draw_lives_bombs(surface, x, y, stats, image):
    for i in range(stats):
        image_rect = image.get_rect()
        image_rect.topleft = x + 15 * i, y
        surface.blit(image, image_rect)


def fade_in():
    fading = pg.Surface((width, height))
    fading.fill(black)
    for alpha in range(0, 300, 2):
        fading.set_alpha(alpha)
        screen.blit(fading, screen.get_rect())
        pg.display.update()
        pg.time.delay(10)


def spawn_item(center, type_of_item, amount=1):
    if type_of_item == 0:
        for _ in range(amount):
            item = PowerItem(center)
            items.add(item)
            all_sprites.add(item)
    if type_of_item == 1:
        for _ in range(amount):
            item = PointItem(center)
            items.add(item)
            all_sprites.add(item)
    if type_of_item == 2:
        for _ in range(amount):
            item = BombItem(center)
            items.add(item)
            all_sprites.add(item)


def clear_bullets():
    for bullet in bullets:
        bullet.kill()


def clear_sprites():
    for sprite in all_sprites:
        sprite.kill()


def clear_enemies():
    for sprite in enemies:
        summon_explosion(sprite.rect.center)
        sprite.kill()


def draw_long_text(surface, text, topleft: tuple, rect, aa=False, bkg=None, color=white):
    x, y = topleft
    line_spacing = -2
    font = font_4
    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg).convert_alpha()
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color).convert_alpha()

        surface.blit(image, (x, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text
