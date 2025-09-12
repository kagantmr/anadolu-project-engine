from constants import *

global playing_music
playing_music = False


def play_music(file_name, loop=-1):
    pg.mixer.music.pause()
    pg.mixer.pre_init()
    pg.mixer.music.load(path.join(music_folder, file_name))
    pg.mixer.music.play(loops=loop)


def play_sound(effect, volume=0.1):
    pg.mixer.pre_init()
    sound = pg.mixer.Sound(path.join(sound_effect_folder, "se_" + effect + ".wav"))
    sound.set_volume(volume)
    pg.mixer.find_channel(True).play(sound)