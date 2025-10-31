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

SARPANCHMEDIUM = {15: pygame.font.Font('files/fonts/Sarpanch-Medium.ttf', 15),
                  12: pygame.font.Font('files/fonts/Sarpanch-Medium.ttf', 12)}

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

UI_BOXES = [
    # (color, x, y, w, h)
    (['inventory', 'items'], (100, 100, 100), 150, 125, 700, 500),        # Entire aura and item background
    ('inventory', (110, 110, 110), 385, 245, 460, 375),        # aura background
    ('inventory', 'inv', None, None, None, None),              # Draw the inventory before proceeding
    ('inventory', (100, 100, 100), 385, 240, 460, 5),          # Bit to hide the text (top)
    ('inventory', (100, 100, 100), 385, 620, 460, 5),          # Bit to hide the text (bottom)
    ('inventory', 'bg color', 385, 625, 460, 45),              # Bit to hide the text (bottom pt 2)
    ('inventory', (130, 130, 130), 155, 130, 690, 40),         # Aura Storage
    ('inventory', (130, 130, 130), 385, 175, 227.5, 30),       # Regular
    ('inventory', (130, 130, 130), 617.5, 175, 227.5, 30),     # Special
    ('inventory', (130, 130, 130), 385, 210, 460, 30),         # Search bar
    ('inventory', (130, 130, 130), 155, 175, 225, 90),         # Aura name
    ('inventory', (130, 130, 130), 155, 290, 225, 190),        # Aura stats
    ('inventory', (130, 130, 130), 155, 505, 225, 115),        # Aura buttons
    ('inventory', (255, 255, 255), 155, 276, 225, 3),          # White bar 1
    ('inventory', (255, 255, 255), 155, 491, 225, 3),          # White bar 2
    ('inventory', (255, 255, 255), 160, 320, 200, 3),           # White bar (aura stats)
    ('inventory', (140, 140, 140), 830, lambda i_i, total_height: 250 + 370 * ((i_i[0] * -1) / total_height), 10, lambda i_i, total_height: min(365, 365 * (INV_SHOWCASE_SIZE / total_height))),  # Scrollbar
]

INV_DIMENSIONS = [7, 405/7]
INV_SHOWCASE_SIZE = 6 * (INV_DIMENSIONS[1] + 5) - 5

UI_TEXT = [
    ('inventory', (255, 255, 255), 500, 150, SARPANCHBOLD[30], 'Aura Storage', 'center'),
    ('inventory', (255, 255, 255), 498.75, 190, SARPANCHBOLD[15], lambda inventory, i_i, aura_list: f'Regular [ {len(inventory)} / xxx ]', 'center'),
    ('inventory', (255, 255, 255), 731.25, 190, SARPANCHBOLD[15], 'Special', 'center'),
    ('inventory', (255, 255, 255), 160, 290, SARPANCHBOLD[20], '[ Information ]', 'topleft'),
    ('inventory', (255, 255, 255), 160, 349, SARPANCHMEDIUM[15], lambda inventory, i_i, aura_list: f'With luck of {inventory[i_i[1]][1]}' if i_i[1] is not None else '', 'topleft'),
    ('inventory', (255, 255, 255), 160, 328, SARPANCHMEDIUM[15], lambda inventory, i_i, aura_list: f'Rolled at: {inventory[i_i[1]][2]} Roll(s)' if i_i[1] is not None else '', 'topleft'),
    ('inventory', (255, 255, 255), 267.5, 220, SARPANCHBOLD[30], lambda inventory, i_i, aura_list: aura_list[inventory[i_i[1]][0]][0] if i_i[1] is not None else '', 'center'),
    ('inventory', (255, 255, 255), 160, 370, SARPANCHMEDIUM[12], lambda inventory, i_i, aura_list: f'Time Discovered: {inventory[i_i[1]][3].strftime("%d/%m/%Y %H:%M")}' if i_i[1] is not None else '', 'topleft')
]

BUTTONS = [
    ('all', (100, 100, 100), (425, 670, 150, 60), (130, 130, 130), 'rect',
        [['Roll', 500, 700, SARPANCHBOLD[30]],
         [lambda roll_info: (f"{roll_info[2]} / {roll_info[3]}" if roll_info[2] != roll_info[3] else 'x2 Luck Ready'), 500, 725, SARPANCHBOLD[15]]]),  # Roll button
    ('all', (100, 100, 100), (270, 675, 130, 55), (130, 130, 130), 'rect',
        [['Auto Roll', 335, 690, SARPANCHBOLD[20]],
         [lambda roll_info: 'ON' if roll_info[4] else 'OFF', 335, 715, SARPANCHBOLD[20]]]),  # Auto roll button
    ('all', (100, 100, 100), (600, 675, 130, 55), (130, 130, 130), 'rect',
        [['Quick Roll', 665, 690, SARPANCHBOLD[20]],
         [lambda roll_info: 'ON' if roll_info[5] else 'OFF', 665, 715, SARPANCHBOLD[20]]]),   # Quick roll button
    ('inventory', (35, 168, 64), (160, 510, 215, 31.6), (48, 230, 88), 'rect',
        [['Equip', 267.5, 525.8, SARPANCHBOLD[20]]])
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