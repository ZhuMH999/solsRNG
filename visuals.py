import pygame
from snippets.constants import SARPANCHBOLD, SEGOE_UI_SYMBOL, BIOME_COLORS, EFFECTS, UI_BOXES, UI_TEXT, INV_DIMENSIONS, INV_SHOWCASE_SIZE, BUTTONS
from snippets.inventory_UI_manager import manage_rows_inv, draw_inventory_slot
from snippets.bg_color_manager import return_interpolated_color
from snippets.roll_manager import roll_aura
import time

class Visuals:
    def __init__(self, win, model):
        self.win = win
        self.model = model

        self.rolling_animation = None

        self.page = 'inventory'
        self.inventory_info = [0, None]

    def initialize_window(self):
        self.win.fill(return_interpolated_color(self.model.time_timer, self.model.time))

    def draw(self, x, y):
        self.win.fill(return_interpolated_color(self.model.time_timer, self.model.time))
        self.manage_UI_text_and_boxes()
        self.manage_buttons(x, y)

        if self.model.roll_info[0] - time.time() > 0:
            pygame.draw.rect(self.win, (150, 150, 150), (430, 675, 140*((self.model.roll_info[0] - time.time()) / 3.2), 50))

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
                pass
                #  print(f'idiot you forgot to add assets for buff {self.model.buffs[i][0]}: {self.model.buffs_list[self.model.buffs[i][0]][0]}')

        self.animate_roll()

    def manage_buttons(self, mousex, mousey):
        for page, color, size, active_color, method, labels in BUTTONS:
            if self.page in page or page == 'all':
                if method == 'rect':
                    pygame.draw.rect(self.win, color, size)
                    big_x_limit = size[2] + size[0]
                    big_y_limit = size[3] + size[1]
                    if size[0] < mousex < big_x_limit and size[1] < mousey < big_y_limit:
                        pygame.draw.rect(self.win, active_color, (size[0] + 5, size[1] + 5, size[2] - 10, size[3] - 10))

                for text, x, y, font in labels:
                    if callable(text):
                        text = text(self.model.roll_info)
                    self.get_text_widget_and_center((255, 255, 255), x, y, font, text)

    def manage_UI_text_and_boxes(self):
        for page, color, xpos, ypos, w, h in UI_BOXES:
            if self.page in page or page == 'all':
                if 'inventory' in page and color == 'inv':
                    for i in range(len(self.model.inventory)):
                        x, cell_y, width, height, text_x, text_y = draw_inventory_slot(i, self.inventory_info[0])
                        pygame.draw.rect(self.win, (140, 140, 140), (x, cell_y, width, height))

                        if 230 < text_y < 650:
                            self.get_text_widget_and_center((255, 255, 255), text_x, text_y, SARPANCHBOLD[10], str(self.model.aura_list[self.model.inventory[i][0]][0]))

                elif color == 'bg color':
                    pygame.draw.rect(self.win, return_interpolated_color(self.model.time_timer, self.model.time), (xpos, ypos, w, h))
                elif callable(ypos):
                    pygame.draw.rect(self.win, color, (xpos, ypos(self.inventory_info, manage_rows_inv(self.model.inventory) * (INV_DIMENSIONS[1] + 5)), w, h(self.inventory_info, manage_rows_inv(self.model.inventory) * (INV_DIMENSIONS[1] + 5))))
                else:
                    pygame.draw.rect(self.win, color, (xpos, ypos, w, h))

        for page, color, xpos, ypos, font, text, pos in UI_TEXT:
            if self.page in page or page == 'all':
                if callable(text):
                    text = text(self.model.inventory, self.inventory_info, self.model.aura_list)

                self.get_text_widget_and_center(color, xpos, ypos, font, text, pos)

    def animate_roll(self, t=None, rolls=None, luck=None, final_roll=None, start=False):
        if self.rolling_animation is None and start:
            self.rolling_animation = [1, 0, time.time()-100, final_roll, roll_aura(luck, self.model.roll_info, self.model.aura_list, self.model.biome_list, self.model.biome, self.model.time, self.model.rolls, self.model.inventory, self.model.runes, is_real_roll=False)[0], luck, rolls, t]

        if self.rolling_animation is not None and time.time() - self.rolling_animation[2] >= 0.05:
            if 20 < self.rolling_animation[1] and self.rolling_animation[0] != 7:
                self.rolling_animation[0] += 1
                self.rolling_animation[1] = 0
                self.rolling_animation[4] = roll_aura(self.rolling_animation[5], self.model.roll_info, self.model.aura_list, self.model.biome_list, self.model.biome, self.model.time, self.model.rolls, self.model.inventory, self.model.runes, is_real_roll=False)[0]

            if self.rolling_animation[0] == 7:
                if self.rolling_animation[1] == 20:
                    self.model.inventory.append([self.rolling_animation[3], self.rolling_animation[5], self.rolling_animation[6], self.rolling_animation[7]])
                if 20 <= self.rolling_animation[1] <= 60:
                    self.get_text_widget_and_center((255, 255, 255), 500, 375, SEGOE_UI_SYMBOL[30], self.model.aura_list[self.rolling_animation[3]][0])
                    self.rolling_animation[1] += 1
                elif self.rolling_animation[1] > 60:
                    self.rolling_animation = None
                else:
                    self.get_text_widget_and_center((255, 255, 255), 500, 355 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], self.model.aura_list[self.rolling_animation[3]][0])
                    self.rolling_animation[1] += 1
                return None

            self.get_text_widget_and_center((255, 255, 255), 500, 355 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], self.rolling_animation[4])
            self.rolling_animation[1] += (8-self.rolling_animation[0])/2

    def get_text_widget_and_center(self, rgb, x, y, font, text, pos='center'):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        if pos == 'center':
            rect.center = (x, y)
        elif pos == 'topleft':
            rect.topleft = (x, y)
        self.win.blit(widget, rect)

    def get_translucent_object_and_draw(self, rgb, x, y, sizex, sizey, transparency):
        s = pygame.Surface((sizex, sizey))
        s.set_alpha(transparency)
        s.fill(rgb)
        self.win.blit(s, (x, y))
