import pygame
import time
import sys
import os

# -----------------------------
# Resource path helper
# -----------------------------
def resource_path(relative_path):
    """ Get absolute path for PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# -----------------------------
# File parsing and decoding
# -----------------------------
def parse_file(filename, int_or_not=False):
    with open(filename, 'r') as file:
        result = []
        for line in file:
            parts = line.strip().split(',')
            if len(parts) > 1 and int_or_not:
                converted = [parts[0]]
                for x in parts[1:]:
                    if x:
                        try:
                            converted.append(int(x))
                        except ValueError:
                            converted.append(x)
                    else:
                        converted.append(x)
            else:
                converted = parts
            result.append(converted)
        return result

def decode_numbers(craft_list):
    results = []
    for craft_item in craft_list:
        item_result = [craft_item[0]]
        for j in range(1, 4):
            smallest_result = []

            encoded = craft_item[j]
            i = 0
            pair = []

            while i < len(encoded) and encoded != '0':
                length = int(encoded[i])
                i += 1
                number = int(encoded[i:i + length])
                i += length
                pair.append(number)
                if len(pair) == 2:
                    smallest_result.append(pair)
                    pair = []
            item_result.append(smallest_result)
        results.append(item_result)

    return results

def get_aura_info(i_i, t):
    if 'L' in str(i_i[1][0]):
        return limbo_aura_list[int(i_i[1][0].split('L')[1].split(',')[0])][t]
    else:
        return aura_list[i_i[1][0]][t]

# -----------------------------
# Pygame initialization
# -----------------------------
pygame.init()
pygame.font.init()

# -----------------------------
# Window dimensions
# -----------------------------
WIDTH = 1000
HEIGHT = 750

# -----------------------------
# Fonts
# -----------------------------
SARPANCHBOLD = {
    40: pygame.font.Font(resource_path('files/fonts/Sarpanch-Bold.ttf'), 40),
    30: pygame.font.Font(resource_path('files/fonts/Sarpanch-Bold.ttf'), 30),
    25: pygame.font.Font(resource_path('files/fonts/Sarpanch-Bold.ttf'), 25),
    20: pygame.font.Font(resource_path('files/fonts/Sarpanch-Bold.ttf'), 20),
    15: pygame.font.Font(resource_path('files/fonts/Sarpanch-Bold.ttf'), 15),
    12: pygame.font.Font(resource_path('files/fonts/Sarpanch-Bold.ttf'), 12),
    10: pygame.font.Font(resource_path('files/fonts/Sarpanch-Bold.ttf'), 10)
}

SARPANCHMEDIUM = {
    15: pygame.font.Font(resource_path('files/fonts/Sarpanch-Medium.ttf'), 15),
    12: pygame.font.Font(resource_path('files/fonts/Sarpanch-Medium.ttf'), 12)
}

SEGOE_UI_SYMBOL = {
    30: pygame.font.Font(resource_path('files/fonts/segoe-ui-symbol.ttf'), 30),
    15: pygame.font.Font(resource_path('files/fonts/segoe-ui-symbol.ttf'), 15)
}

ARIAL = {10: pygame.font.SysFont('Arial', 10)}

# -----------------------------
# Game constants
# -----------------------------
BIOME_COLORS = [
    (30, 83, 64),
    (214, 125, 203),
    (100, 100, 100),
    (84, 84, 84),
    (110, 54, 202),
    (100, 100, 100),
    (38, 99, 188),
    (204, 50, 1),
    (177, 137, 87),
    (97, 131, 255),
    (178, 255, 250),
    (122, 209, 255),
    (255, 255, 168),
    (197, 133, 255),
    (67, 67, 67)
]

POTION_COLORS = {
    'Oblivion': (79, 66, 134),
    'Mythical': (201, 76, 76),
    'Legendary': (189, 134, 61),
    'Epic': (106, 73, 184),
    'Rare': (72, 143, 196),
    'Uncommon': (103, 192, 103),
    'Common': (154, 154, 155),
    'Other': (92, 96, 96)
}

EFFECTS = pygame.transform.scale(pygame.image.load(resource_path('files/images/sprite_sheet.png')), (450, 300))
EFFECT_SIZE = (9, 6, 50)

# -----------------------------
# UI Images
# -----------------------------
aura = pygame.transform.scale(pygame.image.load(resource_path('files/images/aura_button.png')), (50, 50))
item = pygame.transform.scale(pygame.image.load(resource_path('files/images/items_button.png')), (50, 50))
STARS = [pygame.image.load(resource_path('files/images/1mstar.png'))]

# -----------------------------
# Load game data
# -----------------------------
aura_list = parse_file(resource_path("files/game_data_raw/auras.txt"), True)
limbo_aura_list = parse_file(resource_path('files/game_data_raw/auras_limbo.txt'), True)
biome_list = parse_file(resource_path("files/game_data_raw/biomes.txt"), True)
items_list = parse_file(resource_path("files/game_data_raw/items.txt"))
buffs_list = parse_file(resource_path("files/game_data_raw/buffs.txt"))
gears_list = parse_file(resource_path("files/game_data_raw/gear.txt"))
crafting_list = decode_numbers(parse_file(resource_path("files/game_data_raw/crafting.txt")))

# -----------------------------
# Gameplay constants
# -----------------------------
ROLL_DISTRIBUTION = [1/16, 1/14, 1/12, 1/9, 1/7, 1/5, 1/3]
GRAVITY = 0.6
JUMP_VELOCITY = -11
PLAYER_SPEED = 4

# -----------------------------
# UI Constants (Buttons, Boxes, Text)
# -----------------------------
UI_BOXES = [
    # (color, x, y, w, h)
    (['inventory', 'items-gears', 'items-items'], (100, 100, 100), 150, 125, 700, 500, 255),        # Entire aura and item background
    (['inventory', 'items-gears', 'items-items'], (110, 110, 110), 385, 245, 460, 375, 255),        # aura background
    ('inventory', 'inv', None, None, None, None, None),              # Draw the inventory before proceeding
    ('items-items', 'items', None, None, None, None, None),          # Draw the items inventory before proceeding
    ('items-gears', 'gears', None, None, None, None, None),          # Draw the gears inventory before proceeding
    (['inventory', 'items-gears', 'items-items'], (100, 100, 100), 385, 240, 460, 5, 255),          # Bit to hide the text (top)
    (['inventory', 'items-gears', 'items-items'], (100, 100, 100), 385, 620, 460, 5, 255),          # Bit to hide the text (bottom)
    (['inventory', 'items-gears', 'items-items'], 'bg color', 385, 625, 460, 45, 255),              # Bit to hide the text (bottom pt 2)
    (['inventory', 'items-gears', 'items-items'], (130, 130, 130), 155, 130, 690, 40, 255),         # Aura Storage
    (['inventory', 'items-gears', 'items-items'], (130, 130, 130), 617.5, 175, 227.5, 30, 255),     # Special
    (['inventory', 'items-gears', 'items-items'], (130, 130, 130), 385, 210, 460, 30, 255),         # Search bar
    ('inventory', (130, 130, 130), 155, 175, 225, 90, 255),         # Aura name
    ('inventory', (130, 130, 130), 155, 290, 225, 190, 255),        # Aura stats
    ('inventory', (130, 130, 130), 155, 505, 225, 115, 255),        # Aura buttons
    ('inventory', (255, 255, 255), 155, 276, 225, 3, 255),          # White bar 1
    ('inventory', (255, 255, 255), 155, 491, 225, 3, 255),          # White bar 2
    ('inventory', (255, 255, 255), 160, 320, 200, 3, 255),           # White bar (aura stats)
    (['inventory', 'items-gears', 'items-items'], (140, 140, 140), 830, lambda i_i, total_height: 250 + 370 * ((i_i[0] * -1) / total_height) if total_height > 0 else 250, 10, lambda i_i, total_height: min(365, 365 * (INV_SHOWCASE_SIZE / total_height)) if total_height > 0 else 365, 255),  # Scrollbar
    ('title_screen', (100, 100, 100), 280, 150, 440, 100, 150),  # title screen backing the words sols rng in python
    ('items-items', (110, 110, 110), 155, 175, 225, 225, 255),    # Potion display
    ('items-gears', (110, 110, 110), 155, 175, 225, 245, 255),    # gear display
    ('items-items', (130, 130, 130), 160, 345, 105, 50, 255),   # potion use number (NOT IN USE YET)
    ('items-items', (130, 130, 130), 160, 180, 215, 160, 225),   # potion image backboard
    ('convo', (110, 110, 110), 270, 480, 460, 120, 190),  # conversation backboard
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (100, 100, 100), 10, 175, 250, 400, 255),   # crafting everything, left
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (100, 100, 100), 720, 155, 270, 440, 255),  # crafting everything, right
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (110, 110, 110), 20, 185, 230, 130, 255),   # crafting image
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (110, 110, 110), 30, 320, 210, 50, 255),    # crafting buff
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (110, 110, 110), 20, 375, 230, 150, 255),   # crafting recipe
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (110, 110, 110), 730, 230, 250, 355, 255),  # crafting selector backboard
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (120, 120, 120), 735, 265, 240, 315, 255),  # crafting selector smaller backboard
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], 'craft', None, None, None, None, None),     # draws crafting before proceeding
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (100, 100, 100), 20, 525, 230, 50, 255),    # bit to hide the bottom #1 (left)
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (110, 110, 110), 735, 260, 240, 5, 255),    # bit to hide the top #1 (right)
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (120, 120, 120), 740, 265, 230, 5, 255),    # bit to hide the top #2 (right)
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (100, 100, 100), 735, 585, 240, 10, 255),   # bit to hide the bottom #1 (right)
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (110, 110, 110), 735, 580, 240, 5, 255),    # bit to hide the bottom #2 (right)
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (120, 120, 120), 740, 575, 230, 5, 255),    # bit to hide the bottom #2 (right)
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (110, 110, 110), 730, 165, 250, 30, 255),   # crafting location name backboard
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (120, 120, 120), 735, 235, 240, 25, 255)   # searchbar
]

UI_TEXT = [
    ('inventory', (255, 255, 255), 500, 150, SARPANCHBOLD[30], 'Aura Storage', 'center'),
    ('inventory', (255, 255, 255), 160, 290, SARPANCHBOLD[20], '[ Information ]', 'topleft'),
    ('inventory', (255, 255, 255), 160, 349, SARPANCHMEDIUM[15], lambda inventory, i_i: f'With luck of {i_i[1][1]}' if i_i[1] is not None else '', 'topleft'),
    ('inventory', (255, 255, 255), 160, 328, SARPANCHMEDIUM[15], lambda inventory, i_i: f'Rolled at: {i_i[1][2]} Roll(s)' if i_i[1] is not None else '', 'topleft'),
    ('inventory', (255, 255, 255), 267.5, 213, SARPANCHBOLD[30], lambda inventory, i_i: get_aura_info(i_i, 0) if i_i[1] is not None else '', 'center'),
    ('inventory', (255, 255, 255), 267.5, 242, SARPANCHBOLD[15], lambda inventory, i_i: f'1 in {get_aura_info(i_i, 1):,}' if i_i[1] is not None else '', 'center'),
    ('inventory', (255, 255, 255), 160, 370, SARPANCHMEDIUM[12], lambda inventory, i_i: f'Time Discovered: {i_i[1][3].strftime("%d/%m/%Y %H:%M")}' if i_i[1] is not None else '', 'topleft'),
    (['items-gears', 'items-items'], (255, 255, 255), 500, 150, SARPANCHBOLD[30], 'Inventory', 'center'),
    ('items-items', (255, 255, 255), 267.5, 260, SARPANCHBOLD[20], lambda inventory, i_i: items_list[i_i[1]][0] if i_i[1] is not None else '', 'center'),
    ('title_screen', (255, 255, 255), 500, 200, SARPANCHBOLD[40], 'Sol\'s RNG in Python', 'center'),
    ('title_screen', (255, 255, 255), 990, 720, SARPANCHBOLD[20], 'Version Alpha 14.0', 'topright'),
    ('title_screen', (255, 255, 255), 10, 630, SARPANCHBOLD[20], 'Credits:', 'topleft'),
    ('title_screen', (255, 255, 255), 10, 660, SARPANCHBOLD[20], 'ZhuMH999 (coder)', 'topleft'),
    ('title_screen', (255, 255, 255), 10, 690, SARPANCHBOLD[20], 'xavietheskinstealer (artist)', 'topleft'),
    ('title_screen', (255, 255, 255), 10, 720, SARPANCHBOLD[20], 'All game idea credits goes to Sol\'s RNG on Roblox', 'topleft')
]

# page, color, size, active_color, method, labels, additional_rects
BUTTONS = [
    ('all', (100, 100, 100), (425, 670, 150, 60), (130, 130, 130), 'rect',
        [['Roll', 500, 700, SARPANCHBOLD[30]],
         [lambda roll_info, inv: (f"{roll_info[2]} / {roll_info[3]}" if roll_info[2] != roll_info[3] else 'x2 Luck Ready'), 500, 725, SARPANCHBOLD[15]]],
        [[(150, 150, 150), 430, 675, lambda r_i: 140 * ((r_i - time.time()) / 3.2) if r_i - time.time() > 0 else 0, 50]]),  # Roll button
    ('all', (100, 100, 100), (270, 675, 130, 55), (130, 130, 130), 'rect',
        [['Auto Roll', 335, 690, SARPANCHBOLD[20]],
         [lambda roll_info, inv: 'ON' if roll_info[4] else 'OFF', 335, 715, SARPANCHBOLD[20]]],
        []),  # Auto roll button
    ('all', (100, 100, 100), (600, 675, 130, 55), (130, 130, 130), 'rect',
        [['Quick Roll', 665, 690, SARPANCHBOLD[20]],
         [lambda roll_info, inv: 'ON' if roll_info[5] else 'OFF', 665, 715, SARPANCHBOLD[20]]],
        []),   # Quick roll button
    ('inventory', (35, 168, 64), (160, 510, 215, 31.6), (48, 230, 88), 'rect',
        [['Equip', 267.5, 525.8, SARPANCHBOLD[20]]],
        []),
    ('inventory', (204, 45, 45), (160, 546.6, 215, 31.6), (235, 28, 28), 'rect',
        [['Remove', 267.5, 562.4, SARPANCHBOLD[20]]],
        []),
    ('inventory', (150, 150, 150), (160, 584.2, 215, 31.6), (160, 160, 160), 'rect',
        [['Lock', 267.5, 600, SARPANCHBOLD[20]]],
        []),
    ('all', aura, (5, 200, 50, 50), None, 'img', [],
        [[(130, 130, 130), 5, 200, 50, 50]]),
    ('all', item, (5, 255, 50, 50), None, 'img', [],
        [[(130, 130, 130), 5, 255, 50, 50]]),
    (['inventory', 'items-items', 'items-gears'], (150, 150, 150), (810, 135, 30, 30), (160, 160, 160), 'rect',
        [['X', 825, 150, SARPANCHBOLD[20]]],
        []),
    ('inventory', (130, 130, 130), (385, 175, 227.5, 30), (140, 140, 140), 'rect',
        [[lambda r_i, inv: f'Regular [ {len(inv)} / xxx ]', 498.75, 190, SARPANCHBOLD[15]]],
        []),
    ('inventory', (130, 130, 130), (617.5, 175, 227.5, 30), (140, 140, 140), 'rect',
        [['Special', 731.25, 190, SARPANCHBOLD[15]]],
        []),
    (['items-gears', 'items-items'], (130, 130, 130), (385, 175, 227.5, 30), (140, 140, 140), 'rect',
        [['Gears', 498.75, 190, SARPANCHBOLD[15]]],
        []),
    (['items-gears', 'items-items'], (130, 130, 130), (617.5, 175, 227.5, 30), (140, 140, 140), 'rect',
        [['Items', 731.25, 190, SARPANCHBOLD[15]]],
        []),
    ('title_screen', (100, 100, 100), (425, 520, 150, 60), (130, 130, 130), 'rect',
        [['Play', 500, 550, SARPANCHBOLD[30]]],
        []),
    (['items-items'], (130, 130, 130), (270, 345, 105, 50), (140, 140, 140), 'rect',
        [['Use', 325, 370, SARPANCHBOLD[25]]],
        []),
    ('items-gears', (140, 140, 140), (170, 265, 65, 65), (150, 150, 150), 'rect',
        [[lambda gears: 'R' if gears[0] is None else gears_list[gears[0]][0], 202.5, 297.5, SARPANCHBOLD[15]]],
        []),
    ('items-gears', (140, 140, 140), (300, 265, 65, 65), (150, 150, 150), 'rect',
        [[lambda gears: 'L' if gears[1] is None else gears_list[gears[1]][0], 332.5, 297.5, SARPANCHBOLD[15]]],
        []),
    ('items-gears', (140, 140, 140), (200, 355, 50, 50), (150, 150, 150), 'rect',
        [['P', 225, 380, SARPANCHBOLD[10]]],
        []),
    ('convo', (110, 110, 110), (270, 610, 146, 40), (130, 130, 130), 'rect',
        [['[ Open ]', 343, 630, SARPANCHBOLD[15]]],
        []),
    ('convo', (110, 110, 110), (427, 610, 146, 40), (130, 130, 130), 'rect',
        [['Who are you?', 500, 630, SARPANCHBOLD[15]]],
        []),
    ('convo', (110, 110, 110), (584, 610, 146, 40), (130, 130, 130), 'rect',
        [['[ Leave ]', 657, 630, SARPANCHBOLD[15]]],
        []),
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (120, 120, 120), (20, 530, 130, 35), (130, 130, 130), 'rect',
        [['Open Recipe', 85, 547.5, SARPANCHBOLD[15]]],
        []),
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (120, 120, 120), (155, 535, 95, 25), (130, 130, 130), 'rect',
        [['Auto', 202.5, 547.5, SARPANCHBOLD[10]]],
        []),
    (['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket'], (120, 120, 120),
     (20, 530, 130, 35), (130, 130, 130), 'rect',
        [['Open Recipe', 85, 547.5, SARPANCHBOLD[15]]],
        []),
    (['crafting-gear', 'crafting-aura', 'crafting-item'], (120, 120, 120),
     (730, 200, 80, 25), (130, 130, 130), 'rect',
        [['Gear', 770, 212.5, SARPANCHBOLD[15]]],
        []),
    (['crafting-gear', 'crafting-aura', 'crafting-item'], (120, 120, 120),
     (815, 200, 80, 25), (130, 130, 130), 'rect',
        [['Aura', 855, 212.5, SARPANCHBOLD[15]]],
        []),
    (['crafting-gear', 'crafting-aura', 'crafting-item'], (120, 120, 120),
     (900, 200, 80, 25), (130, 130, 130), 'rect',
        [['Item', 940, 212.5, SARPANCHBOLD[15]]],
        [])
]

INV_DIMENSIONS = [7, 405/7]
INV_SHOWCASE_SIZE = 6 * (INV_DIMENSIONS[1] + 5) - 5
ITEMS_DIMENSIONS = [6, 405/6]