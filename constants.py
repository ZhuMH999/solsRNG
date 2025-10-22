import pygame

pygame.init()
pygame.font.init()

WIDTH = 1000
HEIGHT = 750

SARPANCHBOLD = {30: pygame.font.Font('assets/Sarpanch-Bold.ttf', 30),
                20: pygame.font.Font('assets/Sarpanch-Bold.ttf', 20),
                15: pygame.font.Font('assets/Sarpanch-Bold.ttf', 15),
                10: pygame.font.Font('assets/Sarpanch-Bold.ttf', 10)}

ARIAL = {30: pygame.font.Font('assets/segoe-ui-symbol.ttf', 30)}

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

EFFECTS = [pygame.transform.scale(pygame.image.load('assets/images/effect0.png'), (50, 50)),
           pygame.transform.scale(pygame.image.load('assets/images/effect1.png'), (50, 50))]

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