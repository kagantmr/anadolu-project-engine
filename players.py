from projectiles_effects_background import *
import time
from constants import *
from sound_engine import play_sound


class PlayerA(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_sprite
        self.image2 = player_sprite_left
        self.image3 = player_sprite_right
        self.rect = self.image.get_rect()
        self.radius = 5
        self.shot_type = "Tones of Natural Flow"
        self.rect.center = (width / 2, height - 20)
        self.x_speed = 0
        self.y_speed = 0
        self.last = pg.time.get_ticks()
        self.last2 = pg.time.get_ticks()
        self.lives = 3
        self.hide = False
        self.power = 0
        self.bombs = 3
        self.bomb_shot = VectoredShotGroup(self.rect.centerx, self.rect.centery, bomb_sprites[0], 1, 1, 2, 8,
                                           pattern_spread=6, pattern_amount=60, bomb=True, speed=6)
        self.last_collision = 0
        self.invincible = False
        self.level = 0
        self.deaths = 0

    def shot_unfocused(self):
        shot_time = pg.time.get_ticks()
        shot_time2 = pg.time.get_ticks()
        if shot_time - self.last > 100:
            self.last = shot_time
            summon_shot(shot2, self.rect.centerx + 10, self.rect.top, 0, -10, 5)
            summon_shot(shot2, self.rect.centerx - 10, self.rect.top, 0, -10, 5)
        if shot_time2 - self.last2 > 150:
            self.last2 = shot_time2
            if 1 <= self.power < 2:
                play_sound("shoot3")
                summon_shot(shot1, self.rect.centerx, self.rect.top, -1, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 1, -10, 4, True)
            if 2 <= self.power < 3:
                play_sound("shoot3")
                summon_shot(shot1, self.rect.centerx, self.rect.top, -1, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 1, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, -3, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 3, -10, 4, True)
            if 3 <= self.power < 4:
                play_sound("shoot3")
                summon_shot(shot1, self.rect.centerx, self.rect.top, -1, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 1, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, -3, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 3, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, -5, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 5, -10, 4, True)
            if self.power == 4:
                play_sound("shoot3")
                summon_shot(shot1, self.rect.left, self.rect.top, 0, -10, 7, True)
                summon_shot(shot1, self.rect.right, self.rect.top, 0, -10, 7, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 1, -10, 7, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, -1, -10, 7, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, -3, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 3, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, -4, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 4, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, -5, -10, 4, True)
                summon_shot(shot1, self.rect.centerx, self.rect.top, 5, -10, 4, True)
            elif self.power > 4.00:
                self.power = 4.00

    def bomb(self):
        if self.bombs > 0:
            self.bomb_shot.rect.center = self.rect.center
            play_sound("explode")
            self.invincible = True
            pg.time.get_ticks()
            screen.blit(bomb_bg, screen.get_rect())
            all_sprites.add(self.bomb_shot)
            clear_bullets()
            self.bomb_shot.shoot()
            self.bombs -= 1

    def immune(self):
        if self.invincible:
            self.image.set_alpha(100)
            self.image2.set_alpha(100)
            self.image3.set_alpha(100)
            now = pg.time.get_ticks()
            if now - self.last_collision > 3000:
                self.invincible = False
        else:
            self.image.set_alpha(255)
            self.image2.set_alpha(255)
            self.image3.set_alpha(255)

    def life_level(self):
        if self.level >= 300:
            self.lives += 1
            play_sound('gain', volume=0.5)
            self.level = 0

    def update(self):
        if self.bombs < 0:
            self.bombs = 0
        self.life_level()
        self.immune()
        if self.hide and pg.time.get_ticks() - 1000:
            self.hide = False
            self.rect.center = (width / 2, 590)
        self.x_speed = 0
        self.y_speed = 0
        key_state = pg.key.get_pressed()
        if key_state[pg.K_z]:
            self.shot_unfocused()
        if key_state[pg.K_LEFT]:
            self.x_speed = -5
        if key_state[pg.K_RIGHT]:
            self.x_speed = 5
        if key_state[pg.K_UP]:
            self.y_speed = -5
        if key_state[pg.K_DOWN]:
            self.y_speed = 5
        if key_state[pg.K_LSHIFT]:
            pg.draw.circle(screen, blue, self.rect.center, self.radius)
            pg.draw.circle(screen, white, self.rect.center, self.radius - 2)
        if key_state[pg.K_LEFT] and key_state[pg.K_LSHIFT]:
            self.x_speed = -2.5
        if key_state[pg.K_RIGHT] and key_state[pg.K_LSHIFT]:
            self.x_speed = 2.5
        if key_state[pg.K_UP] and key_state[pg.K_LSHIFT]:
            self.y_speed = -2.5
        if key_state[pg.K_DOWN] and key_state[pg.K_LSHIFT]:
            self.y_speed = 2.5
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.rect.clamp_ip(game_area)
        if self.x_speed > 0:
            self.image = self.image3
        if self.x_speed < 0:
            self.image = self.image2
        if self.x_speed == 0:
            self.image = player_sprite


class PlayerB(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_sprite
        self.image2 = player_sprite_left
        self.image3 = player_sprite_right
        self.rect = self.image.get_rect()
        self.radius = 5
        self.type = "player"
        self.shot_type = "Blossoming Flower"
        self.rect.center = (width / 2, 590)
        self.x_speed = 0
        self.y_speed = 0
        self.last = pg.time.get_ticks()
        self.last2 = pg.time.get_ticks()
        self.lives = 3
        self.hide = False
        self.power = 0
        self.bombs = 3
        self.level = 0
        self.last_collision = 0
        self.invincible = False
        self.deaths = 0

    def shot_unfocused(self):
        shot_time2 = pg.time.get_ticks()
        if shot_time2 - self.last2 > 100:
            self.last2 = shot_time2
            summon_shot(shot2, self.rect.centerx + 10, self.rect.top, 0, -10, 5)
            summon_shot(shot2, self.rect.centerx - 10, self.rect.top, 0, -10, 5)
        shot_time = pg.time.get_ticks()
        if shot_time - self.last > 200:
            self.last = shot_time
            if 1 <= self.power < 2:
                summon_homing_shot(shot4, self.rect.centerx, self.rect.bottom, 0, 5, 5)
                play_sound("shoot2")
            if 2 <= self.power < 3:
                summon_homing_shot(shot4, self.rect.left - 20, self.rect.bottom, 0, 5, 5)
                summon_homing_shot(shot4, self.rect.right + 20, self.rect.bottom, 0, 5, 5)
                play_sound("shoot2")
            if 3 <= self.power < 4:
                summon_homing_shot(shot4, self.rect.left - 20, self.rect.bottom, 0, 5, 5)
                summon_homing_shot(shot4, self.rect.right + 20, self.rect.bottom, 0, 5, 5)
                summon_homing_shot(shot4, self.rect.centerx, self.rect.top, 0, 5, 5)
                play_sound("shoot2")
            if self.power == 4:
                summon_homing_shot(shot4, self.rect.left - 20, self.rect.bottom, 0, 5, 10)
                summon_homing_shot(shot4, self.rect.right + 20, self.rect.bottom, 0, 5, 10)
                summon_homing_shot(shot4, self.rect.left - 20, self.rect.top, 0, 5, 10)
                summon_homing_shot(shot4, self.rect.right + 20, self.rect.top, 0, 5, 10)
                play_sound("shoot2")
            elif self.power > 4.00:
                self.power = 4.00

    def bomb(self):
        if self.bombs > 0:
            play_sound("explode")
            self.invincible = True
            pg.time.get_ticks()
            screen.blit(bomb_bg, screen.get_rect())
            clear_bullets()
            for i in range(0, 50):
                summon_shot(bomb_sprites[1], randint(0, width),
                            self.rect.centery, 0, randint(-10, -5), 6, do_rotation=True, bomb=True)
                summon_shot(bomb_sprites[1], randint(0, width),
                            self.rect.centery, 0, randint(5, 10), 6, do_rotation=True, bomb=True)
            self.bombs -= 1

    def immune(self):
        if self.invincible:
            self.image.set_alpha(100)
            self.image2.set_alpha(100)
            self.image3.set_alpha(100)
            now = pg.time.get_ticks()
            if now - self.last_collision > 3000:
                self.invincible = False
        else:
            self.image.set_alpha(255)
            self.image2.set_alpha(255)
            self.image3.set_alpha(255)

    def life_level(self):
        if self.level >= 300:
            self.lives += 1
            play_sound('gain', volume=0.5)
            self.level = 0

    def update(self):
        if self.bombs < 0:
            self.bombs = 0
        self.life_level()
        self.immune()
        if self.hide and pg.time.get_ticks() - 1000:
            self.hide = False
            self.rect.center = (width / 2, 590)
        self.x_speed = 0
        self.y_speed = 0
        key_state = pg.key.get_pressed()
        if key_state[pg.K_z]:
            self.shot_unfocused()

        if key_state[pg.K_LEFT]:
            self.x_speed = -7
        if key_state[pg.K_RIGHT]:
            self.x_speed = 7
        if key_state[pg.K_UP]:
            self.y_speed = -7
        if key_state[pg.K_DOWN]:
            self.y_speed = 7
        if key_state[pg.K_LSHIFT]:
            pg.draw.circle(screen, blue, self.rect.center, self.radius)
            pg.draw.circle(screen, white, self.rect.center, self.radius - 2)
        if key_state[pg.K_LEFT] and key_state[pg.K_LSHIFT]:
            self.x_speed = -3.5
        if key_state[pg.K_RIGHT] and key_state[pg.K_LSHIFT]:
            self.x_speed = 3.5
        if key_state[pg.K_UP] and key_state[pg.K_LSHIFT]:
            self.y_speed = -3.5
        if key_state[pg.K_DOWN] and key_state[pg.K_LSHIFT]:
            self.y_speed = 3.5
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.rect.clamp_ip(game_area)
        if self.x_speed > 0:
            self.image = self.image3
        if self.x_speed < 0:
            self.image = self.image2
        if self.x_speed == 0:
            self.image = player_sprite


class PlayerC(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_sprite
        self.image2 = player_sprite_left
        self.image3 = player_sprite_right
        self.rect = self.image.get_rect()
        self.radius = 5
        self.rect.center = (width / 2, 590)
        self.x_speed = 0
        self.y_speed = 0
        self.last = pg.time.get_ticks()
        self.last2 = pg.time.get_ticks()
        self.lives = 3
        self.hide = False
        self.power = 0
        self.hidden = False
        self.time = 0
        self.bombs = 3
        self.last_collision = 0
        self.invincible = False
        self.level = 0
        self.deaths = 0
        self.shot_type = "Protector Flames"

    def shot_unfocused(self):
        shot_time2 = pg.time.get_ticks()
        if shot_time2 - self.last2 > 100:
            self.last2 = shot_time2
            summon_shot(shot2, self.rect.centerx + 10, self.rect.top, 0, -10, 5)
            summon_shot(shot2, self.rect.centerx - 10, self.rect.top, 0, -10, 5)
        shot_time = pg.time.get_ticks()
        if shot_time - self.last > 200:
            self.last = shot_time
            if 0 <= self.power < 1:
                pass
            if 1 <= self.power < 2:
                play_sound("shoot")
                summon_animated_shot(shot3, self.rect.centerx, self.rect.top, 0, -10, 7)
            if 2 <= self.power < 3:
                play_sound("shoot")
                summon_animated_shot(shot3, self.rect.centerx + 20, self.rect.top, 0, -5, 7)
                summon_animated_shot(shot3, self.rect.centerx - 20, self.rect.top, 0, -5, 7)
            if 3 <= self.power < 4:
                play_sound("shoot")
                summon_animated_shot(shot3, self.rect.centerx + 20, self.rect.top, 0, -5, 7)
                summon_animated_shot(shot3, self.rect.centerx - 20, self.rect.top, 0, -5, 7)
                summon_animated_shot(shot3, self.rect.centerx, self.rect.top, 0, -5, 7)
            if self.power == 4:
                play_sound("shoot")
                summon_animated_shot(shot3, self.rect.centerx + 10, self.rect.top, 0, -5, 7)
                summon_animated_shot(shot3, self.rect.centerx - 10, self.rect.top, 0, -5, 7)
                summon_animated_shot(shot3, self.rect.centerx + 30, self.rect.top, 0, -5, 7)
                summon_animated_shot(shot3, self.rect.centerx - 30, self.rect.top, 0, -5, 7)
            elif self.power > 4:
                self.power = 4.00

    def bomb(self):
        if self.bombs > 0:
            play_sound("explode")
            self.invincible = True
            pg.time.get_ticks()
            screen.blit(bomb_bg, screen.get_rect())
            clear_bullets()
            for i in range(0, 25):
                summon_shot(bomb_sprites[2], i * 40, 0, 0, 7, 10, do_rotation=True, bomb=True)
            self.bombs -= 1

    def immune(self):
        if self.invincible:
            self.image.set_alpha(100)
            self.image2.set_alpha(100)
            self.image3.set_alpha(100)
            now = pg.time.get_ticks()
            if now - self.last_collision > 3000:
                self.invincible = False
        else:
            self.image.set_alpha(255)
            self.image2.set_alpha(255)
            self.image3.set_alpha(255)

    def hide(self):
        self.hidden = True
        self.time = time.time()
        self.rect.center = (width / 2, 590)

    def life_level(self):
        if self.level >= 300:
            self.lives += 1
            play_sound('gain', volume=0.5)
            self.level = 0

    def update(self):
        if self.bombs < 0:
            self.bombs = 0
        self.life_level()
        self.immune()
        if self.hide and pg.time.get_ticks() - 1000:
            self.hide = False
            self.rect.center = (width / 2, 590)
        self.x_speed = 0
        self.y_speed = 0
        key_state = pg.key.get_pressed()
        if key_state[pg.K_z]:
            self.shot_unfocused()
        if key_state[pg.K_LEFT]:
            self.x_speed = -4
        if key_state[pg.K_RIGHT]:
            self.x_speed = 4
        if key_state[pg.K_UP]:
            self.y_speed = -4
        if key_state[pg.K_DOWN]:
            self.y_speed = 4
        if key_state[pg.K_LSHIFT]:
            pg.draw.circle(screen, blue, self.rect.center, self.radius)
            pg.draw.circle(screen, white, self.rect.center, self.radius - 2)
        if key_state[pg.K_LEFT] and key_state[pg.K_LSHIFT]:
            self.x_speed = -1.5
        if key_state[pg.K_RIGHT] and key_state[pg.K_LSHIFT]:
            self.x_speed = 1.5
        if key_state[pg.K_UP] and key_state[pg.K_LSHIFT]:
            self.y_speed = -1.5
        if key_state[pg.K_DOWN] and key_state[pg.K_LSHIFT]:
            self.y_speed = 1.5
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.rect.clamp_ip(game_area)
        if self.x_speed > 0:
            self.image = self.image3
        if self.x_speed < 0:
            self.image = self.image2
        if self.x_speed == 0:
            self.image = player_sprite
