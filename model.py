import random
import time
from snippets import buff_manager as buffm
from snippets import inventory_UI_manager as iUIm
from snippets import roll_manager as rollm
from snippets.constants import aura_list, limbo_aura_list, biome_list, items_list, ITEMS_DIMENSIONS, INV_DIMENSIONS

class Model:
    def __init__(self, player):
        self.player = player
        self.player_x = 100
        self.player_y = 480

        self.camera_x = 0
        self.camera_y = 0

        self.rolls = 0
        self.time = 10
        self.biome = None
        self.runes = []
        self.biome_timer = time.time()
        self.time_timer = time.time() + 30
        self.luck = 1
        self.roll_info = [time.time()-1000, 3.2, 1, 10, False, False]

        self.inventory = []
        self.items_inventory = {i: 1 for i in range(len(items_list))}
        self.buffs = []

    def check_buffs_and_remove(self):
        for b in self.buffs:
            if ('S' in b and b[1] <= time.time()) or ('R' in b and self.rolls >= b[1]):
                management, buffs = buffm.manage_buffs(False, b[0], self.runes)
                self.manage_buff_effects(management, buffs)
                self.buffs.remove(b)

    def manage_buff_effects(self, management, buffs):
        for manage in management:
            if manage[1] == '+':
                action = 1
            else:
                action = -1

            if manage[0] == 'L':
                self.luck += action * manage[2]
            elif manage[0] == 'S':
                pass
            elif manage[0] == 'B':
                if action == 1:
                    self.runes.append(manage[2])
                else:
                    self.runes.remove(manage[2])

        if buffs is not None:
            self.buffs = buffs
            self.buffs.sort(key=lambda x: x[0])

    def roll_biome(self):
        if time.time() - self.biome_timer > 0:
            self.biome_timer = time.time() + 1
            self.biome = None
            for i in range(9):
                if random.randint(1, biome_list[i][1]) == 1:
                    self.biome = i
                    print(biome_list[i])
                    self.biome_timer = time.time() + biome_list[i][2]
                    print(self.biome)
                    break

    def change_time(self):
        if time.time() - self.time_timer > 0:
            if self.time == 10:
                self.time = 11
                self.time_timer = time.time() + biome_list[self.time][2]
            elif self.time == 11:
                self.time = 10
                self.time_timer = time.time() + biome_list[self.time][2]

    def check_where_interact(self, x, y, visuals, mode):
        if visuals.page != 'title_screen':
            if 425 <= x <= 575 and 670 <= y <= 730 and mode == 1:
                self.handle_roll_outputs(rollm.roll_aura(rollm.manage_luck(self.roll_info, self.luck), self.roll_info, self.biome, self.time, self.rolls, self.inventory, self.runes, aura_list, limbo_aura_list, biome_list, self.buffs, visuals))

            elif 270 <= x <= 400 and 675 <= y <= 730 and mode == 1:
                if self.roll_info[4]:
                    self.roll_info[4] = False
                else:
                    self.roll_info[4] = True
            elif 600 <= x <= 730 and 675 <= y <= 730 and mode == 1:
                if self.roll_info[5]:
                    self.roll_info[5] = False
                else:
                    self.roll_info[5] = True
            elif 5 <= x <= 55 and 200 <= y <= 250:
                visuals.inventory_info[0] = 0
                visuals.inventory_info[1] = None
                visuals.page = 'inventory'
            elif 5 <= x <= 55 and 255 <= y <= 305:
                visuals.inventory_info[0] = 0
                visuals.inventory_info[1] = None
                visuals.page = 'items-items'

        if visuals.page == 'inventory':
            if 385 <= x <= 845 and 245 <= y <= 620:
                if mode == 1:
                    clicked = iUIm.get_clicked_inventory_cell((x, y), visuals, self.inventory, visuals.inventory_info[1], INV_DIMENSIONS)
                    if clicked is None or type(clicked) == list:
                        visuals.inventory_info[1] = None
                    else:
                        visuals.inventory_info[1] = self.inventory[clicked]

                elif 4 <= mode <= 5:
                    visuals.inventory_info[0] += (mode * 2 - 9) * -3
                    visuals.inventory_info[0] = iUIm.cutoff_inv_scrolling(visuals.inventory_info[0], self.inventory)
            elif 810 <= x <= 840 and 135 <= y <= 165:
                visuals.page = 'main'

        if visuals.page == 'items-items':
            if 385 <= x <= 845 and 245 <= y <= 620:
                if mode == 1:
                    visuals.inventory_info[1] = iUIm.get_clicked_inventory_cell((x, y), visuals, self.items_inventory, visuals.inventory_info[1], ITEMS_DIMENSIONS, True)
                elif 4 <= mode <= 5:
                    visuals.inventory_info[0] += (mode * 2 - 9) * -3
                    visuals.inventory_info[0] = iUIm.cutoff_inv_scrolling(visuals.inventory_info[0], self.items_inventory, True)
            elif 810 <= x <= 840 and 135 <= y <= 165:
                visuals.page = 'main'
            elif 270 <= x <= 375 or 345 <= y <= 395:
                if len(items_list[visuals.inventory_info[1]]) >= 4:
                    management, buffs = buffm.add_buffs(visuals.inventory_info[1], self.runes, self.buffs, self.rolls)
                    self.manage_buff_effects(management, buffs)

        if visuals.page == 'title_screen':
            if 425 <= x <= 575 and 520 <= y <= 580:
                visuals.page = 'main'

    def handle_roll_outputs(self, output):
        if output is not None:
            print(output[0])
            self.roll_info = output[1]
            self.inventory = output[2]
            self.rolls = output[3]

    def handle_game_tick(self, visuals):
        self.roll_biome()
        self.change_time()
        self.check_buffs_and_remove()

        if self.roll_info[4]:
            self.handle_roll_outputs(rollm.roll_aura(rollm.manage_luck(self.roll_info, self.luck), self.roll_info, self.biome, self.time, self.rolls, self.inventory, self.runes, aura_list, limbo_aura_list, biome_list, self.buffs, visuals))
