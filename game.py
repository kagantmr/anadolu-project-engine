# Imports of other modules
from enemy import *
from gui import Button
from sound_engine import *
from boss import *
from players import *
from dialogue import TextBox
import sys
from datetime import datetime


def kill_player(player, collision):
    """
    Makes the player invincible, spawns items, kills the player and clears the screen.
    Also prevents enemies on the screen from shooting.
    """
    play_sound("death")
    player.invincible = True
    death_start = pg.time.get_ticks()
    player.kill()
    for i in range(int(player.power) * 20):
        spawn_item((randint(collision.rect.left, collision.rect.right),
                    randint(collision.rect.top, collision.rect.bottom)), 0)
    if death_start - pg.time.get_ticks() > 2000:
        all_sprites.add(player)
    player.hide = True
    for bullet in bullets:
        bullet.kill()
    for enemy in enemies:
        enemy.do_shoot = False
    player.lives -= 1
    player.power = 0
    player.deaths += 1
    player.bombs = 3
    summon_explosion(collision.rect.center)
    player.last_collision = pg.time.get_ticks()


def draw_stage_data(player, score):
    screen.blit(cover, screen.get_rect())
    draw_text(screen, f'{translation["score_text"]} ' + str(score).zfill(20), (502, 0))
    draw_text(screen, f'{translation["highscore_text"]} ' + str(records["high_score"]).zfill(20), (188, 0))
    draw_text(screen, f'{translation["day_text"]} {datetime.now().strftime("%A")}', (9, 22))
    draw_text(screen, f'{translation["date_text"]} {datetime.now().strftime("%d/%d/%Y")}', (9, 62))
    draw_text(screen, f'{translation["time_text"]} {datetime.now().strftime("%H:%M:%S")}', (9, 102))
    draw_text(screen, f'{translation["game_text"]}', (9, 142))
    draw_lives_bombs(screen, 9, 165, int(clock.get_fps() / 60 * 10), stat_images[2])
    draw_text(screen, '%.2f' % clock.get_fps() + 'fps', (0, height - 20))
    draw_text(screen, f'{translation["power_text"]}' + str(player.power), (786, 62))
    draw_text(screen, f'{translation["lives_text"]}', (786, 102))
    draw_lives_bombs(screen, 786, 125, player.lives, stat_images[0])
    draw_text(screen, f'{translation["bombs_text"]}', (786, 165))
    draw_lives_bombs(screen, 786, 187, player.bombs, stat_images[1])
    draw_text(screen, f'{translation["level_text"]}', (786, 220))
    draw_lives_bombs(screen, 786, 240, int(player.level / 300 * 10), stat_images[4])


def stage1_loop(player):
    """
    Main loop.
    """

    pause_quit_button = Button((width / 2, 2 * height / 3), buttons[2])
    play_music("music2.ogg")
    midboss = Midboss()
    background1 = Background(backgrounds1[0], -2)
    background2 = Background(backgrounds1[1], 0)  # Scrolling background loader.
    background2.background_image.set_alpha(100)
    stage1_boss = Boss(False)
    # Variables
    last = pg.time.get_ticks()
    score = 0  # Score
    stage = True
    crashed = False
    paused = False
    first_box = TextBox((186, 566), 21, 5, stage1_boss, dlg_1)
    second_box = TextBox((186, 566), 20, 20, None, dlg_2)
    counter = 0
    enemy_location = game_area.left + 20
    delay = 1000
    alpha = 101
    while not crashed:
        screen.fill(white)
        if not paused:
            counter += 1

            background1.update()

            all_sprites.draw(screen)
            background2.update()
            all_sprites.update()

            all_sprites.add(player)

            if counter % 100 == 0:
                background2.background_image.set_alpha(alpha)
                alpha += 5
            if counter == 2000:
                all_sprites.add(midboss)
                stage = False
                clear_bullets()
                clear_enemies()
            if counter > 2000 and midboss.health <= 0:
                stage = True
                delay = 1500
            if enemy_location > width:
                enemy_location = game_area.left + 20
            now = pg.time.get_ticks()
            if now - last > delay and stage:
                last = now
                if 100 < counter < 1000:
                    e = Enemy(enemy1[0], randint(0, 2), enemy_location, -25, 0, 2, health=20)
                    all_sprites.add(e)
                    enemies.add(e)
                    enemy_location += 50
                elif 1000 <= counter < 1800:
                    position, enemy_speed = choice([(1, 5), (game_area.right, -2)])
                    e = Enemy(enemy1[1], 4, position, randint(40, int(width / 3)), enemy_speed, 0, health=5)
                    all_sprites.add(e)
                    enemies.add(e)
                elif 4800 > counter > 1800:
                    spawn_enemy_randomly(choice(enemy1), randint(0, 2), 2)
            if counter == 4800:
                clear_bullets()
                clear_enemies()
                stage = False

            if counter == 4900:
                all_sprites.add(first_box)
            if counter > 4900 and stage1_boss.health <= 0:
                all_sprites.add(second_box)
            if counter > 4900 and stage1_boss.health <= 0 and second_box.i > 10:
                second_box.kill()
                fade_in()
                game = stage2_loop(player, score)
                return game
            # SPRITE AND DISPLAY UPDATES
            pause_quit_button.kill()
            draw_stage_data(player, score)
            if 1 < counter < 2000:
                draw_text(screen, f'{translation["stage1title1"]}', (786, 22))
            elif 2000 <= counter < 4000:
                draw_text(screen, f'{translation["stage1title2"]}', (786, 22))
            elif counter >= 4000:
                draw_text(screen, f'{translation["stage1title3"]}', (786, 22))

        if paused:

            all_sprites.add(pause_quit_button)
            background1.render()
            background2.render()
            screen.blit(bomb_bg, screen.get_rect())
            all_sprites.draw(screen)
            draw_stage_data(player, score)
            if 1 < counter < 2000:
                draw_text(screen, f'{translation["stage1title1"]}', (786, 22))
            elif 2000 <= counter < 4000:
                draw_text(screen, f'{translation["stage1title2"]}', (786, 22))
            elif counter >= 4000:
                draw_text(screen, f'{translation["stage1title3"]}', (786, 22))
            draw_centered_text(screen, f'{translation["paused"]}', game_area.center, font_3)
        # Lives
        if player.lives < 0:
            if records["high_score"] < score:
                records["high_score"] = score
            dump_into_table(records, 'records.json')
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if records["high_score"] < score:
                    records["high_score"] = score
                dump_into_table(records, 'records.json')
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if first_box.i - 1 < len(dlg_1) and first_box.alive():
                    first_box.i += 1
            # Bomb event is here.
            if event.type == pg.MOUSEBUTTONDOWN:
                if paused and pause_quit_button.check_if_collided(pg.mouse.get_pos()):
                    if records["high_score"] < score:
                        records["high_score"] = score
                    dump_into_table(records, 'records.json')
                    return
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                player.bomb()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                paused = not paused
        # Summons

        # COLLISIONS GO HERE
        enemy_collision = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
        # Items
        item_collision = pg.sprite.spritecollide(player, items, True)
        midboss_player_collision = pg.sprite.collide_rect(player, midboss)
        midboss_collision = pg.sprite.spritecollide(midboss, shots, True, pg.sprite.collide_circle)
        midboss_bomb_collision = pg.sprite.spritecollide(midboss, bomb_shots, False, pg.sprite.collide_circle)

        # Enemy death

        # Enemy death (with bombs)
        shot_collision2 = pg.sprite.groupcollide(bomb_shots, enemies, False, True, pg.sprite.collide_circle)
        # Player death
        bullet_collision = pg.sprite.spritecollide(player, bullets, True, pg.sprite.collide_circle)
        if len(bomb_shots) != 0:
            clear_bullets()
        for collision in enemy_collision:
            if not player.invincible:  # Checks if the player is invincible
                kill_player(player, collision)
        if midboss_player_collision:
            if not player.invincible:  # Checks if the player is invincible
                kill_player(player, player)
        for collision in midboss_collision:
            score += 50
            midboss.health -= collision.damage
        for collision in midboss_bomb_collision:
            score += 50
            midboss.health -= collision.damage
        if stage1_boss.alive() and counter > 4800:
            boss_collision = pg.sprite.spritecollide(stage1_boss, shots, True, pg.sprite.collide_circle)
            boss_bomb_collision = pg.sprite.spritecollide(stage1_boss, bomb_shots, False, pg.sprite.collide_circle)
            for collision in boss_collision:
                if stage1_boss.attack_state:
                    score += 50
                    stage1_boss.health -= collision.damage
            for collision in boss_bomb_collision:
                if stage1_boss.attack_state:
                    score += 50
                    stage1_boss.health -= collision.damage / 2
        for enemy in enemies:
            for shot in shots:
                if pg.sprite.collide_rect(enemy, shot):
                    enemy.health -= shot.damage
                    shot.kill()
                    if enemy.health < 0:
                        play_sound("enemy_death", volume=.5)
                        summon_explosion(enemy.rect.center)
                        score += randint(100, 500)
                        spawn_item(enemy.rect.center, 0)
                        for i in range(randint(1, 6)):
                            spawn_item(determine_center(enemy), 1)
        for collision in shot_collision2:
            play_sound("enemy_death", volume=.5)
            summon_explosion(collision.rect.center)
            score += randint(100, 500)
            spawn_item(collision.rect.center, 0)
            for i in range(randint(1, 6)):
                spawn_item(determine_center(collision), 1)
        for collision in bullet_collision:
            if not player.invincible:
                kill_player(player, collision)
        for collision in item_collision:
            play_sound("power")
            if collision.type == "power":
                if player.power != 4:
                    player.power += .05
                    # Will round the player power to 2 decimal places.
                    player.power = float('%.2f' % player.power)
            if collision.type == "point":
                player.level += 1
                score += 200
            if collision.type == "bomb":
                play_sound('gain')
                player.bombs += 1

        pg.display.update()
        # Draws stuff on the screen.

        clock.tick(60)


def stage2_loop(player, score):
    """
    Main loop.
    """

    pause_quit_button = Button((width / 2, 2 * height / 3), buttons[2])
    play_music("music5.ogg")
    background1 = Background(backgrounds2[0], -1)
    background2 = Background(backgrounds2[1], -4)
    background3 = Background(backgrounds2[2], -2)
    background4 = Background(backgrounds2[3], 0)  # Scrolling background loader.
    background4.background_image.set_alpha(0)
    stage2_boss = Boss2(False)
    # Variables
    last = pg.time.get_ticks()
    last2 = pg.time.get_ticks()
    stage = True
    crashed = False
    paused = False
    first_box = TextBox((186, 566), 22, 3, stage2_boss, dlg_3, music="music6.ogg")
    second_box = TextBox((186, 566), 50, 50, None, dlg_4)
    counter = 0
    enemy_location = game_area.left + 20
    delay = 1000
    alpha = 0
    while not crashed:
        screen.fill(white)
        if not paused:
            counter += 1

            background1.update()
            background4.render()
            background2.update()

            all_sprites.draw(screen)
            all_sprites.update()
            background3.update()
            all_sprites.add(player)
            if enemy_location > width:
                enemy_location = game_area.left + 20
            if counter % 20 == 0 and counter > 2000:
                alpha += 5
                background4.background_image.set_alpha(alpha)
            now = pg.time.get_ticks()
            if now - last2 > 5000 and stage:
                last2 = now
                if 100 < counter < 1000 or 4000 > counter > 3000:
                    e = Enemy(enemy2[0], 6, game_area.left + 100, -25, 0, 2, health=60)
                    e2 = Enemy(enemy2[0], 7, game_area.right - 100, -25, 0, 2, health=60)
                    all_sprites.add(e, e2)
                    enemies.add(e, e2)
                elif 5000 > counter > 4000:
                    position, enemy_speed = choice([(game_area.left, 3), (game_area.right, -3)])
                    e = Enemy(enemy1[1], 9, position, randint(40, int(width / 3)), enemy_speed, 0, health=50)
                    all_sprites.add(e)
                    enemies.add(e)
            if now - last > delay and stage:
                last = now
                if 1000 <= counter < 1800:
                    position, enemy_speed = choice([(game_area.left, 5), (game_area.right, -5)])
                    e = Enemy(enemy1[1], 8, position, randint(40, int(width / 3)), enemy_speed, 0, health=20)
                    all_sprites.add(e)
                    enemies.add(e)
                elif 5000 > counter > 1800:
                    spawn_enemy_randomly(choice(enemy1), randint(10, 11), 2, health=40)
            if counter == 5000:
                clear_bullets()
                clear_enemies()
                stage = False

            if counter == 5000:
                all_sprites.add(first_box)
            if counter > 5000 and stage2_boss.health <= 0:
                all_sprites.add(second_box)
            if counter > 5000 and stage2_boss.health <= 0 and second_box.i > len(dlg_4):
                second_box.kill()
                fade_in()
                game = stage3_loop(player, score)
                return game
            # SPRITE AND DISPLAY UPDATES
            pause_quit_button.kill()
            draw_stage_data(player, score)

            if 1 < counter < 2000:
                draw_text(screen, f'{translation["stage2title1"]}', (786, 22))
            elif 2000 <= counter < 4000:
                draw_text(screen, f'{translation["stage2title2"]}', (786, 22))
            elif counter >= 4000:
                draw_text(screen, f'{translation["stage2title3"]}', (786, 22))

        if paused:

            all_sprites.add(pause_quit_button)
            background1.render()
            background2.render()
            screen.blit(bomb_bg, screen.get_rect())
            all_sprites.draw(screen)
            background3.render()
            draw_stage_data(player, score)
            if 1 < counter < 2000:
                draw_text(screen, f'{translation["stage2title1"]}', (786, 22))
            elif 2000 <= counter < 4000:
                draw_text(screen, f'{translation["stage2title2"]}', (786, 22))
            elif counter >= 4000:
                draw_text(screen, f'{translation["stage2title3"]}', (786, 22))
            draw_centered_text(screen, f'{translation["paused"]}', game_area.center, font_3)
        # Lives
        if player.lives < 0:
            if records["high_score"] < score:
                records["high_score"] = score
            dump_into_table(records, 'records.json')
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if records["high_score"] < score:
                    records["high_score"] = score
                dump_into_table(records, 'records.json')
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if first_box.i - 1 < len(dlg_1) and first_box.alive():
                    first_box.i += 1
            # Bomb event is here.
            if event.type == pg.MOUSEBUTTONDOWN and paused and pause_quit_button.check_if_collided(pg.mouse.get_pos()):
                if records["high_score"] < score:
                    records["high_score"] = score
                dump_into_table(records, 'records.json')
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                player.bomb()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                paused = not paused
        # Summons

        # COLLISIONS GO HERE
        enemy_collision = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
        # Items
        item_collision = pg.sprite.spritecollide(player, items, True)

        # Enemy death

        # Enemy death (with bombs)
        shot_collision2 = pg.sprite.groupcollide(bomb_shots, enemies, False, True, pg.sprite.collide_circle)
        # Player death
        bullet_collision = pg.sprite.spritecollide(player, bullets, True, pg.sprite.collide_circle)
        if len(bomb_shots) != 0:
            clear_bullets()
        for collision in enemy_collision:
            if not player.invincible:  # Checks if the player is invincible
                kill_player(player, collision)

        if stage2_boss.alive() and counter > 4800:
            boss_collision = pg.sprite.spritecollide(stage2_boss, shots, True, pg.sprite.collide_circle)
            boss_bomb_collision = pg.sprite.spritecollide(stage2_boss, bomb_shots, False, pg.sprite.collide_circle)
            for collision in boss_collision:
                if stage2_boss.attack_state:
                    score += 50
                    stage2_boss.health -= collision.damage
            for collision in boss_bomb_collision:
                if stage2_boss.attack_state:
                    score += 50
                    stage2_boss.health -= collision.damage
        for enemy in enemies:
            for shot in shots:
                if pg.sprite.collide_rect(enemy, shot):
                    enemy.health -= shot.damage
                    shot.kill()
                    if enemy.health < 0:
                        play_sound("enemy_death", volume=.5)
                        summon_explosion(enemy.rect.center)
                        score += randint(100, 500)
                        spawn_item(enemy.rect.center, 0)
                        for i in range(randint(1, 6)):
                            spawn_item(determine_center(enemy), 1)
        for collision in shot_collision2:
            play_sound("enemy_death", volume=.5)
            summon_explosion(collision.rect.center)
            score += randint(100, 500)
            spawn_item(collision.rect.center, 0)
            for i in range(randint(1, 6)):
                spawn_item(determine_center(collision), 1)
        for collision in bullet_collision:
            if not player.invincible:
                kill_player(player, collision)
        for collision in item_collision:
            play_sound("power")
            if collision.type == "power":
                if player.power != 4:
                    player.power += .05
                    # Will round the player power to 2 decimal places.
                    player.power = float('%.2f' % player.power)
            if collision.type == "point":
                player.level += 1
                score += 200
            if collision.type == "bomb":
                play_sound('gain')
                player.bombs += 1
        pg.display.update()

        # Draws stuff on the screen.
        screen.fill(white)
        clock.tick(60)


def stage3_loop(player, score):
    """
    Main loop.
    """

    pause_quit_button = Button((width / 2, 2 * height / 3), buttons[2])
    play_music("music7.ogg")
    background1 = Background(backgrounds3[0], -1)
    background2 = Background(backgrounds3[1], -2)
    background3 = Background(backgrounds3[2], -2)
    stage3_boss = Boss3(False)
    # Variables
    last = pg.time.get_ticks()
    last2 = pg.time.get_ticks()
    stage = True
    crashed = False
    paused = False
    first_box = TextBox((186, 566), len(dlg_5) - 2, 5, stage3_boss, dlg_5, music="music9.ogg")
    second_box = TextBox((186, 566), 50, 50, None, dlg_6, music=None)
    counter = 0
    enemy_location = game_area.left + 20
    delay = 1500
    while not crashed:
        screen.fill(black)
        if not paused:
            counter += 1

            background1.update()
            background2.update()
            background3.update()
            all_sprites.draw(screen)
            all_sprites.update()
            all_sprites.add(player)
            if enemy_location > width:
                enemy_location = game_area.left + 20
            now = pg.time.get_ticks()
            if now - last2 > 5000 and stage:
                last2 = now
                if 1 < counter < 1000:
                    e = Enemy(enemy2[0], 12, game_area.centerx, -25, 0, 1, health=500)
                    all_sprites.add(e)
                    enemies.add(e)
                elif 1000 < counter < 2000:
                    e = Enemy(enemy2[1], 13, game_area.left + 20, -25, 0, 1, health=100)
                    e2 = Enemy(enemy2[1], 13, game_area.right - 20, -25, 0, 1, health=100)
                    all_sprites.add(e, e2)
                    enemies.add(e, e2)
                elif 7800 > counter > 6000:
                    spawn_enemy_randomly(choice(enemy1), 15, 4, health=40)
            if now - last > delay and stage:
                last = now
                if 2000 < counter < 4000:
                    spawn_enemy_randomly(choice(enemy1), 15, 2, health=40)
                if 4000 <= counter < 6000:
                    position, enemy_speed = choice([(game_area.left + 50, randint(1, 10)),
                                                    (game_area.right - 50, randint(-10, -1))])
                    e = Enemy(enemy1[1], 14, position, randint(40, int(width / 3)), enemy_speed, 0, health=150)
                    all_sprites.add(e)
                    enemies.add(e)
            if counter == 7800:
                clear_bullets()
                clear_enemies()
                stage = False

            if counter == 7800:
                all_sprites.add(first_box)
            if counter > 7800 and stage3_boss.health <= 0:
                all_sprites.add(second_box)
            if counter > 7800 and stage3_boss.health <= 0 and second_box.i > len(dlg_6) - 1:
                second_box.kill()
                fade_in()
                game = stage4_loop(player, score)
                return game
            '''
            if counter > 7800 and stage2_boss.health <= 0:
                all_sprites.add(second_box)
            if counter > 7800 and stage2_boss.health <= 0 and second_box.i > len(dlg_4):
                draw_text(screen, "STAGE CLEAR", (385, 250), font_3)
                second_box.kill()
                return'''
            # SPRITE AND DISPLAY UPDATES
            pause_quit_button.kill()
            draw_stage_data(player, score)
            if 1 < counter < 3000:
                draw_text(screen, f'{translation["stage3title1"]}', (786, 22))
            elif 3000 <= counter < 7800:
                draw_text(screen, f'{translation["stage3title2"]}', (786, 22))
            elif counter >= 7800:
                draw_text(screen, f'{translation["stage3title3"]}', (786, 22))

        if paused:

            all_sprites.add(pause_quit_button)
            background1.render()
            background2.render()
            background3.render()
            screen.blit(bomb_bg, screen.get_rect())
            all_sprites.draw(screen)
            draw_stage_data(player, score)
            if 1 < counter < 3000:
                draw_text(screen, f'{translation["stage3title1"]}', (786, 22))
            elif 3000 <= counter < 7800:
                draw_text(screen, f'{translation["stage3title2"]}', (786, 22))
            elif counter >= 7800:
                draw_text(screen, f'{translation["stage3title3"]}', (786, 22))
            draw_centered_text(screen, f'{translation["paused"]}', game_area.center, font_3)
        # Lives
        if player.lives < 0:
            if records["high_score"] < score:
                records["high_score"] = score
            dump_into_table(records, 'records.json')
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if records["high_score"] < score:
                    records["high_score"] = score
                dump_into_table(records, 'records.json')
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if first_box.i - 1 < len(dlg_1) and first_box.alive():
                    first_box.i += 1
            # Bomb event is here.
            if event.type == pg.MOUSEBUTTONDOWN:
                if paused and pause_quit_button.check_if_collided(pg.mouse.get_pos()):
                    if records["high_score"] < score:
                        records["high_score"] = score
                    dump_into_table(records, 'records.json')
                    return
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                player.bomb()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                paused = not paused
        # Summons

        # COLLISIONS GO HERE
        enemy_collision = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
        # Items
        item_collision = pg.sprite.spritecollide(player, items, True)

        # Enemy death

        # Enemy death (with bombs)
        shot_collision2 = pg.sprite.groupcollide(bomb_shots, enemies, False, True, pg.sprite.collide_circle)
        # Player death
        bullet_collision = pg.sprite.spritecollide(player, bullets, True, pg.sprite.collide_circle)
        if len(bomb_shots) != 0:
            clear_bullets()
        for collision in enemy_collision:
            if not player.invincible:  # Checks if the player is invincible
                kill_player(player, collision)
        if stage3_boss.alive() and counter > 4800:
            boss_collision = pg.sprite.spritecollide(stage3_boss, shots, True, pg.sprite.collide_circle)
            boss_bomb_collision = pg.sprite.spritecollide(stage3_boss, bomb_shots, False, pg.sprite.collide_circle)
            for collision in boss_collision:
                if stage3_boss.attack_state:
                    stage3_boss.health -= collision.damage
            for collision in boss_bomb_collision:
                if stage3_boss.attack_state:
                    stage3_boss.health -= collision.damage
        for enemy in enemies:
            for shot in shots:
                if pg.sprite.collide_rect(enemy, shot):
                    enemy.health -= shot.damage
                    shot.kill()
                    if enemy.health < 0:
                        play_sound("enemy_death", volume=.5)
                        summon_explosion(enemy.rect.center)
                        score += randint(100, 500)
                        spawn_item(enemy.rect.center, 0)
                        for i in range(randint(1, 6)):
                            spawn_item(determine_center(enemy), 1)
        for collision in shot_collision2:
            play_sound("enemy_death", volume=.5)
            summon_explosion(collision.rect.center)
            score += randint(100, 500)
            spawn_item(collision.rect.center, 0)
            for i in range(randint(1, 6)):
                spawn_item(determine_center(collision), 1)
        for collision in bullet_collision:
            if not player.invincible:
                kill_player(player, collision)
        for collision in item_collision:
            play_sound("power")
            if collision.type == "power":
                if player.power != 4:
                    player.power += .05
                    # Will round the player power to 2 decimal places.
                    player.power = float('%.2f' % player.power)
            if collision.type == "point":
                player.level += 1
                score += 200
            if collision.type == "bomb":
                play_sound('gain')
                player.bombs += 1

        pg.display.update()

        # Draws stuff on the screen.
        clock.tick(60)


def stage4_loop(player, score):
    """
    Main loop.
    """

    pause_quit_button = Button((width / 2, 2 * height / 3), buttons[2])
    play_music("music10.ogg")
    background1 = Background(backgrounds4[1], -1)
    background2 = Background(backgrounds4[0], -10)
    background3 = Background(backgrounds4[2], -6)
    background4 = Background(backgrounds4[3], 0)
    background4.background_image.set_alpha(0)
    bg_alpha = 0
    midboss = Midboss2()
    stage4_boss = Boss4(False)
    # Variables
    last = pg.time.get_ticks()
    last2 = pg.time.get_ticks()
    stage = True
    crashed = False
    paused = False
    first_box = TextBox((186, 566), len(dlg_7) - 1, 5, stage4_boss, dlg_7, music="music11.ogg")
    second_box = TextBox((186, 566), 80, 5, None, dlg_8)
    counter = 0
    enemy_location = game_area.left + 20
    delay = 1500
    while not crashed:
        screen.fill(black)

        if not paused:
            if counter > 8000:
                background4.background_image.set_alpha(bg_alpha)
                bg_alpha += 0.5

            if counter == 4800:
                all_sprites.add(midboss)
                stage = False
                clear_bullets()
                clear_enemies()
            if counter > 4800 and midboss.health < 0:
                stage = True

            counter += 1
            background1.update()
            background2.update()
            background3.update()
            background4.update()
            all_sprites.draw(screen)
            all_sprites.update()
            all_sprites.add(player)
            if enemy_location > width:
                enemy_location = game_area.left + 20
            now = pg.time.get_ticks()
            if now - last2 > 4000 and stage:
                last2 = now
                if 1 < counter < 1000:
                    e = Enemy(enemy3[2], 16, game_area.centerx - 50, -25, 0, 1, health=200, do_rotate=True)
                    e2 = Enemy(enemy3[2], 16, game_area.centerx + 50, -25, 0, 1, health=200, do_rotate=True)
                    all_sprites.add(e, e2)
                    enemies.add(e, e2)
                elif 1000 < counter < 3000:
                    e = Enemy(enemy3[1], 18, game_area.left + 100, -25, 0, 2, health=100)
                    e2 = Enemy(enemy3[2], 17, game_area.centerx, -25, 0, 1, health=400, do_rotate=True)
                    e3 = Enemy(enemy3[1], 18, game_area.right - 100, -25, 0, 2, health=100)
                    e3.thread.increase = -5
                    all_sprites.add(e, e2, e3)
                    enemies.add(e, e2, e3)
                elif 8000 < counter < 10400:
                    spawn_enemy_randomly(enemy3[0], 20, 10, health=40)
            if now - last > delay and stage:
                last = now
                if 3000 <= counter < 6000:
                    position, enemy_speed = choice([(game_area.left + 10, randint(1, 3)),
                                                    (game_area.right - 10, randint(-3, -1))])
                    e = Enemy(enemy3[1], 21, position, randint(40, int(width / 3)), enemy_speed, 0, health=150)
                    all_sprites.add(e)
                    enemies.add(e)
                if 6000 <= counter < 8000:
                    position, enemy_speed = choice([(game_area.left + 50, randint(5, 10)),
                                                    (game_area.right - 50, randint(-10, -5))])
                    e = Enemy(enemy3[1], 22, position, randint(40, int(width / 3)), enemy_speed, 0, health=150)
                    all_sprites.add(e)
                    enemies.add(e)

            if counter == 10400:
                all_sprites.add(first_box)
                clear_bullets()
                clear_enemies()
                stage = False

            # SPRITE AND DISPLAY UPDATES
            pause_quit_button.kill()
            draw_stage_data(player, score)
            if 1 < counter < 5000:
                draw_text(screen, f'{translation["stage4title1"]}', (786, 22))
            elif 5000 <= counter < 8000:
                draw_text(screen, f'{translation["stage4title2"]}', (786, 22))
            elif counter >= 8000:
                draw_text(screen, f'{translation["stage4title3"]}', (786, 22))

        if paused:

            all_sprites.add(pause_quit_button)
            background1.render()
            background2.render()
            background3.render()
            background4.render()
            screen.blit(bomb_bg, screen.get_rect())
            all_sprites.draw(screen)
            draw_stage_data(player, score)
            if 1 < counter < 5000:
                draw_text(screen, f'{translation["stage4title1"]}', (786, 22))
            elif 5000 <= counter < 8000:
                draw_text(screen, f'{translation["stage4title2"]}', (786, 22))
            elif counter >= 8000:
                draw_text(screen, f'{translation["stage4title3"]}', (786, 22))
            draw_centered_text(screen, f'{translation["paused"]}', game_area.center, font_3)
        # Lives
        if player.lives < 0:
            if records["high_score"] < score:
                records["high_score"] = score
            dump_into_table(records, 'records.json')
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if records["high_score"] < score:
                    records["high_score"] = score
                dump_into_table(records, 'records.json')
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if first_box.i - 1 < len(dlg_1) and first_box.alive():
                    first_box.i += 1
            # Bomb event is here.
            if event.type == pg.MOUSEBUTTONDOWN:
                if paused and pause_quit_button.check_if_collided(pg.mouse.get_pos()):
                    if records["high_score"] < score:
                        records["high_score"] = score
                    dump_into_table(records, 'records.json')
                    return
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                player.bomb()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                paused = not paused
        # Summons
        # COLLISIONS GO HERE
        enemy_collision = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
        # Items
        item_collision = pg.sprite.spritecollide(player, items, True)

        # Enemy death
        if counter > 10400 and stage4_boss.health <= 0:
            all_sprites.add(second_box)
        if counter > 10400 and stage4_boss.health <= 0 and second_box.i > len(dlg_8) - 1:
            second_box.kill()
            fade_in()
            game = stage5_loop(player, score)
            return game
        # Enemy death (with bombs)
        shot_collision2 = pg.sprite.groupcollide(bomb_shots, enemies, False, True, pg.sprite.collide_circle)
        # Player death
        bullet_collision = pg.sprite.spritecollide(player, bullets, True, pg.sprite.collide_circle)
        if len(bomb_shots) != 0:
            clear_bullets()
        for collision in enemy_collision:
            if not player.invincible:  # Checks if the player is invincible
                kill_player(player, collision)
        if stage4_boss.alive() and counter > 4800:
            boss_collision = pg.sprite.spritecollide(stage4_boss, shots, True, pg.sprite.collide_circle)
            boss_bomb_collision = pg.sprite.spritecollide(stage4_boss, bomb_shots, False, pg.sprite.collide_circle)
            for collision in boss_collision:
                if stage4_boss.attack_state:
                    stage4_boss.health -= collision.damage
            for collision in boss_bomb_collision:
                if stage4_boss.attack_state:
                    stage4_boss.health -= collision.damage
        if midboss.alive() and counter > 4800:
            boss_collision = pg.sprite.spritecollide(midboss, shots, True, pg.sprite.collide_circle)
            boss_bomb_collision = pg.sprite.spritecollide(midboss, bomb_shots, False, pg.sprite.collide_circle)
            for collision in boss_collision:
                midboss.health -= collision.damage
            for collision in boss_bomb_collision:
                midboss.health -= collision.damage
        for enemy in enemies:
            for shot in shots:
                if pg.sprite.collide_rect(enemy, shot):
                    enemy.health -= shot.damage
                    shot.kill()
                    if enemy.health < 0:
                        play_sound("enemy_death", volume=.5)
                        summon_explosion(enemy.rect.center)
                        score += randint(100, 500)
                        spawn_item(enemy.rect.center, 0)
                        for i in range(randint(1, 6)):
                            spawn_item(determine_center(enemy), 1)
        for collision in shot_collision2:
            play_sound("enemy_death", volume=.5)
            summon_explosion(collision.rect.center)
            score += randint(100, 500)
            spawn_item(collision.rect.center, 0)
            for i in range(randint(1, 6)):
                spawn_item(determine_center(collision), 1)
        for collision in bullet_collision:
            if not player.invincible:
                kill_player(player, collision)
        for collision in item_collision:
            play_sound("power")
            if collision.type == "power":
                if player.power != 4:
                    player.power += .05
                    # Will round the player power to 2 decimal places.
                    player.power = float('%.2f' % player.power)
            if collision.type == "point":
                player.level += 1
                score += 200
            if collision.type == "bomb":
                play_sound('gain')
                player.bombs += 1

        pg.display.update()

        # Draws stuff on the screen.
        clock.tick(60)


def stage5_loop(player, score):
    """
    Main loop.
    """

    pause_quit_button = Button((width / 2, 2 * height / 3), buttons[2])
    play_music("music12.ogg")
    background1 = Background(backgrounds5[0], 0)
    background2 = Background(backgrounds5[1], -5)
    background3 = Background(backgrounds5[2], 0)
    background3.background_image.set_alpha(0)
    stage5_boss = Boss5(False)
    # Variables
    last = pg.time.get_ticks()
    stage = True
    crashed = False
    paused = False
    first_box = TextBox((186, 566), len(dlg_9) - 2, 5, stage5_boss, dlg_9, music="music13.ogg")
    counter = 0
    enemy_location = game_area.left + 20
    delay = 5000
    end_counter = 0
    while not crashed:
        if not paused:
            counter += 1

            background1.update()
            background3.update()
            background2.update()
            all_sprites.draw(screen)
            all_sprites.add(player)
            all_sprites.update()
            if enemy_location > width:
                enemy_location = game_area.left + 20
            now = pg.time.get_ticks()
            if now - last > delay and stage:
                last = now
                spawn_enemy_randomly(choice(enemy1), 23, 3, health=75)

            if counter == 6500:
                clear_bullets()
                clear_enemies()
                stage = False

            if counter == 6500:
                all_sprites.add(first_box)

            if counter > 6500 and first_box.i >= 13 and stage5_boss.health != 15000:
                background3.background_image.set_alpha((15000 - stage5_boss.health) / 15000 * 255)
            if counter > 6500 and first_box.i >= 13 and stage5_boss.health < 0:
                end_counter += 1
                all_sprites.add()
            if counter > 6500 and first_box.i >= 13 and stage5_boss.health < 0 and end_counter > 500:
                fade_in()
                if records["high_score"] < score:
                    records["high_score"] = score
                if isinstance(player, PlayerA):
                    records["a_cleared"] = True
                if isinstance(player, PlayerB):
                    records["b_cleared"] = True
                if isinstance(player, PlayerC):
                    records["c_cleared"] = True
                dump_into_table(records, 'records.json')
                return [True, score, player, player.deaths]
            # SPRITE AND DISPLAY UPDATES
            pause_quit_button.kill()
            draw_stage_data(player, score)
            draw_text(screen, f'{translation["stage5title"]}', (786, 22))

        if paused:

            all_sprites.add(pause_quit_button)
            background1.render()
            background3.render()
            background2.render()
            screen.blit(bomb_bg, screen.get_rect())
            all_sprites.draw(screen)
            draw_stage_data(player, score)
            draw_text(screen, f'{translation["stage5title"]}', (786, 22))
            draw_centered_text(screen, f'{translation["paused"]}', game_area.center, font_3)
        # Lives
        if player.lives < 0:
            if records["high_score"] < score:
                records["high_score"] = score
            dump_into_table(records, 'records.json')
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if records["high_score"] < score:
                    records["high_score"] = score
                dump_into_table(records, 'records.json')
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if first_box.i - 1 < len(dlg_1) and first_box.alive():
                    first_box.i += 1
            # Bomb event is here.
            if event.type == pg.MOUSEBUTTONDOWN:
                if paused and pause_quit_button.check_if_collided(pg.mouse.get_pos()):
                    if records["high_score"] < score:
                        records["high_score"] = score
                    dump_into_table(records, 'records.json')
                    return
            if event.type == pg.KEYDOWN and event.key == pg.K_x:
                player.bomb()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                paused = not paused
        # Summons

        # COLLISIONS GO HERE
        enemy_collision = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
        # Items
        item_collision = pg.sprite.spritecollide(player, items, True)

        # Enemy death

        # Enemy death (with bombs)
        shot_collision2 = pg.sprite.groupcollide(bomb_shots, enemies, False, True, pg.sprite.collide_circle)
        # Player death
        bullet_collision = pg.sprite.spritecollide(player, bullets, True, pg.sprite.collide_circle)
        if len(bomb_shots) != 0:
            clear_bullets()
        for collision in enemy_collision:
            if not player.invincible:  # Checks if the player is invincible
                kill_player(player, collision)
        if stage5_boss.alive() and counter > 6500:
            boss_collision = pg.sprite.spritecollide(stage5_boss, shots, True, pg.sprite.collide_circle)
            boss_bomb_collision = pg.sprite.spritecollide(stage5_boss, bomb_shots, False, pg.sprite.collide_circle)
            for collision in boss_collision:
                if stage5_boss.attack_state:
                    stage5_boss.health -= collision.damage
            for collision in boss_bomb_collision:
                if stage5_boss.attack_state:
                    stage5_boss.health -= collision.damage / 2
        for enemy in enemies:
            for shot in shots:
                if pg.sprite.collide_rect(enemy, shot):
                    enemy.health -= shot.damage
                    shot.kill()
                    if enemy.health < 0:
                        play_sound("enemy_death", volume=.5)
                        summon_explosion(enemy.rect.center)
                        score += randint(100, 500)
                        spawn_item(enemy.rect.center, 0)
                        for i in range(randint(1, 6)):
                            spawn_item(determine_center(enemy), 1)
        for collision in shot_collision2:
            play_sound("enemy_death", volume=.5)
            summon_explosion(collision.rect.center)
            score += randint(100, 500)
            spawn_item(collision.rect.center, 0)
            for i in range(randint(1, 6)):
                spawn_item(determine_center(collision), 1)
        for collision in bullet_collision:
            if not player.invincible:
                kill_player(player, collision)
        for collision in item_collision:
            play_sound("power")
            if collision.type == "power":
                if player.power != 4:
                    player.power += .05
                    # Will round the player power to 2 decimal places.
                    player.power = float('%.2f' % player.power)
            if collision.type == "point":
                player.level += 1
                score += 200
            if collision.type == "bomb":
                play_sound('gain')
                player.bombs += 1

        pg.display.update()

        # Draws stuff on the screen.
        screen.fill(black)
        clock.tick(60)
