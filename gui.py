from constants import *
from projectiles_effects_background import load_font


class GUImage(pg.sprite.Sprite):
    def __init__(self, image, pos, do_slide=False, do_slide_from_above=False):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.do_slide = do_slide
        self.do_slide_from_above = do_slide_from_above

    def slide_from_above(self):
        if self.rect.centery != height / 3:
            self.rect.centery += 2

    def slide(self):
        if self.rect.centerx != width / 2:
            self.rect.centerx += 4

    def update(self):
        if self.do_slide_from_above:
            self.slide_from_above()
        if self.do_slide:
            self.slide()


class Text(pg.sprite.Sprite):
    def __init__(self, text, center, size=20):
        pg.sprite.Sprite.__init__(self)
        self.font = load_font('pc-9800', size)
        self.image = self.font.render(text, True, white)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def check_if_collided(self, mouse_position):
        if self.rect.right > mouse_position[0] > self.rect.left and self.rect.bottom > mouse_position[1] \
                > self.rect.top and self.alive():
            return True
        else:
            return False


class Button(pg.sprite.Sprite):
    def __init__(self, center, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center

    def check_if_collided(self, mouse_position):
        if self.rect.right > mouse_position[0] > self.rect.left and self.rect.bottom > mouse_position[1] \
                > self.rect.top and self.alive():
            return True
        else:
            return False
