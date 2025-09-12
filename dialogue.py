from constants import *
from projectiles_effects_background import draw_long_text
from sound_engine import play_music


class TextBox(pg.sprite.Sprite):
    def __init__(self, topleft, break_point1, break_point2, boss, dialogue, music="music4.ogg"):
        pg.sprite.Sprite.__init__(self)
        self.image = textbox
        self.rect = self.image.get_rect()
        self.permanent_topleft = topleft
        self.rect.topleft = topleft
        self.count = 0
        self.text_rect = pg.Rect(436, 570, 332, 124)
        self.i = 0
        self.breakpoint = break_point1
        self.breakpoint2 = break_point2
        self.do_it_once = 0
        self.boss = boss
        self.dialogue = dialogue
        self.music = music

    def display_dialogue(self, dialogue):
        sprite_location = dialogue[0]
        sprite = load_image(0, 0, portrait_folder, dialogue[1])
        text = dialogue[2]
        if sprite_location == "left":
            self.rect.topleft = self.permanent_topleft
            screen.blit(sprite, (186, 440))
            draw_long_text(screen, text, (436, self.rect.top + 3), self.text_rect)
        if sprite_location == "right":
            # self.rect.topleft = (186, 317)
            screen.blit(sprite, (526, 440))
            draw_long_text(screen, text, (self.rect.left + 5, self.rect.top + 5), self.text_rect)

    def update(self):
        try:
            self.display_dialogue(self.dialogue[self.i])
        except IndexError:
            if self.boss is not None:
                self.boss.rect.y = height / 4
                all_sprites.add(self.boss)
                self.boss.attack_state = True
            self.kill()
        if self.i >= self.breakpoint2:
            if self.boss is not None:
                screen.blit(self.boss.image, (game_area.centerx - self.boss.rect.width / 2, game_area.height / 4))
        if self.i >= self.breakpoint:
            if self.do_it_once == 0:
                play_music(self.music)
                self.do_it_once += 1
        if self.i - 1 < len(self.dialogue):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.i += 1
        else:
            self.boss.attack_state = True
            self.kill()
