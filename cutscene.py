from players import *
from sound_engine import play_music
import sys


class CutsceneDisplayer:
    def __init__(self, dialogue):
        self.count = 0
        self.text_rect = pg.Rect(88, 600, 786, 120)
        self.i = 0
        self.whole_dialogue = dialogue
        self.dialogue = dialogue[self.i]

    def advance_cutscene(self):
        try:
            self.i += 1
            self.dialogue = self.whole_dialogue[self.i]
        except IndexError:
            return True

    def display_dialogue(self):
        sprite = load_image(0, 0, ending_folder, self.dialogue[0])
        text = self.dialogue[1]
        screen.blit(sprite, (0, 0))
        draw_long_text(screen, text, (88, 600), self.text_rect, color=black)


def cutscene_loop_a(details: list):
    clear_sprites()
    displayer = CutsceneDisplayer(cutscene_a)
    play_music("music14.ogg")
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_z:
                if displayer.advance_cutscene():
                    fade_in()
                    return details
        all_sprites.update()
        screen.fill(black)
        screen.blit(cutscene_image, screen.get_rect())
        displayer.display_dialogue()
        all_sprites.draw(screen)
        pg.display.update()
        clock.tick(60)


def cutscene_loop_b(details: list):
    clear_sprites()
    displayer = CutsceneDisplayer(cutscene_b)
    play_music("music14.ogg")
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_z:
                if displayer.advance_cutscene():
                    fade_in()
                    return details
        all_sprites.update()
        screen.fill(black)
        screen.blit(cutscene_image, screen.get_rect())
        displayer.display_dialogue()
        all_sprites.draw(screen)
        pg.display.update()
        clock.tick(60)


def cutscene_loop_c(details: list):
    clear_sprites()
    displayer = CutsceneDisplayer(cutscene_c)
    play_music("music14.ogg")
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_z:
                if displayer.advance_cutscene():
                    fade_in()
                    return
        all_sprites.update()
        screen.fill(black)
        screen.blit(cutscene_image, screen.get_rect())
        displayer.display_dialogue()
        all_sprites.draw(screen)
        pg.display.update()
        clock.tick(60)
