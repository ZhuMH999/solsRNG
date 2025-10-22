import pygame
from constants import SARPANCHBOLD, ARIAL, BIOME_COLORS, EFFECTS
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
        pygame.draw.rect(self.win, (100, 100, 100), (425, 670, 150, 60))

        if 425 <= x <= 575 and 670 <= y <= 730:
            pygame.draw.rect(self.win, (130, 130, 130), (430, 675, 140, 50))

        if self.model.roll_info[0] - time.time() > 0:
            pygame.draw.rect(self.win, (150, 150, 150), (430, 675, 140*((self.model.roll_info[0] - time.time()) / 3.2), 50))

        self.get_text_widget_and_center((255, 255, 255), 500, 700, SARPANCHBOLD[30], 'Roll')

        # Auto roll button
        pygame.draw.rect(self.win, (100, 100, 100), (270, 675, 130, 55))

        if 270 <= x <= 400 and 675 <= y <= 730:
            pygame.draw.rect(self.win, (130, 130, 130), (275, 680, 120, 45))

        self.get_text_widget_and_center((255, 255, 255), 335, 690, SARPANCHBOLD[20], 'Auto Roll')

        if self.model.roll_info[4]:
            self.get_text_widget_and_center((255, 255, 255), 335, 715, SARPANCHBOLD[20], 'ON')
        else:
            self.get_text_widget_and_center((255, 255, 255), 335, 715, SARPANCHBOLD[20], 'OFF')

        # Quick roll button
        pygame.draw.rect(self.win, (100, 100, 100), (600, 675, 130, 55))

        if 600 <= x <= 730 and 675 <= y <= 730:
            pygame.draw.rect(self.win, (130, 130, 130), (605, 680, 120, 45))

        self.get_text_widget_and_center((255, 255, 255), 665, 690, SARPANCHBOLD[20], 'Quick Roll')

        if self.model.roll_info[5]:
            self.get_text_widget_and_center((255, 255, 255), 665, 715, SARPANCHBOLD[20], 'ON')
        else:
            self.get_text_widget_and_center((255, 255, 255), 665, 715, SARPANCHBOLD[20], 'OFF')

        # Bonus Roll indicator
        if self.model.roll_info[2] != self.model.roll_info[3]:
            self.get_text_widget_and_center((255, 255, 255), 500, 725, SARPANCHBOLD[15], f'{self.model.roll_info[2]} / {self.model.roll_info[3]}')
        else:
            self.get_text_widget_and_center((255, 255, 255), 500, 725, SARPANCHBOLD[15], 'x2 Luck Ready')

        # Biome and time indicator
        if self.model.biome is None:
            self.get_text_widget_and_center((255, 255, 255), 10, 695, SARPANCHBOLD[15], '[ NORMAL ]', 'topleft')
        elif self.model.biome is not None:
            self.get_text_widget_and_center(BIOME_COLORS[self.model.biome], 10, 695, SARPANCHBOLD[15], f'[ {self.model.biome_list[self.model.biome][0].upper()} ]', 'topleft')
        self.get_text_widget_and_center(BIOME_COLORS[self.model.time], 10, 715, SARPANCHBOLD[20], self.model.biome_list[self.model.time][0].upper(), 'topleft')

        # Effects
        for i in range(len(self.model.buffs)):
            try:
                self.win.blit(EFFECTS[self.model.buffs[i][0]], (950, 50*i))
                if self.model.buffs[i][2] == 'S':
                    self.get_text_widget_and_center((255, 255, 255), 975, 10 + i*50, SARPANCHBOLD[10], str(round(self.model.buffs[i][1] - time.time())))
            except:
                print(f'idiot you forgot to add assets for {self.model.buffs[i][0]}')

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
                    self.get_text_widget_and_center((255, 255, 255), 500, 375, ARIAL[30], self.rolling_animation[3])
                    self.rolling_animation[1] += 1
                elif self.rolling_animation[1] > 60:
                    self.rolling_animation = None
                else:
                    self.get_text_widget_and_center((255, 255, 255), 500, 355 + self.rolling_animation[1], ARIAL[30], self.rolling_animation[3])
                    self.rolling_animation[1] += 1
                return None

            self.get_text_widget_and_center((255, 255, 255), 500, 355 + self.rolling_animation[1], ARIAL[30], self.rolling_animation[4])
            self.rolling_animation[1] += (8-self.rolling_animation[0])/2

    def get_text_widget_and_center(self, rgb, x, y, font, text, pos='center'):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        if pos == 'center':
            rect.center = (x, y)
        elif pos == 'topleft':
            rect.topleft = (x, y)
        self.win.blit(widget, rect)
