from pygame.math import Vector2
from bullet import BulletGroup
from constants import *
from projectiles_effects_background import draw_lives_bombs, spawn_item, clear_bullets, draw_text
from sound_engine import play_sound


class Midboss(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = boss1[0]
        self.attack_image = boss1[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .40 / 2)
        self.rect.x = game_area.centerx - self.rect.width / 2
        self.rect.y = -150
        self.last = pg.time.get_ticks()
        self.health = 800
        self.attacking = False
        self.is_boss = True
        self.velocity = Vector2(0, 1)
        self.position = Vector2(self.rect.center)
        self.movement_delay = 1000
        self.last_movement = pg.time.get_ticks()
        self.frequency = 6000
        self.timeout = 1500
        self.offset = 100
        self.acceleration = Vector2(0, 1)
        self.desired = Vector2(0, 0)
        self.target = randint(100 + game_area.left, game_area.right), randint(100 + game_area.top, int(game_area.bottom / 2))
        self.last_target = 0
        self.moving = False
        self.thread = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[0], 5, 3, fire_rate=200,
                                  pattern_amount=3, pattern_spread=120)
        self.thread2 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[3], 2, 5, fire_rate=800,
                                   pattern_amount=10, pattern_spread=36)
        self.count = 0

    def wander(self):
        if pg.time.get_ticks() - self.last_target > self.frequency:
            self.last_target = pg.time.get_ticks()
            self.target = Vector2(randint(100 + game_area.left, game_area.right),
                                  randint(100 + game_area.top, int(game_area.bottom / 2)))
        return self.seek(self.target)

    def seek(self, target: Vector2):
        self.desired = (target - self.position).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 1:
            steer.scale_to_length(1)
        return steer

    def attack(self):
        if self.health > 0:
            self.thread.shoot()
            self.thread2.shoot()
        self.thread.rect.center = self.rect.centerx, self.rect.centery
        self.thread2.rect.center = determine_center(self)

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, green, self.position, (self.position + self.velocity * scale), 5)
        pg.draw.circle(screen, blue, (int(self.target[0]), int(self.target[1])), 8)

    def update(self):
        self.timeout -= 1
        if self.timeout < 0:
            self.health = self.timeout
        if self.health > 0:
            draw_text(screen, str(self.timeout), (737, 23))
            draw_lives_bombs(screen, game_area.x + 3, 25, int(self.health / 800 * 35), stat_images[3])
        if not self.rect.collidepoint(self.target) and self.health > 0:
            self.velocity += self.wander()
            self.position += self.velocity
            self.image = boss1[0]
        elif self.rect.collidepoint(self.target):
            self.wander()
            self.image = boss1[1]
        elif self.health <= 0:
            if self.count == 0 and self.timeout > 0:
                for i in range(10):
                    spawn_item(determine_center(self), 0)
                    spawn_item(determine_center(self), 1)
                spawn_item(self.rect.center, 2, amount=1)
                self.count += 1
            self.health -= 1
            self.velocity += self.seek(Vector2(width / 2, -150))
            self.position += self.velocity
            if self.rect.collidepoint(width / 2, -150):
                self.kill()
        self.rect.clamp_ip(game_area)
        self.rect.center = self.position
        if self.velocity.length() > 2:
            self.velocity.scale_to_length(2)
        self.attack()


class Boss(pg.sprite.Sprite):
    def __init__(self, attack_state):
        pg.sprite.Sprite.__init__(self)
        self.image = boss1[0]
        self.attack_image = boss1[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .40 / 2)
        self.rect.x = game_area.centerx - self.rect.width / 2
        self.rect.y = game_area.height / 4
        self.last = pg.time.get_ticks()
        self.health = 4000
        self.attack_state = attack_state
        self.is_boss = True
        self.velocity = Vector2(0, 1)
        self.position = Vector2(self.rect.center)
        self.movement_delay = 1000
        self.last_movement = pg.time.get_ticks()
        self.frequency = 6000
        self.offset = 100
        self.acceleration = Vector2(0, 1)
        self.desired = Vector2(0, 0)
        self.target = randint(100 + game_area.left, game_area.right), randint(100 + game_area.top, int(game_area.bottom / 2))
        self.last_target = 0
        self.moving = False
        self.thread = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[2], 5, 3, fire_rate=200,
                                  pattern_amount=8, pattern_spread=45)
        self.thread2 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[1], 3, 5, fire_rate=800,
                                   pattern_amount=30, pattern_spread=12)
        self.thread3 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[2], 4, 3, fire_rate=200,
                                   pattern_amount=10, pattern_spread=36)
        self.thread4 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 2, 1, fire_rate=500,
                                   pattern_amount=8, pattern_spread=45)
        self.count = 0
        self.do_once = 0

    def wander(self):
        if pg.time.get_ticks() - self.last_target > self.frequency:
            self.last_target = pg.time.get_ticks()
            self.target = Vector2(randint(100 + game_area.left, game_area.right),
                                  randint(100 + game_area.top, int(game_area.bottom / 2)))
        return self.seek(self.target)

    def seek(self, target: Vector2):
        self.desired = (target - self.position).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 1:
            steer.scale_to_length(1)
        return steer

    def attack(self):
        if 4000 >= self.health > 2000:
            self.thread.shoot()
            self.thread2.shoot()
        elif 2000 >= self.health > 1000:
            self.thread.shoot()
            self.thread3.shoot()
        elif 1000 >= self.health > 0:
            self.thread3.shoot()
            self.thread4.shoot()
        self.thread.rect.center = self.rect.centerx, self.rect.centery
        self.thread2.rect.center = self.rect.centerx, self.rect.centery
        self.thread3.rect.center = self.rect.centerx, self.rect.centery
        self.thread4.rect.center = self.rect.centerx, self.rect.centery

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, green, self.position, (self.position + self.velocity * scale), 5)
        pg.draw.circle(screen, blue, (int(self.target[0]), int(self.target[1])), 8)

    def update(self):
        if self.health > 0:
            draw_lives_bombs(screen, game_area.x + 3, 25, int(self.health / 4000 * 40), stat_images[3])
        if self.attack_state:
            if not self.rect.collidepoint(self.target) and self.health > 0:
                self.velocity += self.wander()
                self.position += self.velocity
                self.image = boss1[0]
            elif self.rect.collidepoint(self.target):
                self.wander()
                if self.health > 0:
                    self.attack()
                self.image = boss1[1]
            if self.health <= 0:

                if self.do_once == 0:
                    clear_bullets()
                    play_sound('bossdeath', volume=3)
                    self.kill()
                    self.do_once += 1

        self.rect.clamp_ip(game_area)
        self.rect.center = self.position
        if self.velocity.length() > 2:
            self.velocity.scale_to_length(2)


class Boss2(pg.sprite.Sprite):
    def __init__(self, attack_state):
        pg.sprite.Sprite.__init__(self)
        self.image = boss2[0]
        self.attack_image = boss2[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .40 / 2)
        self.rect.x = game_area.centerx - self.rect.width / 2
        self.rect.y = game_area.height / 4
        self.last = pg.time.get_ticks()
        self.health = 5000
        self.attack_state = attack_state
        self.is_boss = True
        self.velocity = Vector2(0, 1)
        self.position = Vector2(self.rect.center)
        self.movement_delay = 1000
        self.last_movement = pg.time.get_ticks()
        self.frequency = 8000
        self.offset = 100
        self.acceleration = Vector2(0, 1)
        self.desired = Vector2(0, 0)
        self.target = randint(100 + game_area.left, game_area.right), randint(100 + game_area.top, int(game_area.bottom / 2))
        self.last_target = 0
        self.moving = False
        self.thread = BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[12], 3, 3, fire_rate=100,
                                  pattern_amount=9, pattern_spread=40, do_random=True, do_accel=True)
        self.thread.accel_amount = 0.5
        self.thread2 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[9], 5, 5, fire_rate=1200,
                                   pattern_amount=20, pattern_spread=18)
        self.thread3 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[2], 3, -5, fire_rate=200,
                                   pattern_amount=10, pattern_spread=36)
        self.thread4 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 2, 1, fire_rate=500,
                                   pattern_amount=8, pattern_spread=45)
        self.thread5 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[7], 4, 2, fire_rate=100,
                                   pattern_amount=6, pattern_spread=60, do_random=True, do_accel=True)
        self.thread6 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 3, 5, fire_rate=500,
                                   pattern_amount=8, pattern_spread=45)
        self.count = 0
        self.do_once = 0

    def wander(self):
        if pg.time.get_ticks() - self.last_target > self.frequency:
            self.last_target = pg.time.get_ticks()
            self.target = Vector2(randint(100 + game_area.left, game_area.right),
                                  randint(100 + game_area.top, int(game_area.bottom / 2)))
        return self.seek(self.target)

    def seek(self, target: Vector2):
        self.desired = (target - self.position).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 1:
            steer.scale_to_length(1)
        return steer

    def attack(self):
        if 5000 >= self.health > 3750:
            self.thread.shoot()
            self.thread2.shoot()
        elif 3750 >= self.health > 2500:
            self.thread2.shoot()
            self.thread3.shoot()
        elif 2500 >= self.health > 1250:
            self.thread2.shoot()
            self.thread4.shoot()
        elif 1250 >= self.health > 0:
            self.thread5.shoot()
            self.thread6.shoot()
        self.thread.rect.center = self.rect.centerx, self.rect.centery
        self.thread2.rect.center = self.rect.centerx, self.rect.centery
        self.thread3.rect.center = self.rect.centerx, self.rect.centery
        self.thread4.rect.center = self.rect.centerx, self.rect.centery
        self.thread5.rect.center = self.rect.centerx, self.rect.centery
        self.thread6.rect.center = self.rect.centerx, self.rect.centery

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, green, self.position, (self.position + self.velocity * scale), 5)
        pg.draw.circle(screen, blue, (int(self.target[0]), int(self.target[1])), 8)

    def update(self):
        if self.health > 0:
            draw_lives_bombs(screen, game_area.x + 3, 25, int(self.health / 5000 * 40), stat_images[3])
        if self.attack_state:
            if not self.rect.collidepoint(self.target) and self.health > 0:
                self.velocity += self.wander()
                self.position += self.velocity
                self.image = boss2[0]
            elif self.rect.collidepoint(self.target):
                self.wander()
                if self.health > 0:
                    self.attack()
                self.image = boss2[1]
            if self.health <= 0:

                if self.do_once == 0:
                    clear_bullets()
                    play_sound('bossdeath', volume=3)
                    self.kill()
                    self.do_once += 1

        self.rect.clamp_ip(game_area)
        self.rect.center = self.position
        if self.velocity.length() > 2:
            self.velocity.scale_to_length(2)


class Boss3(pg.sprite.Sprite):
    def __init__(self, attack_state):
        pg.sprite.Sprite.__init__(self)
        self.image = boss3[0]
        self.attack_image = boss3[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .40 / 2)
        self.rect.x = game_area.centerx - self.rect.width / 2
        self.rect.y = game_area.height / 4
        self.last = pg.time.get_ticks()
        self.health = 6000
        self.attack_state = attack_state
        self.is_boss = True
        self.velocity = Vector2(0, 1)
        self.position = Vector2(self.rect.center)
        self.movement_delay = 1000
        self.last_movement = pg.time.get_ticks()
        self.frequency = 2000
        self.offset = 100
        self.acceleration = Vector2(0, 1)
        self.desired = Vector2(0, 0)
        self.target = randint(100 + game_area.left, game_area.right), randint(100 + game_area.top, int(game_area.bottom / 2))
        self.last_target = 0
        self.moving = False
        self.thread = BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[2], 4, 3, fire_rate=200,
                                  pattern_amount=12, pattern_spread=30, do_random=True)
        self.thread2 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[14], 2, 2, fire_rate=200,
                                   pattern_amount=6, pattern_spread=60, do_accel=True)
        self.thread2.accel_amount = 0.03
        self.thread3 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[11], 3, -5, fire_rate=200,
                                   pattern_amount=10, pattern_spread=36)
        self.thread4 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[5], 5, 1, fire_rate=300,
                                   pattern_amount=8, pattern_spread=45, do_curve=True, curve=0.25)
        self.thread4opposite = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[5], 5, -1, fire_rate=300,
                                           pattern_amount=8, pattern_spread=45, do_curve=True, curve=-0.25)
        self.thread5 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[7], 4, 2, fire_rate=200,
                                   pattern_amount=6, pattern_spread=60)
        self.thread6 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 3, 5, fire_rate=500,
                                   pattern_amount=8, pattern_spread=45)
        self.thread7 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 4, -.5, fire_rate=500,
                                   pattern_amount=10, pattern_spread=36)
        self.thread8 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 4, .5, fire_rate=500,
                                   pattern_amount=10, pattern_spread=36)
        self.thread9 = BulletGroup(self.rect.x, self.rect.y, choice(pointed_bullet_images[13:16]), 3, 5, fire_rate=300,
                                   pattern_amount=20, pattern_spread=18, do_random=True)
        self.count = 0
        self.do_once = 0

    def wander(self):
        if pg.time.get_ticks() - self.last_target > self.frequency:
            self.last_target = pg.time.get_ticks()
            self.target = Vector2(randint(100 + game_area.left, game_area.right),
                                  randint(100 + game_area.top, int(game_area.bottom / 2)))
        return self.seek(self.target)

    def seek(self, target: Vector2):
        self.desired = (target - self.position).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 1:
            steer.scale_to_length(1)
        return steer

    def attack(self):
        if 6000 >= self.health > 4800:
            self.thread.shoot()
            self.thread2.shoot()
        elif 4800 >= self.health > 3600:
            self.thread2.shoot()
            self.thread3.shoot()
        elif 3600 >= self.health > 2400:
            self.thread4opposite.shoot()
            self.thread4.shoot()
        elif 2400 >= self.health > 1200:
            self.thread4.do_curve, self.thread.do_curve = False, False
            self.thread4.do_accel, self.thread.accel = True, True
            self.thread4.speed, self.thread.speed = 1, 1
            self.thread4.shoot()
            self.thread4opposite.shoot()
        elif 1200 >= self.health > 0:
            self.thread7.shoot()
            self.thread8.shoot()
            self.thread9.shoot()

        self.thread.rect.center = self.rect.centerx, self.rect.centery
        self.thread2.rect.center = self.rect.centerx, self.rect.centery
        self.thread3.rect.center = self.rect.centerx, self.rect.centery
        self.thread4.rect.center = self.rect.centerx, self.rect.centery
        self.thread4opposite.rect.center = self.rect.centerx, self.rect.centery
        self.thread5.rect.center = self.rect.centerx, self.rect.centery
        self.thread6.rect.center = self.rect.centerx, self.rect.centery
        self.thread7.rect.center = self.rect.centerx, self.rect.centery
        self.thread8.rect.center = self.rect.centerx, self.rect.centery
        self.thread9.bullet_image = choice(pointed_bullet_images[13:16])
        self.thread9.rect.center = self.rect.centerx, self.rect.centery

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, green, self.position, (self.position + self.velocity * scale), 5)
        pg.draw.circle(screen, blue, (int(self.target[0]), int(self.target[1])), 8)

    def update(self):
        if self.health > 0:
            draw_lives_bombs(screen, game_area.x + 3, 25, int(self.health / 6000 * 40), stat_images[3])
        if self.attack_state:
            if not self.rect.collidepoint(self.target) and self.health > 0:
                self.velocity += self.wander()
                self.position += self.velocity
                self.image = boss3[0]
            elif self.rect.collidepoint(self.target):
                self.wander()
                if self.health > 0:
                    self.attack()
                self.image = boss3[1]
            if self.health <= 0:

                if self.do_once == 0:
                    clear_bullets()
                    play_sound('bossdeath', volume=3)
                    self.kill()
                    self.do_once += 1

        self.rect.clamp_ip(game_area)
        self.rect.center = self.position
        if self.velocity.length() > 4:
            self.velocity.scale_to_length(4)


class Midboss2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = boss4[0]
        self.attack_image = boss4[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .40 / 2)
        self.rect.x = game_area.centerx - self.rect.width / 2
        self.rect.y = game_area.height / 4
        self.last = pg.time.get_ticks()
        self.health = 1000
        self.attacking = False
        self.is_boss = True
        self.velocity = Vector2(0, 1)
        self.position = Vector2(self.rect.center)
        self.movement_delay = 1000
        self.last_movement = pg.time.get_ticks()
        self.frequency = 2000
        self.timeout = 2000
        self.offset = 100
        self.acceleration = Vector2(0, 1)
        self.desired = Vector2(0, 0)
        self.target = randint(100 + game_area.left, game_area.right), randint(100 + game_area.top, int(game_area.bottom / 2))
        self.last_target = 0
        self.moving = False
        self.thread = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[1], 5, 1, fire_rate=200,
                                  pattern_amount=6, pattern_spread=60)
        self.thread2 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[1], 5, -1, fire_rate=200,
                                   pattern_amount=6, pattern_spread=60)
        self.count = 0

    def wander(self):
        if pg.time.get_ticks() - self.last_target > self.frequency:
            self.last_target = pg.time.get_ticks()
            self.target = Vector2(randint(100 + game_area.left, game_area.right),
                                  randint(100 + game_area.top, int(game_area.bottom / 2)))
        return self.seek(self.target)

    def seek(self, target: Vector2):
        self.desired = (target - self.position).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 1:
            steer.scale_to_length(1)
        return steer

    def attack(self):
        if self.health > 0:
            self.thread.shoot()
            self.thread2.shoot()
        self.thread.rect.center = self.rect.centerx, self.rect.centery
        self.thread2.rect.center = self.rect.centerx, self.rect.centery

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, green, self.position, (self.position + self.velocity * scale), 5)
        pg.draw.circle(screen, blue, (int(self.target[0]), int(self.target[1])), 8)

    def update(self):
        self.timeout -= 1
        if self.timeout < 0:
            self.health = self.timeout
        if self.health > 0:
            draw_text(screen, str(self.timeout), (737, 43))
            draw_lives_bombs(screen, game_area.x + 3, 25, int(self.health / 1000 * 40), stat_images[3])
        if not self.rect.collidepoint(self.target) and self.health > 0:
            self.velocity += self.wander()
            self.position += self.velocity
            self.image = boss4[0]
        elif self.rect.collidepoint(self.target):
            self.wander()
            self.image = boss4[1]
        elif self.health <= 0:
            if self.count == 0 and self.timeout > 0:
                for i in range(50):
                    spawn_item(determine_center(self), 0)
                    spawn_item(determine_center(self), 1)
                spawn_item(self.rect.center, 2, amount=1)
                self.count += 1
            self.health -= 1
            self.velocity += self.seek(Vector2(width / 2, -150))
            self.position += self.velocity
            if self.rect.collidepoint(width / 2, -150):
                self.kill()
        self.rect.clamp_ip(game_area)
        self.rect.center = self.position
        if self.velocity.length() > 1:
            self.velocity.scale_to_length(1)
        self.attack()


class Boss4(pg.sprite.Sprite):
    def __init__(self, attack_state):
        pg.sprite.Sprite.__init__(self)
        self.image = boss4[0]
        self.attack_image = boss4[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .40 / 2)
        self.rect.x = game_area.centerx - self.rect.width / 2
        self.rect.y = game_area.height / 4
        self.last = pg.time.get_ticks()
        self.health = 8000
        self.attack_state = attack_state
        self.is_boss = True
        self.velocity = Vector2(0, 1)
        self.position = Vector2(self.rect.center)
        self.movement_delay = 1000
        self.last_movement = pg.time.get_ticks()
        self.frequency = 10000
        self.offset = 100
        self.acceleration = Vector2(0, 1)
        self.desired = Vector2(0, 0)
        self.target = randint(100 + game_area.left, game_area.right), randint(100 + game_area.top, int(game_area.bottom / 2))
        self.last_target = 0
        self.moving = False
        self.thread = BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[6], 4, 3, fire_rate=400,
                                  pattern_amount=12, pattern_spread=30, do_random=True, do_curve=True, curve=0.5)
        self.thread_opp = BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[6], 4, -3,
                                      fire_rate=400,
                                      pattern_amount=12, pattern_spread=30, do_random=True, do_curve=True, curve=-0.5)
        self.thread2 = BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[12], 0.5, 1,
                                   fire_rate=200,
                                   pattern_amount=12, pattern_spread=30, do_accel=True)
        self.thread3 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[10], 3, -5, fire_rate=100,
                                   pattern_amount=5, pattern_spread=72)
        self.thread4 = BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[8], 5, 3,
                                   fire_rate=800,
                                   pattern_amount=20, pattern_spread=18, do_curve=True, curve=0.25)
        self.thread4opposite = BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[8], 5, -3,
                                           fire_rate=800, pattern_amount=20, pattern_spread=18, do_curve=True,
                                           curve=-0.25)
        self.thread5 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[16], 6, 1, fire_rate=200,
                                   pattern_amount=9, pattern_spread=40)
        self.thread5_opp = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[16], 6, -1, fire_rate=200,
                                       pattern_amount=9, pattern_spread=40)
        self.thread6 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[10], 0.1, 1, fire_rate=100,
                                   pattern_amount=5, pattern_spread=72, do_accel=True)
        self.thread6_opp = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[10], 0.1, -1, fire_rate=100,
                                       pattern_amount=5, pattern_spread=72, do_accel=True)
        self.thread7 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 4, -.5, fire_rate=500,
                                   pattern_amount=10, pattern_spread=36)
        self.thread8 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[5], 4, .5, fire_rate=500,
                                   pattern_amount=10, pattern_spread=36)
        self.thread9 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 7, 1, fire_rate=500,
                                   pattern_amount=12, pattern_spread=30, do_accel=True)

        self.count = 0
        self.do_once = 0

    def wander(self):
        if pg.time.get_ticks() - self.last_target > self.frequency:
            self.last_target = pg.time.get_ticks()
            self.target = Vector2(randint(100 + game_area.left, game_area.right),
                                  randint(100 + game_area.top, int(game_area.bottom / 2)))
        return self.seek(self.target)

    def seek(self, target: Vector2):
        self.desired = (target - self.position).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 1:
            steer.scale_to_length(1)
        return steer

    def attack(self):
        if 8000 >= self.health > 7000:
            self.thread.shoot()
            self.thread_opp.shoot()
        elif 7000 >= self.health > 6000:
            self.thread2.shoot()
            self.thread3.shoot()
        elif 6000 >= self.health > 5000:
            self.thread4opposite.shoot()
            self.thread4.shoot()
        elif 5000 >= self.health > 4000:
            self.thread5_opp.shoot()
            self.thread5.shoot()
        elif 4000 >= self.health > 3000:
            self.thread6.shoot()
            self.thread6_opp.shoot()
        elif 3000 >= self.health > 2000:
            self.thread7.shoot()
            self.thread8.shoot()
            self.thread9.shoot()
        elif 2000 >= self.health > 1000:
            self.thread7.shoot()
            self.thread8.shoot()
            self.thread9.shoot()
        elif 1000 >= self.health > 0:
            self.thread7.shoot()
            self.thread8.shoot()
            self.thread9.shoot()

        self.thread.rect.center = self.rect.centerx, self.rect.centery
        self.thread_opp.rect.center = self.rect.centerx, self.rect.centery
        self.thread2.rect.center = self.rect.centerx, self.rect.centery
        self.thread3.rect.center = determine_center(self)
        self.thread4.rect.center = self.rect.centerx, self.rect.centery
        self.thread4opposite.rect.center = self.rect.centerx, self.rect.centery
        self.thread5.rect.center = self.rect.centerx - 100, self.rect.centery
        self.thread5_opp.rect.center = self.rect.centerx + 100, self.rect.centery
        self.thread6.rect.center = self.rect.centerx, self.rect.centery
        self.thread6_opp.rect.center = self.rect.centerx, self.rect.centery
        self.thread6.rect.center = self.rect.centerx, self.rect.centery
        self.thread7.rect.center = self.rect.centerx, self.rect.centery
        self.thread8.rect.center = self.rect.centerx, self.rect.centery
        self.thread9.bullet_image = choice(pointed_bullet_images[13:16])
        self.thread9.rect.center = self.rect.centerx, self.rect.centery

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, green, self.position, (self.position + self.velocity * scale), 5)
        pg.draw.circle(screen, blue, (int(self.target[0]), int(self.target[1])), 8)

    def update(self):
        if self.health > 0:
            draw_lives_bombs(screen, game_area.x + 3, 25, int(self.health / 8000 * 40), stat_images[3])
        if self.attack_state:
            if not self.rect.collidepoint(self.target) and self.health > 0:
                self.velocity += self.wander()
                self.position += self.velocity
                self.image = boss4[0]
            elif self.rect.collidepoint(self.target):
                self.wander()
                if self.health > 0:
                    self.attack()
                self.image = boss4[1]
            if self.health <= 0:

                if self.do_once == 0:
                    clear_bullets()
                    play_sound('bossdeath', volume=3)
                    self.kill()
                    self.do_once += 1

        self.rect.clamp_ip(game_area)
        self.rect.center = self.position
        if self.velocity.length() > 1:
            self.velocity.scale_to_length(1)


class Boss5(pg.sprite.Sprite):
    def __init__(self, attack_state):
        pg.sprite.Sprite.__init__(self)
        self.image = boss5[0]
        self.attack_image = boss5[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .40 / 2)
        self.rect.x = game_area.centerx - self.rect.width / 2
        self.rect.y = game_area.height / 4
        self.last = pg.time.get_ticks()
        self.health = 15000
        self.attack_state = attack_state
        self.is_boss = True
        self.velocity = Vector2(0, 1)
        self.position = Vector2(self.rect.center)
        self.movement_delay = 1000
        self.last_movement = pg.time.get_ticks()
        self.frequency = 30000
        self.offset = 10
        self.acceleration = Vector2(0, 1)
        self.desired = Vector2(0, 0)
        self.target = randint(100 + game_area.left, game_area.right), randint(100 + game_area.top, int(game_area.bottom / 2))
        self.last_target = 0
        self.moving = False
        self.thread = BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[8], 3, 1, fire_rate=200,
                                  pattern_amount=6, pattern_spread=60, do_accel=True)
        self.thread_opp = BulletGroup(self.rect.centerx, self.rect.centery, circular_bullet_images[8], 3, -1,
                                      fire_rate=200,
                                      pattern_amount=6, pattern_spread=60, do_accel=True)
        self.thread2 = BulletGroup(self.rect.centerx, self.rect.centery, pointed_bullet_images[5], 0.5, 1,
                                   fire_rate=200,
                                   pattern_amount=20, pattern_spread=18, do_accel=True)
        self.thread3 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[7], 3, -5, fire_rate=100,
                                   pattern_amount=8, pattern_spread=45)
        self.thread4 = BulletGroup(self.rect.x, self.rect.y, choice(pointed_bullet_images[0:5]), 4, 0.8, fire_rate=200,
                                   pattern_amount=24, pattern_spread=15)
        self.thread5 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[16], 2, 2, fire_rate=200,
                                   pattern_amount=12, pattern_spread=15)
        self.thread5_opp = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[16], 2, 2, fire_rate=200,
                                       pattern_amount=12, pattern_spread=15)
        self.thread6 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[10], 4, 1, fire_rate=100,
                                   pattern_amount=10, pattern_spread=10)
        self.thread6_opp = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[10], 4, -1, fire_rate=100,
                                       pattern_amount=10, pattern_spread=10)
        self.thread7 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[5], 4, -.5, fire_rate=300,
                                   pattern_amount=3, pattern_spread=120)
        self.thread8 = BulletGroup(self.rect.x, self.rect.y, circular_bullet_images[5], 4, .5, fire_rate=300,
                                   pattern_amount=3, pattern_spread=120)
        self.thread9 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[5], 1, 1, fire_rate=200,
                                   pattern_amount=12, pattern_spread=30, do_accel=True)
        self.thread10 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[11], 1, 3, fire_rate=25,
                                    pattern_amount=4, pattern_spread=90, do_accel=True)
        self.thread11 = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[12], 3, 2, fire_rate=60,
                                    pattern_amount=1, pattern_spread=1)
        self.thread11_opp = BulletGroup(self.rect.x, self.rect.y, pointed_bullet_images[12], 3, -2, fire_rate=100,
                                        pattern_amount=1, pattern_spread=1)

        self.count = 0
        self.do_once = 0

    def wander(self):
        if pg.time.get_ticks() - self.last_target > self.frequency:
            self.last_target = pg.time.get_ticks()
            self.target = Vector2(randint(100 + game_area.left, game_area.right),
                                  randint(100 + game_area.top, int(game_area.bottom / 2)))
        return self.seek(self.target)

    def seek(self, target: Vector2):
        self.desired = (target - self.position).normalize() * 10
        steer = (self.desired - self.velocity)
        if steer.length() > 1:
            steer.scale_to_length(1)
        return steer

    def attack(self):
        if 15000 >= self.health > 14000:
            self.thread.shoot()
            self.thread_opp.shoot()
        elif 14000 >= self.health > 13000:
            self.thread2.shoot()
            self.thread3.shoot()
        elif 13000 >= self.health > 12000:
            self.thread4.shoot()
        elif 12000 >= self.health > 11000:
            self.thread5_opp.shoot()
            self.thread5.shoot()
        elif 11000 >= self.health > 10000:
            self.thread6.shoot()
            self.thread6_opp.shoot()
        elif 10000 >= self.health > 9000:
            self.thread7.shoot()
            self.thread8.shoot()
        elif 9000 >= self.health > 8000:
            self.thread7.shoot()
            self.thread8.shoot()
            self.thread9.shoot()
        elif 8000 >= self.health > 7000:
            self.thread10.shoot()
        elif 7000 >= self.health > 6000:
            self.thread8.shoot()
            self.thread9.shoot()
        elif 6000 >= self.health > 5000:
            self.thread7.shoot()
            self.thread8.shoot()
            self.thread9.shoot()
        elif 5000 >= self.health >= 4000:
            self.thread7.shoot()
            self.thread9.shoot()
            self.thread10.shoot()
        elif 4000 > self.health:
            self.thread11.pattern_amount = int((4000 - self.health) / 1000 + 3)
            self.thread11.pattern_spread = int(360 / self.thread11.pattern_amount)
            self.thread11.shoot()
            self.thread11_opp.pattern_amount = int((4000 - self.health) / 1000 + 3)
            self.thread11_opp.pattern_spread = int(360 / self.thread11.pattern_amount)
            self.thread11_opp.shoot()

        self.thread.rect.center = self.rect.centerx, self.rect.centery
        self.thread_opp.rect.center = self.rect.centerx, self.rect.centery
        self.thread2.rect.center = self.rect.centerx, self.rect.centery
        self.thread3.rect.center = randint(self.rect.left - 100, self.rect.right + 100), \
                                   randint(self.rect.top - 100, int(self.rect.bottom + 100))
        self.thread4.rect.center = self.rect.centerx, self.rect.centery
        self.thread4.bullet_image = choice(pointed_bullet_images[0:5])
        self.thread5.rect.center = self.rect.centerx - 100, self.rect.centery
        self.thread5_opp.rect.center = self.rect.centerx + 100, self.rect.centery
        self.thread6.rect.center = self.rect.centerx, self.rect.centery
        self.thread6_opp.rect.center = self.rect.centerx, self.rect.centery
        self.thread6.rect.center = self.rect.centerx, self.rect.centery
        self.thread7.rect.center = self.rect.centerx, self.rect.centery
        self.thread8.rect.center = self.rect.centerx, self.rect.centery
        self.thread9.bullet_image = choice(pointed_bullet_images[13:16])
        self.thread9.rect.center = self.rect.centerx, self.rect.centery
        self.thread10.rect.center = self.rect.centerx, self.rect.centery
        self.thread11.rect.center = self.rect.centerx, self.rect.centery
        self.thread11_opp.rect.center = self.rect.centerx, self.rect.centery

    def draw_vectors(self):
        scale = 25
        pg.draw.line(screen, green, self.position, (self.position + self.velocity * scale), 5)
        pg.draw.circle(screen, blue, (int(self.target[0]), int(self.target[1])), 8)

    def update(self):
        if self.health > 0:
            draw_lives_bombs(screen, game_area.x + 3, 25, int(self.health / 15000 * 40), stat_images[3])
        if self.attack_state:
            if not self.rect.collidepoint(self.target) and self.health > 0:
                self.velocity += self.wander()
                self.position += self.velocity
                self.image = boss5[0]
            elif self.rect.collidepoint(self.target):
                self.wander()
                if self.health > 0:
                    self.attack()
                self.image = boss5[1]
            if self.health <= 0:

                if self.do_once == 0:
                    clear_bullets()
                    play_sound('bossdeath', volume=3)
                    self.kill()
                    self.do_once += 1

        self.rect.clamp_ip(game_area)
        self.rect.center = self.position
        if self.velocity.length() > 5:
            self.velocity.scale_to_length(5)
