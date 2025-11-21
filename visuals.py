import pygame
from snippets.constants import SARPANCHBOLD, SEGOE_UI_SYMBOL, ARIAL, BIOME_COLORS, UI_BOXES, UI_TEXT, INV_DIMENSIONS, BUTTONS, STARS, biome_list, aura_list, limbo_aura_list, buffs_list
from snippets.inventory_UI_manager import manage_rows_inv, draw_inventory_slot
from snippets.bg_color_manager import return_interpolated_color
from snippets.roll_manager import roll_aura, add_aura_to_inv
from snippets.sprite_sheet_manager import split_sprites
import time

class Visuals:
    def __init__(self, win, model):
        self.win = win
        self.model = model

        self.rolling_animation = None
        self.cutscene_animation = None

        self.page = 'main'
        self.inventory_info = [0, None]

        self.buff_sprites = split_sprites()

    def initialize_window(self):
        self.win.fill(return_interpolated_color(self.model.time_timer, self.model.time))

    def draw(self, x, y):
        self.win.fill(return_interpolated_color(self.model.time_timer, self.model.time))
        self.manage_UI_text_and_boxes()
        self.manage_buttons(x, y)
        self.manage_buff_description(x, y)

        # Biome and time indicator
        if self.model.biome is None:
            self.get_text_widget_scale_and_center((255, 255, 255), 10, 695, SARPANCHBOLD[15], '[ NORMAL ]', 1, 'topleft')
        elif self.model.biome is not None:
            self.get_text_widget_scale_and_center(BIOME_COLORS[self.model.biome], 10, 695, SARPANCHBOLD[15], f'[ {biome_list[self.model.biome][0].upper()} ]', 1, 'topleft')
        self.get_text_widget_scale_and_center(BIOME_COLORS[self.model.time], 10, 715, SARPANCHBOLD[20], biome_list[self.model.time][0].upper(), 1, 'topleft')

        # Effects
        for i in range(len(self.model.buffs)):
            self.win.blit(self.buff_sprites[self.model.buffs[i][0]], (950 - (i // 15) * 50, 0 + (i % 15)*50))
            if self.model.buffs[i][2] == 'S':
                time_s = round(self.model.buffs[i][1] - time.time())
                time_formatted = self.determine_time(time_s)
                self.get_text_widget_scale_and_center((0, 0, 0), 976 - (i // 15) * 50, 11 + (i % 15)*50, ARIAL[10], time_formatted, 1)
                self.get_text_widget_scale_and_center((255, 255, 255), 975 - (i // 15) * 50, 10 + (i % 15)*50, ARIAL[10], time_formatted, 1)
            elif self.model.buffs[i][2] == 'R':
                self.get_text_widget_scale_and_center((0, 0, 0), 976 - (i // 15) * 50, 11 + (i % 15)*50, ARIAL[10], f'x{str(self.model.buffs[i][1] - self.model.rolls)}', 1)
                self.get_text_widget_scale_and_center((255, 255, 255), 975 - (i // 15) * 50, 10 + (i % 15)*50, ARIAL[10], f'x{str(self.model.buffs[i][1] - self.model.rolls)}', 1)

        self.animate_roll()

    def manage_buttons(self, mousex, mousey):
        for page, color, size, active_color, method, labels, additional_rects in BUTTONS:
            if self.page in page or page == 'all':
                big_x_limit = size[2] + size[0]
                big_y_limit = size[3] + size[1]
                if method == 'rect':
                    pygame.draw.rect(self.win, color, size)
                    if size[0] < mousex < big_x_limit and size[1] < mousey < big_y_limit:
                        pygame.draw.rect(self.win, active_color, (size[0] + 5, size[1] + 5, size[2] - 10, size[3] - 10))

                    for c, x, y, w, h in additional_rects:
                        if callable(w):
                            w = w(self.model.roll_info[0])
                        pygame.draw.rect(self.win, c, (x, y, w, h))

                elif method == 'img':
                    for c, x, y, w, h in additional_rects:
                        pygame.draw.rect(self.win, c, (x, y, w, h))
                        if size[0] < mousex < big_x_limit and size[1] < mousey < big_y_limit:
                            pygame.draw.rect(self.win, (c[0] + 20, c[1] + 20, c[2] + 20), (x, y, w, h))
                    self.win.blit(color, size)

                for text, x, y, font in labels:
                    if callable(text):
                        text = text(self.model.roll_info)
                    self.get_text_widget_scale_and_center((255, 255, 255), x, y, font, text, 1)

    def manage_UI_text_and_boxes(self):
        for page, color, xpos, ypos, w, h in UI_BOXES:
            if self.page in page or page == 'all':
                if 'inventory' in page and color == 'inv':
                    for i in range(len(self.model.inventory)):
                        x, cell_y, width, height, text_x, text_y = draw_inventory_slot(i, self.inventory_info[0])
                        pygame.draw.rect(self.win, (140, 140, 140), (x, cell_y, width, height))

                        if 230 < text_y < 650:
                            text = self.model.inventory[i][0]
                            if 'L' in str(text):
                                self.get_text_widget_scale_and_center((255, 255, 255), text_x, text_y, SARPANCHBOLD[10], str(limbo_aura_list[int(text.split('L')[1].split(',')[0])][0]), 1)
                            else:
                                self.get_text_widget_scale_and_center((255, 255, 255), text_x, text_y, SARPANCHBOLD[10], str(aura_list[text][0]), 1)

                elif color == 'bg color':
                    pygame.draw.rect(self.win, return_interpolated_color(self.model.time_timer, self.model.time), (xpos, ypos, w, h))
                elif callable(ypos):
                    pygame.draw.rect(self.win, color, (xpos, ypos(self.inventory_info, manage_rows_inv(self.model.inventory) * (INV_DIMENSIONS[1] + 5)), w, h(self.inventory_info, manage_rows_inv(self.model.inventory) * (INV_DIMENSIONS[1] + 5))))
                else:
                    pygame.draw.rect(self.win, color, (xpos, ypos, w, h))

        for page, color, xpos, ypos, font, text, pos in UI_TEXT:
            if self.page in page or page == 'all':
                if callable(text):
                    text = text(self.model.inventory, self.inventory_info)

                self.get_text_widget_scale_and_center(color, xpos, ypos, font, text, 1, pos)

    def manage_buff_description(self, x, y):
        x_grid = (1000-x)//50
        y_grid = y//50

        if len(self.model.buffs) > x_grid * 15 + y_grid:
            layers = 0
            number_to_left = x_grid * 15 + y_grid + 15
            while number_to_left < len(self.model.buffs):
                layers += 1
                number_to_left += 15
            self.get_translucent_object_and_draw((0, 0, 0), (19 - x_grid - layers) * 50 - 140, max(min(y, 680), 10), 130, 60, 120, border_radius=5)
            pygame.draw.rect(self.win, (255, 255, 255), ((19 - x_grid - layers) * 50 - 130, max(min(y+17, 697), 27), 110, 3))
            self.get_text_widget_scale_and_center((255, 255, 255), (19 - x_grid - layers) * 50 - 75, max(min(y+10, 690), 20), SARPANCHBOLD[10], buffs_list[self.model.buffs[x_grid * 15 + y_grid][0]][0], 1)

    def animate_roll(self, biome=None, t=None, rolls=None, luck=None, final_roll=None, start=False):
        if self.rolling_animation is None and start:
            self.rolling_animation = [1, 0, time.time()-100, final_roll, roll_aura(luck, self.model.roll_info, self.model.biome, self.model.time, self.model.rolls, self.model.inventory, self.model.runes, aura_list, limbo_aura_list, biome_list, self.model.buffs, is_real_roll=False)[0], luck, rolls, t, biome]

        if self.rolling_animation is not None:
            if self.rolling_animation[0] == 7:
                if 20 <= self.rolling_animation[1]:
                    if self.rolling_animation[8] == 12:
                        self.get_text_widget_scale_and_center((0, 0, 0), 502, 377, SEGOE_UI_SYMBOL[30], limbo_aura_list[self.rolling_animation[3]][0], 1)
                        self.get_text_widget_scale_and_center((255, 255, 255), 500, 375, SEGOE_UI_SYMBOL[30], limbo_aura_list[self.rolling_animation[3]][0], 1)
                    else:
                        self.get_text_widget_scale_and_center((0, 0, 0), 502, 377, SEGOE_UI_SYMBOL[30], aura_list[self.rolling_animation[3]][0], 1)
                        self.get_text_widget_scale_and_center((255, 255, 255), 500, 375, SEGOE_UI_SYMBOL[30], aura_list[self.rolling_animation[3]][0], 1)
                elif self.rolling_animation[1] < 20:
                    if self.rolling_animation[8] == 12:
                        self.get_text_widget_scale_and_center((0, 0, 0), 502, 357 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], limbo_aura_list[self.rolling_animation[3]][0], 1)
                        self.get_text_widget_scale_and_center((255, 255, 255), 500, 355 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], limbo_aura_list[self.rolling_animation[3]][0], 1)
                    else:
                        self.get_text_widget_scale_and_center((0, 0, 0), 502, 357 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], aura_list[self.rolling_animation[3]][0], 1)
                        self.get_text_widget_scale_and_center((255, 255, 255), 500, 355 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], aura_list[self.rolling_animation[3]][0], 1)
            else:
                self.get_text_widget_scale_and_center((0, 0, 0), 502, 357 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], self.rolling_animation[4], 1)
                self.get_text_widget_scale_and_center((255, 255, 255), 500, 355 + self.rolling_animation[1], SEGOE_UI_SYMBOL[30], self.rolling_animation[4], 1)

            if time.time() - self.rolling_animation[2] >= 0.015:
                self.rolling_animation[2] = time.time()
                self.manage_rolling_animation_cycle()

    def manage_rolling_animation_cycle(self):
        if 20 < self.rolling_animation[1] and self.rolling_animation[0] != 7:
            self.rolling_animation[4] = roll_aura(self.rolling_animation[5], self.model.roll_info, self.model.biome, self.model.time, self.model.rolls, self.model.inventory, self.model.runes, aura_list, limbo_aura_list, biome_list, self.model.buffs, is_real_roll=False)[0]
            self.rolling_animation[0] += 1
            self.rolling_animation[1] = 0
        elif self.rolling_animation[0] == 7:
            if self.rolling_animation[1] == 20:
                if self.rolling_animation[8] == 12:
                    aura_rolled = limbo_aura_list[self.rolling_animation[3]]
                else:
                    aura_rolled = None
                add_aura_to_inv(self.rolling_animation[8], aura_rolled, self.model.inventory, self.rolling_animation[5], self.rolling_animation[6], self.rolling_animation[3], self.rolling_animation[7])
            elif self.rolling_animation[1] > 60:
                self.rolling_animation = None
                return None
            self.rolling_animation[1] += 1
        else:
            self.rolling_animation[1] += (8 - self.rolling_animation[0]) / 2

    def manage_cutscenes(self, rolled_aura=None, start=False):
        if self.cutscene_animation is None and start:
            self.cutscene_animation = [(255, 255, 255), time.time()-100, 1]
        if self.cutscene_animation is not None and time.time() - self.cutscene_animation[1] >= 0:
            self.img_rotation_size_color_and_draw(STARS[0], (255, 255, 255), 500, 375, (self.cutscene_animation[2] * 5) + 700, self.cutscene_animation[2] % 360)
            self.cutscene_animation[1] += 0.05
            self.cutscene_animation[2] += 1
            if self.cutscene_animation[2] > 1000:
                self.cutscene_animation = None

    def get_text_widget_scale_and_center(self, rgb, x, y, font, text, maximum, pos='center'):
        widget = font.render(text, True, rgb)
        rect = widget.get_rect()
        if pos == 'center':
            rect.center = (x, y)
        elif pos == 'topleft':
            rect.topleft = (x, y)
        self.win.blit(widget, rect)

    def get_translucent_object_and_draw(self, rgb, x, y, sizex, sizey, transparency, border_radius=0):
        s = pygame.Surface((sizex, sizey), pygame.SRCALPHA)
        s.set_alpha(transparency)
        pygame.draw.rect(s, rgb, (0, 0, sizex, sizey), border_radius=border_radius)
        self.win.blit(s, (x, y))

    def img_rotation_size_color_and_draw(self, img, rgb, x, y, size, deg):
        img_new = pygame.transform.rotate(pygame.transform.scale(img, (size, size)), deg)
        img_new_rect = img_new.get_rect()
        img_new_rect.center = (x, y)
        self.win.blit(img_new, img_new_rect)

    def determine_time(self, time_s):
        time_formatted = ''
        if time_s // 3600 != 0 and time_formatted == '':
            time_formatted = str(time_s // 3600) + ':'
        if (time_formatted == '' and (time_s % 3600) // 60 != 0) or time_formatted != 0:
            time_formatted = time_formatted + str((time_s % 3600) // 60) + ':'
        if (time_formatted == '' and (time_s % 3600) % 60 != 0) or time_formatted != 0:
            time_formatted = time_formatted + str((time_s % 3600) % 60)
        return time_formatted
