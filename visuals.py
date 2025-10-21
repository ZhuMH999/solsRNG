import pygame
from constants import SARPARNCHBOLD, ARIAL, BIOME_COLORS
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

        # Roll button
        pygame.draw.rect(self.win, (100, 100, 100), (325, 510, 150, 70))

        if 325 <= x <= 475 and 510 <= y <= 580:
            pygame.draw.rect(self.win, (130, 130, 130), (330, 515, 140, 60))

        if self.model.roll_info[0] - time.time() > 0:
            pygame.draw.rect(self.win, (150, 150, 150), (330, 515, 140*((self.model.roll_info[0] - time.time()) / 3.2), 60))

        self.get_text_widget_and_center((255, 255, 255), 400, 545, SARPARNCHBOLD[30], 'Roll')

        # Bonus Roll indicator
        if self.model.roll_info[2] != self.model.roll_info[3]:
            self.get_text_widget_and_center((255, 255, 255), 400, 570, SARPARNCHBOLD[15], f'{self.model.roll_info[2]} / {self.model.roll_info[3]}')
        else:
            self.get_text_widget_and_center((255, 255, 255), 400, 570, SARPARNCHBOLD[15], 'x2 Luck Ready')

        # Biome and time indicator
        if self.model.biome is None:
            self.get_text_widget_and_center((255, 255, 255), 10, 505, SARPARNCHBOLD[15], '[ NORMAL ]', 'topleft')
        elif self.model.biome is not None:
            self.get_text_widget_and_center(BIOME_COLORS[self.model.biome], 10, 505, SARPARNCHBOLD[15], f'[ {self.model.biome_list[self.model.biome][0].upper()} ]', 'topleft')
        if self.model.time == 10:
            self.get_text_widget_and_center((255, 255, 168), 10, 525, SARPARNCHBOLD[20], 'DAYTIME', 'topleft')
        elif self.model.time == 11:
            self.get_text_widget_and_center((197, 133, 255), 10, 525, SARPARNCHBOLD[20], 'NIGHTTIME', 'topleft')

        self.animate_roll()

    def animate_roll(self, luck=None, final_roll=None, start=False):
        if self.rolling_animation is None and start:
            self.rolling_animation = [1, 0, time.time()-100, final_roll, self.model.roll_aura(luck=luck, is_real_roll=False)[0], luck]

        if self.rolling_animation is not None and time.time() - self.rolling_animation[2] >= 0.05:
            if 20 < self.rolling_animation[1] and self.rolling_animation[0] != 7:
                self.rolling_animation[0] += 1
                self.rolling_animation[1] = 0
                self.rolling_animation[4] = self.model.roll_aura(luck=self.rolling_animation[5], is_real_roll=False)[0]

            if self.rolling_animation[0] == 7:
                if 20 <= self.rolling_animation[1] <= 60:
                    self.get_text_widget_and_center((255, 255, 255), 400, 300, ARIAL[30], self.rolling_animation[3])
                    self.rolling_animation[1] += 1
                elif self.rolling_animation[1] > 60:
                    self.rolling_animation = None
                else:
                    self.get_text_widget_and_center((255, 255, 255), 400, 280 + self.rolling_animation[1], ARIAL[30], self.rolling_animation[3])
                    self.rolling_animation[1] += 1
                return None

            self.get_text_widget_and_center((255, 255, 255), 400, 280 + self.rolling_animation[1], ARIAL[30], self.rolling_animation[4])
            self.rolling_animation[1] += (8-self.rolling_animation[0])/2

    def get_text_widget_and_center(self, rgb, x, y, font, text, pos='center'):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        if pos == 'center':
            rect.center = (x, y)
        elif pos == 'topleft':
            rect.topleft = (x, y)
        self.win.blit(widget, rect)
