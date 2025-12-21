import pygame

class World:
    def __init__(self):
        self.platforms = [
            pygame.Rect(0, 520, 2000, 40),   # ground
            pygame.Rect(400, 440, 120, 20),
            pygame.Rect(700, 380, 120, 20),
        ]
