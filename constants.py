
# IMPORTS ---------------------------
from json import load, dump
from os import path, environ
from sys import exit
from platform import system
from random import *
import pygame as pg
# -----------------------------------

pg.init()
pg.font.init()
info = pg.display.Info()

""" I have no genuine idea what this was for, maybe at some point it was for OpenGL testing? Because 
    at some point I did try to use OpenGL to render backgrounds for some reason... keeping it though
    bcuz I think it helped with fullscreen (which I kind of don't want to support anymore)."""
if system() == 'Windows':
    environ['SDL_VIDEODRIVER'] = 'windib'

class EngineError(Exception):
    pass


asset_folder = path.join(path.dirname(__file__), "assets")


def read_from_table(file: str) -> dict:
    """
    Wrapper around open() and json.load(), used in dialogue and ending cutscene routines.
    
    Parameters:
        file (str): Name of the file to load located in "assets/".
        
    Returns:
        dict: Parsed JSON contents of the file.
    """
    with open(path.join(asset_folder, file), 'r', encoding='utf-8') as file:
        return load(file)


def dump_into_table(content: dict, file: str) -> None:
    """
    Wrapper around open() and json.dump(), used to save progress.
    
    Parameters:
        content (dict): The data to dump as a dict.
        file (str): Name of the file to load located in "assets/".
        
    Returns:
        dict: Parsed JSON contents of the file.
    """
    with open(path.join(asset_folder, file), 'w', encoding='utf-8') as file:
        return dump(content, file)

def load_font(font_name, size) -> pg.font.Font:
    return pg.font.Font(path.join(font_folder, font_name + ".ttf"), size)

translation = read_from_table('translation_table.json') # Load preferred translation file
records = read_from_table('records.json') # Load the previous records (Currently has problems)
full_screen = False # Due to issues with Tkinter full screen mode is disabled for now





# ------------------------------------------------------------------------------------ Folder variables.
game_folder = path.abspath(__file__)
img_folder = path.join(path.dirname(__file__), "assets", "img")
player_folder = path.join(path.dirname(__file__), "assets", "img", "player")
projectile_folder = path.join(path.dirname(__file__), "assets", "img", "projectiles")
enemy_folder = path.join(path.dirname(__file__), "assets", "img", "enemy")
effect_folder = path.join(path.dirname(__file__), "assets", "img", "effects")
background_folder = path.join(path.dirname(__file__), "assets", "img", "backgrounds")
music_folder = path.join(path.dirname(__file__), "assets", "snd", "music")
sound_effect_folder = path.join(path.dirname(__file__), "assets", "snd", "se")
font_folder = path.join(path.dirname(__file__), "assets", "font")
gui_folder = path.join(path.dirname(__file__), "assets", "img", "gui")
boss_folder = path.join(path.dirname(__file__), "assets", "img", "bosses")
dialogue_folder = path.join(path.dirname(__file__), "assets", "dialogue")
portrait_folder = path.join(path.dirname(__file__), "assets", "img", "portraits")
ending_folder = path.join(path.dirname(__file__), "assets", "img", "endings")
# ------------------------------------------------------------------------------------------------------

def determine_center(collision: pg.sprite.Sprite) -> tuple:
    """
    Returns a random point in the range of 20 pixels around the bounding box of the sprite, to display animation effects. 
    Could be inlined later? Turned into a lambda function?
    
    Parameters:
        collision (pg.sprite.Sprite): The colliding sprite.
        
    Returns:
        tuple: The random point to display animations in.
    """
    return randint(collision.rect.left - 20, collision.rect.right + 20), randint(collision.rect.top - 20, collision.rect.bottom + 20)



def read_dialogue(file_name: str, encoding: str = 'utf-8') -> list[str]:
    """
    Reads a .dlg file into a list. The .dlg files are formatted as lines in the format of "location:image_name:text".
    
    
    Parameters:
        file_name (str): The name of the .dlg file to open.
        encoding (str, optional): The type of encoding. Default is utf-8.
        
    Returns:
        list[str]: The parsed dialogue in lines.
    """
    with open(file_name, 'r', encoding=encoding) as file:
        new_text = []
        for text_line in file.readlines():
            new_text.append(text_line.strip("\n").split(':', 2))
        return new_text


# Function to load images.

def load_image(start, stop, folder, image_name, extension=".png"):
    image_list = []
    if start == stop:  # If start and stop values are equal, take the image name and add it the .png extension.
        image = pg.image.load(path.join(folder, image_name + extension)).convert_alpha()
        return image  # Return the image.
    else:  # Otherwise do a list of the loaded files.
        for i in range(start, stop + 1):
            image = pg.image.load(path.join(folder, image_name + str(i) + extension)).convert_alpha()
            image_list.append(image)
        return image_list  # Return the list of images.


# Sprite groups.
all_sprites = pg.sprite.Group()
shots = pg.sprite.Group()
enemies = pg.sprite.Group()
bullets = pg.sprite.Group()
items = pg.sprite.Group()
bomb_shots = pg.sprite.Group()

# Screen cover size.
game_area = pg.Rect(180, 22, 599, 674)
# Boss variables


# Screen-related variables
width = 960
height = 720

screen = pg.display.set_mode((width, height), pg.HWSURFACE | pg.HWACCEL, vsync=1)
info = pg.display.Info()


# Sprite images.
player_sprite = load_image(0, 0, player_folder, "player0")
player_sprite_left = load_image(0, 0, player_folder, "player1")
player_sprite_right = load_image(0, 0, player_folder, "player2")

explosion_sprite = load_image(0, 4, effect_folder, "explosion")

shot1 = load_image(0, 0, player_folder, "bullet1")
shot2 = load_image(0, 0, player_folder, "bullet2")
shot3 = load_image(3, 5, player_folder, "bullet")
shot4 = load_image(0, 0, player_folder, "bullet6")

bomb_sprites = load_image(1, 3, player_folder, "bomb")

enemy1 = load_image(1, 2, enemy_folder, "enemy")
enemy2 = load_image(3, 5, enemy_folder, "enemy")
enemy3 = load_image(5, 8, enemy_folder, "enemy")
enemy4 = load_image(8, 10, enemy_folder, "enemy")

boss1 = load_image(1, 2, boss_folder, "boss1_")
boss2 = load_image(1, 2, boss_folder, "boss2_")
boss3 = load_image(1, 2, boss_folder, "boss3_")
boss4 = load_image(1, 2, boss_folder, "boss4_")
boss5 = load_image(1, 2, boss_folder, "boss5_")

circular_bullet_images = load_image(1, 11, projectile_folder, "bullet")
pointed_bullet_images = load_image(12, 29, projectile_folder, "bullet")

item_sprites = load_image(1, 5, projectile_folder, "item")

bomb_bg = load_image(0, 0, background_folder, 'bomb')
backgrounds1 = load_image(1, 2, background_folder, 'background')
backgrounds2 = load_image(3, 6, background_folder, 'background')
backgrounds3 = load_image(7, 9, background_folder, 'background')
backgrounds4 = load_image(10, 13, background_folder, 'background')
backgrounds5 = load_image(14, 16, background_folder, 'background')

cover = load_image(0, 0, gui_folder, "cover")
stat_images = load_image(1, 5, gui_folder, "gui_")
buttons = load_image(1, 6, gui_folder, "button")
shot_types = load_image(1, 3, gui_folder, "type")
menu_background = load_image(0, 0, gui_folder, "menu_background")
background_shade = load_image(0, 0, gui_folder, "shade")
silhouette = load_image(0, 0, gui_folder, "silhouette")
textbox = load_image(0, 0, gui_folder, "box")
cutscene_image = load_image(0, 0, gui_folder, "ending_bg")
ending_image = load_image(0, 0, gui_folder, "ending")
game_image = load_image(0, 0, gui_folder, "cover2")
scroll_image = load_image(0, 0, gui_folder, "scroll")
cast_image = load_image(0, 0, gui_folder, "cast")

dlg_1 = read_dialogue(path.join(dialogue_folder, "dlg_1.dlg"))
dlg_2 = read_dialogue(path.join(dialogue_folder, "dlg_2.dlg"))
dlg_3 = read_dialogue(path.join(dialogue_folder, "dlg_3.dlg"))
dlg_4 = read_dialogue(path.join(dialogue_folder, "dlg_4.dlg"))
dlg_5 = read_dialogue(path.join(dialogue_folder, "dlg_5.dlg"))
dlg_6 = read_dialogue(path.join(dialogue_folder, "dlg_6.dlg"))
dlg_7 = read_dialogue(path.join(dialogue_folder, "dlg_7.dlg"))
dlg_8 = read_dialogue(path.join(dialogue_folder, "dlg_8.dlg"))
dlg_9 = read_dialogue(path.join(dialogue_folder, "dlg_9.dlg"))
cutscene_a = read_dialogue(path.join(dialogue_folder, "cutscene_a.dlg"))
cutscene_b = read_dialogue(path.join(dialogue_folder, "cutscene_b.dlg"))
cutscene_c = read_dialogue(path.join(dialogue_folder, "cutscene_c.dlg"))





font_1 = load_font('pc-9800', 20)
font_2 = load_font('pc-9800', 40)
font_3 = load_font('pc-9800', 60)
font_4 = load_font('win', 30)

clock = pg.time.Clock()  # Brings the clock

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
orange = (255, 100, 10)
yellow = (255, 255, 0)
blue_green = (0, 255, 170)
maroon = (115, 0, 0)
lime = (180, 255, 100)
pink = (255, 100, 180)
purple = (240, 0, 255)
gray = (127, 127, 127)
magenta = (255, 0, 230)
brown = (100, 40, 0)
forest_green = (0, 50, 0)
navy_blue = (0, 0, 100)
rust = (210, 150, 75)
dandelion_yellow = (255, 200, 0)
highlighter = (255, 255, 100)
sky_blue = (0, 255, 255)
light_gray = (200, 200, 200)
dark_gray = (50, 50, 50)
tan = (230, 220, 170)
coffee_brown = (200, 190, 140)
moon_glow = (235, 245, 255)
