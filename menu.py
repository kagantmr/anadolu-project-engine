# Imports of other modules
from players import *
from sound_engine import *
from gui import *
import sys

pg.font.init()

button1 = Button((width / 4, 550), buttons[0])
button2 = Button((3 * width / 4, 550), buttons[1])
button8 = Button((2 * width / 4, 550), buttons[4])
shade = Background(background_shade, -1)
shade.bgX1 = 0
shade.bgX2 = 0
button3 = Button((width / 4, height / 2 + 50), shot_types[0])
button4 = Button((2 * width / 4, height / 2 + 50), shot_types[1])
button5 = Button((3 * width / 4, height / 2 + 50), shot_types[2])
button6 = Button((480, 2 * height / 3), buttons[2])
silhouette = GUImage(silhouette, (-100, height / 2), do_slide=True)
title = GUImage(buttons[3], (width / 2, -50), do_slide_from_above=True)
track_1 = Text(f'1. {translation["track_1"]}', (30, 30))
track_2 = Text(f'2. {translation["track_2"]}', (30, 60))
track_3 = Text(f'3. {translation["track_3"]}', (30, 90))
track_4 = Text(f'4. {translation["track_4"]}', (30, 120))
track_5 = Text(f'5. {translation["track_5"]}', (30, 150))
track_6 = Text(f'6. {translation["track_6"]}', (30, 180))
track_7 = Text(f'7. {translation["track_7"]}', (30, 210))
track_8 = Text(f'8. {translation["track_8"]}', (30, 240))
track_9 = Text(f'9. {translation["track_9"]}', (30, 60))
track_10 = Text(f'10. {translation["track_10"]}', (30, 90))
track_11 = Text(f'11. {translation["track_11"]}', (30, 120))
track_12 = Text(f'12. {translation["track_12"]}', (30, 150))
track_13 = Text(f'13. {translation["track_13"]}', (30, 180))
track_14 = Text(f'14. {translation["track_14"]}', (30, 210))
back_button = Text(f'< {translation["back_button"]}', (850, 690))
track_1.rect.topleft = (50, 50)
track_2.rect.topleft = (50, 80)
track_3.rect.topleft = (50, 110)
track_4.rect.topleft = (50, 140)
track_5.rect.topleft = (50, 170)
track_6.rect.topleft = (50, 200)
track_7.rect.topleft = (50, 230)
track_8.rect.topleft = (50, 260)
track_9.rect.topleft = (50, 290)
track_10.rect.topleft = (50, 320)
track_11.rect.topleft = (50, 350)
track_12.rect.topleft = (50, 380)
track_13.rect.topleft = (50, 410)
track_14.rect.topleft = (50, 440)


def start_screen():
    clear_sprites()
    records = read_from_table('records.json')
    silhouette.rect.center = (-100, height / 2)
    all_sprites.add(silhouette)
    all_sprites.add(title)
    all_sprites.add(button1, button2, button8)
    choose_menu = False
    music_menu = False
    menu = True
    play_music("music1.ogg")
    while menu:
        screen.fill(white)
        if choose_menu:
            clear_sprites()
            all_sprites.add(back_button)
            if records["a_cleared"]:
                all_sprites.add(Text(f'{translation["cleared"]}', (width / 4, height / 3 + 50)))
            if records["b_cleared"]:
                all_sprites.add(Text(f'{translation["cleared"]}', (2 * width / 4, height / 3 + 50)))
            if records["c_cleared"]:
                all_sprites.add(Text(f'{translation["cleared"]}', (3 * width / 4, height / 3 + 50)))
            all_sprites.add(Text(f'{translation["nay_type_text"]}', (width / 2, height / 4)))
            all_sprites.add(Text(f'{translation["type_a_text"]}', (width / 2, height / 2 + 140)))
            all_sprites.add(Text(f'{translation["type_b_text"]}', (width / 2, height / 2 + 180)))
            all_sprites.add(Text(f'{translation["type_c_text"]}', (width / 2, height / 2 + 220)))
            all_sprites.add(button3, button4, button5)
        if music_menu:
            if not records["a_cleared"] and not records["b_cleared"] and not records["c_cleared"]:
                play_sound("denied")
                music_menu = False
            else:
                clear_sprites()
                all_sprites.add(back_button)
                all_sprites.add(Text(f'{translation["music_room_top"]}', (width / 2, 20)))
                all_sprites.add(track_1, track_2, track_3, track_4, track_5, track_6, track_7, track_8, track_9,
                                track_10, track_11, track_12, track_13, track_14)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.mixer.music.stop()
                fade_in()
                sys.exit(1)
            if event.type == pg.MOUSEBUTTONDOWN:
                if button1.check_if_collided(pg.mouse.get_pos()):
                    choose_menu = True
                if button2.check_if_collided(pg.mouse.get_pos()):
                    pg.mixer.music.stop()
                    sys.exit(1)
                if button8.check_if_collided(pg.mouse.get_pos()):
                    music_menu = True
                if back_button.check_if_collided(pg.mouse.get_pos()):
                    if music_menu:
                        play_music("music1.ogg")
                    clear_sprites()
                    all_sprites.add(silhouette)
                    all_sprites.add(title)
                    all_sprites.add(button1, button2, button8)
                    choose_menu = False
                    music_menu = False
                    menu = True
                if choose_menu:
                    if button3.check_if_collided(pg.mouse.get_pos()):
                        fade_in()
                        clear_sprites()
                        return PlayerA()
                    if button4.check_if_collided(pg.mouse.get_pos()):
                        fade_in()
                        clear_sprites()
                        return PlayerB()
                    if button5.check_if_collided(pg.mouse.get_pos()):
                        fade_in()
                        clear_sprites()
                        return PlayerC()
                if music_menu:
                    if track_1.check_if_collided(pg.mouse.get_pos()):
                        play_music('music1.ogg')
                    if track_2.check_if_collided(pg.mouse.get_pos()):
                        play_music('music2.ogg')
                    if track_3.check_if_collided(pg.mouse.get_pos()):
                        play_music('music4.ogg')
                    if track_4.check_if_collided(pg.mouse.get_pos()):
                        play_music('music5.ogg')
                    if track_5.check_if_collided(pg.mouse.get_pos()):
                        play_music('music6.ogg')
                    if track_6.check_if_collided(pg.mouse.get_pos()):
                        play_music('music7.ogg')
                    if track_7.check_if_collided(pg.mouse.get_pos()):
                        play_music('music8.ogg')
                    if track_8.check_if_collided(pg.mouse.get_pos()):
                        play_music('music10.ogg')
                    if track_9.check_if_collided(pg.mouse.get_pos()):
                        play_music('music11.ogg')
                    if track_10.check_if_collided(pg.mouse.get_pos()):
                        play_music('music12.ogg')
                    if track_11.check_if_collided(pg.mouse.get_pos()):
                        play_music('music13.ogg')
                    if track_12.check_if_collided(pg.mouse.get_pos()):
                        play_music('music14.ogg')
                    if track_13.check_if_collided(pg.mouse.get_pos()):
                        play_music('music15.ogg')
                    if track_14.check_if_collided(pg.mouse.get_pos()):
                        play_music('music3.ogg')

        # Draws stuff on the screen.

        # SPRITE AND DISPLAY UPDATES
        all_sprites.update()
        screen.blit(menu_background, screen.get_rect())
        draw_text(screen, '%.2f' % clock.get_fps() + 'fps', (0, height - 20))
        shade.update()
        all_sprites.draw(screen)
        pg.display.update()
        clock.tick(60)
