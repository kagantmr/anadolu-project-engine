from game import *
from cutscene import *
from menu import *
import sys

pg.display.set_icon(load_image(0, 0, gui_folder, "icon", extension=".ico"))
pg.display.set_caption("Anadolu Projesi: Issız Tamağ Öyküsü ~ Forsaken Infernal Tale v1.0.0")


def ending(details: list):
    play_music("music15.ogg")
    scroll_y_location = height
    game_alpha = 0
    cast_alpha = 0
    cast_image.set_alpha(0)
    game_image.set_alpha(0)
    pause_quit_button = Button((width / 2, 2 * height / 3), buttons[2])
    counter = 0
    while True:
        counter += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if pause_quit_button.check_if_collided(pg.mouse.get_pos()):
                    main()
                    return
        all_sprites.update()
        screen.fill(black)
        screen.blit(ending_image, screen.get_rect())
        if counter > 200 and scroll_y_location > -658:
            game_image.set_alpha(game_alpha)
            screen.blit(scroll_image, (width / 2 - scroll_image.get_rect().width, scroll_y_location))
            screen.blit(game_image, (width / 2 + 100, height / 2 - 150))
            scroll_y_location -= 1
            game_alpha += 1
        if scroll_y_location <= -658:
            cast_image.set_alpha(cast_alpha)
            screen.blit(cast_image, screen.get_rect())
            cast_alpha += 1
            draw_centered_text(screen, f'{translation["thank_you"]}', (width / 2, 200), font_3)
            draw_centered_text(screen, f'{translation["ending_message"]}', (width / 2, 300), font_1)
            draw_centered_text(screen, f'{translation["final_score_text"]} {details[1]}', (width / 2, 350), font_1)
            draw_centered_text(screen, f'{translation["deaths_text"]} {details[3]}', (width / 2, 400), font_1)
        if cast_alpha > 255:
            all_sprites.add(pause_quit_button)
        all_sprites.draw(screen)
        pg.display.update()
        clock.tick(60)


def cutscene(details: list):
    player_type = details[2]
    if isinstance(player_type, PlayerA):
        cutscene_loop_a(details)
    if isinstance(player_type, PlayerB):
        cutscene_loop_b(details)
    if isinstance(player_type, PlayerC):
        cutscene_loop_c(details)
    fade_in()
    ending(details)


def game_over(is_over=None, score=None, shot_type=None, deaths=None):
    return_button = Button((850, 675), buttons[2])
    if is_over is None:
        fade_in()
        play_music("music3.ogg")
    else:
        return [is_over, score, shot_type, deaths]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if button6.check_if_collided(pg.mouse.get_pos()):
                    main()
                    return
                if return_button.check_if_collided(pg.mouse.get_pos()):
                    main()
                    return
        all_sprites.update()
        screen.fill(black)
        if is_over is None:
            all_sprites.add(button6)
            all_sprites.add(Text(translation["game_over"], (width / 2, height / 3), size=50))
        all_sprites.draw(screen)
        pg.display.update()
        clock.tick_busy_loop(60)


def main():
    if full_screen:
        pg.display.set_mode((width, height), pg.HWSURFACE | pg.FULLSCREEN | pg.SCALED | pg.HWACCEL, vsync=1)
    clear_sprites()
    player = start_screen()
    if_ended = stage1_loop(player)
    clear_sprites()
    try:
        cutscene_state = game_over(is_over=if_ended[0], score=if_ended[1], shot_type=if_ended[2], deaths=if_ended[3])
    except TypeError:
        cutscene_state = game_over()
    cutscene(cutscene_state)


main()
pg.quit()
