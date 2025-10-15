import pygame
from constants import TEMPFONT
import time

class Visuals:
    def __init__(self, win, model):
        self.win = win
        self.model = model

        self.rolling_animation = None

    def initialize_window(self):
        self.win.fill('black')

    def draw(self, x, y):
        self.win.fill('black')

        pygame.draw.rect(self.win, (100, 100, 100), (325, 510, 150, 70))
        if 325 <= x <= 475 and 510 <= y <= 580:
            pygame.draw.rect(self.win, (130, 130, 130), (330, 515, 140, 60))

        self.get_text_widget_and_center((255, 255, 255), 400, 545, TEMPFONT, 'Roll')

        self.animate_roll()

    def animate_roll(self, final_roll=None, start=False):
        if self.rolling_animation is None and start:
            self.rolling_animation = [1, 0, time.time()-100, final_roll, self.model.roll_aura(is_real_roll=False)[0]]

        if self.rolling_animation is not None and time.time() - self.rolling_animation[2] >= 0.05:
            if 40 < self.rolling_animation[1] and self.rolling_animation[0] != 6:
                self.rolling_animation[0] += 1
                self.rolling_animation[1] = 0
                self.rolling_animation[4] = self.model.roll_aura(is_real_roll=False)[0]

            if self.rolling_animation[0] == 6:
                if 40 <= self.rolling_animation[1] <= 80:
                    self.get_text_widget_and_center((255, 255, 255), 400, 300, TEMPFONT, self.rolling_animation[3])
                    self.rolling_animation[1] += 2
                elif self.rolling_animation[1] > 60:
                    self.rolling_animation = None
                else:
                    self.get_text_widget_and_center((255, 255, 255), 400, 260 + self.rolling_animation[1], TEMPFONT, self.rolling_animation[3])
                    self.rolling_animation[1] += 2
                return None

            self.get_text_widget_and_center((255, 255, 255), 400, 260 + self.rolling_animation[1], TEMPFONT, self.rolling_animation[4])
            self.rolling_animation[1] += 2

    def get_text_widget_and_center(self, rgb, c_x, c_y, font, text):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        rect.center = (c_x, c_y)
        self.win.blit(widget, rect)
