import pygame

pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 750

SARPANCHBOLD = {40: pygame.font.Font('files/fonts/Sarpanch-Bold.ttf', 40),
                30: pygame.font.Font('files/fonts/Sarpanch-Bold.ttf', 30),
                20: pygame.font.Font('files/fonts/Sarpanch-Bold.ttf', 20),
                15: pygame.font.Font('files/fonts/Sarpanch-Bold.ttf', 15),
                10: pygame.font.Font('files/fonts/Sarpanch-Bold.ttf', 10)}

SARPANCHMEDIUM = {15: pygame.font.Font('files/fonts/Sarpanch-Medium.ttf', 15)}

SEGOE_UI_SYMBOL = {30: pygame.font.Font('files/fonts/segoe-ui-symbol.ttf', 30),
                   15: pygame.font.Font('files/fonts/segoe-ui-symbol.ttf', 15)}

BIOME_COLORS = [(30, 83, 64),
                (214, 125, 203),
                (84, 84, 84),
                (110, 54, 202),
                (38, 99, 188),
                (204, 50, 1),
                (177, 137, 87),
                (97, 131, 255),
                (178, 255, 250),
                (122, 209, 255),
                (255, 255, 168),
                (197, 133, 255),
                (67, 67, 67)]

EFFECTS = [pygame.transform.scale(pygame.image.load('files/images/effect0.png'), (50, 50)),
           pygame.transform.scale(pygame.image.load('files/images/effect1.png'), (50, 50))]

INVENTORY_UI_BOXES = [
    # (color, x, y, w, h)
    ((100, 100, 100), 150, 125, 700, 500),        # Entire aura background
    ((110, 110, 110), 385, 245, 460, 375),        # aura background
    ('inv', None, None, None, None),              # Draw the inventory before proceeding
    ((100, 100, 100), 385, 240, 460, 5),          # Bit to hide the text (top)
    ((100, 100, 100), 385, 620, 460, 5),          # Bit to hide the text (bottom)
    ('bg color', 385, 625, 460, 45),              # Bit to hide the text (bottom pt 2)
    ((130, 130, 130), 155, 130, 690, 40),         # Aura Storage
    ((130, 130, 130), 385, 175, 227.5, 30),       # Regular
    ((130, 130, 130), 617.5, 175, 227.5, 30),     # Special
    ((130, 130, 130), 385, 210, 460, 30),         # Search bar
    ((130, 130, 130), 155, 175, 225, 90),         # Aura name
    ((130, 130, 130), 155, 290, 225, 190),        # Aura stats
    ((130, 130, 130), 155, 505, 225, 115),        # Aura buttons
    ((255, 255, 255), 155, 276, 225, 3),          # White bar 1
    ((255, 255, 255), 155, 491, 225, 3),          # White bar 2
    ((255, 255, 255), 160, 320, 200, 3)           # White bar (aura stats)
]

INV_DIMENSIONS = [7, 405/7]
INV_SHOWCASE_SIZE = 6 * (INV_DIMENSIONS[1] + 5) - 5

INVENTORY_UI_TEXT = [
    ((255, 255, 255), 500, 150, SARPANCHBOLD[30], 'Aura Storage', 'center'),
    ((255, 255, 255), 498.75, 190, SARPANCHBOLD[15], lambda inventory, i_i, aura_list: f'Regular [ {len(inventory)} / xxx ]', 'center'),
    ((255, 255, 255), 731.25, 190, SARPANCHBOLD[15], 'Special', 'center'),
    ((255, 255, 255), 160, 290, SARPANCHBOLD[20], '[ Information ]', 'topleft'),
    ((255, 255, 255), 160, 347, SARPANCHMEDIUM[15], lambda inventory, i_i, aura_list: f'With luck of {inventory[i_i[1]][1]}' if i_i[1] is not None else '', 'topleft'),
    ((255, 255, 255), 160, 328, SARPANCHMEDIUM[15], lambda inventory, i_i, aura_list: f'Rolled at: {inventory[i_i[1]][2]}' if i_i[1] is not None else '', 'topleft'),
    ((255, 255, 255), 267.5, 220, SARPANCHBOLD[30], lambda inventory, i_i, aura_list: aura_list[inventory[i_i[1]][0]][0] if i_i[1] is not None else '', 'center')
]

BUTTONS = [
    ((100, 100, 100), (425, 670, 150, 60), (130, 130, 130), 'rect',
        [['Roll', 500, 700, SARPANCHBOLD[30]],
         [lambda roll_info: (f"{roll_info[2]} / {roll_info[3]}" if roll_info[2] != roll_info[3] else 'x2 Luck Ready'), 500, 725, SARPANCHBOLD[15]]]),  # Roll button
    ((100, 100, 100), (270, 675, 130, 55), (130, 130, 130), 'rect',
        [['Auto Roll', 335, 690, SARPANCHBOLD[20]],
         [lambda roll_info: 'ON' if roll_info[4] else 'OFF', 335, 715, SARPANCHBOLD[20]]]),  # Auto roll button
    ((100, 100, 100), (600, 675, 130, 55), (130, 130, 130), 'rect',
        [['Quick Roll', 665, 690, SARPANCHBOLD[20]],
         [lambda roll_info: 'ON' if roll_info[5] else 'OFF', 665, 715, SARPANCHBOLD[20]]])   # Quick roll button
]



'''
0: Glitched
1: Dreamspace
2: Null
3: Corruption
4: Starfall
5: Hell
6: Sandstorm
7: Rainy
8: Snowy
9: Windy
10: Day
11: Night
12: Limbo
'''