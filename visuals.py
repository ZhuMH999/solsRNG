import pygame
from constants import TEMPFONT

class Visuals:
    def __init__(self, win, model):
        self.win = win
        self.model = model

    def initialize_window(self):
        self.win.fill('black')

    def draw(self, x, y):
        self.win.fill('black')
        pygame.draw.rect(self.win, (100, 100, 100), (325, 510, 150, 70))
        if 325 <= x <= 475 and 510 <= y <= 580:
            pygame.draw.rect(self.win, (130, 130, 130), (330, 515, 140, 60))
        self.get_text_widget_and_center((255, 255, 255), 400, 545, TEMPFONT, 'Roll')

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)
