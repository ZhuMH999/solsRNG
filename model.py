import random
import time
from snippets import buff_manager as buffm
from snippets import inventory_UI_manager as iUIm
from snippets import roll_manager as rollm
from snippets import crafting_UI_manager as cUIm
from snippets.constants import aura_list, limbo_aura_list, biome_list, items_list, gears_list, crafting_list, ITEMS_DIMENSIONS, INV_DIMENSIONS

class Model:
    def __init__(self, player):
        self.player = player
        self.player_x = 100
        self.player_y = 480

        self.camera_x = 0
        self.camera_y = 0

        self.rolls = 0
        self.time = 12
        self.biome = None
        self.runes = []
        self.biome_timer = time.time() + 60
        self.time_timer = time.time() + 30
        self.luck = 1
        self.roll_info = [time.time()-1000, 3.2, 1, 10, False, False]

        self.gears_inventory = {i: 1 for i in range(len(gears_list))}
        self.gears = [None, None]
        self.items_inventory = {i: 4000 for i in range(len(items_list))}
        self.inventory = []
        self.buffs = []

        for i in range(1000):
            management, buffs = buffm.add_buffs(25, self.runes, self.buffs, self.rolls)
            self.manage_buff_effects(management, buffs)
            management, buffs = buffm.add_buffs(16, self.runes, self.buffs, self.rolls)
            self.manage_buff_effects(management, buffs)
            management, buffs = buffm.add_buffs(17, self.runes, self.buffs, self.rolls)
            self.manage_buff_effects(management, buffs)

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

    def roll_biome(self, item_used=None):
        if time.time() - self.biome_timer > 0:
            self.biome_timer = time.time() + 1
            self.biome = None
            for i in range(2, 12):
                if random.randint(1, biome_list[i][1]) == 1:
                    self.biome = i
                    print(biome_list[i])
                    self.biome_timer = time.time() + biome_list[i][2]
                    print(self.biome)
                    break

        elif item_used is not None:
            if item_used == 'sc':
                if random.randint(1, 30000) == 1:
                    self.biome = 0
                elif random.randint(1, 5000) == 1:
                    self.biome = 1
                else:
                    weights = []
                    for biome in biome_list:
                        *_, weight = biome
                        weights.append(float(weight))
                    self.biome = random.choices(range(15), weights=weights, k=1)[0]
                self.biome_timer = time.time() + biome_list[self.biome][2]

            elif item_used == 'br':
                if random.randint(1, 30000) == 1:
                    self.biome = 0
                elif random.randint(1, 5000) == 1:
                    self.biome = 1
                else:
                    self.biome = random.randint(3, 11)
                self.biome_timer = time.time() + biome_list[self.biome][2]

    def change_time(self):
        if time.time() - self.time_timer > 0:
            if self.time == 12:
                self.time = 13
                self.time_timer = time.time() + biome_list[self.time][2]
            elif self.time == 12:
                self.time = 13
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
                    visuals.inventory_info[1] = iUIm.get_clicked_inventory_cell((x, y), visuals, self.items_inventory, visuals.inventory_info[1], ITEMS_DIMENSIONS, True, ['Potion', 'Rune', 'Tool', 'Material', 'Misc', 'Event'], items_list)
                elif 4 <= mode <= 5:
                    visuals.inventory_info[0] += (mode * 2 - 9) * -3
                    visuals.inventory_info[0] = iUIm.cutoff_inv_scrolling(visuals.inventory_info[0], self.items_inventory, True, ['Potion', 'Rune', 'Tool', 'Material', 'Misc', 'Event'], items_list)
            elif 810 <= x <= 840 and 135 <= y <= 165:
                visuals.page = 'main'
            elif 385 <= x <= 612.5 and 175 <= y <= 205:
                visuals.inventory_info[0] = 0
                visuals.inventory_info[1] = None
                visuals.page = 'items-gears'
            elif 270 <= x <= 375 and 345 <= y <= 395:
                if visuals.inventory_info[1] is not None:
                    if len(items_list[visuals.inventory_info[1]]) >= 4:
                        self.items_inventory[visuals.inventory_info[1]] -= 1
                        management, buffs = buffm.add_buffs(visuals.inventory_info[1], self.runes, self.buffs, self.rolls)
                        self.manage_buff_effects(management, buffs)
                    elif items_list[visuals.inventory_info[1]][1] == 'Tool':
                        if items_list[visuals.inventory_info[1]][0] == 'Biome Randomizer':
                            self.roll_biome('br')
                        elif items_list[visuals.inventory_info[1]][0] == 'Strange Controller':
                            self.roll_biome('sc')

        if visuals.page == 'items-gears':
            if 385 <= x <= 845 and 245 <= y <= 620:
                if mode == 1:
                    visuals.inventory_info[1] = iUIm.get_clicked_inventory_cell((x, y), visuals, self.gears_inventory, visuals.inventory_info[1], ITEMS_DIMENSIONS, True, ['Right', 'Left', 'Pocket'], gears_list)
                elif 4 <= mode <= 5:
                    visuals.inventory_info[0] += (mode * 2 - 9) * -3
                    visuals.inventory_info[0] = iUIm.cutoff_inv_scrolling(visuals.inventory_info[0], self.gears_inventory, True, ['Right', 'Left', 'Pocket'], gears_list)
            elif 617.5 <= x <= 845 and 175 <= y <= 205:
                visuals.inventory_info[0] = 0
                visuals.inventory_info[1] = None
                visuals.page = 'items-items'
            elif (170 <= x <= 235 and 265 <= y <= 330) or (300 <= x <= 365 and 265 <= y <= 330):
                print('e')
                if 170 <= x <= 235 and 265 <= y <= 330:
                    name = 'Right'
                    n = 0
                else:
                    name = 'Left'
                    n = 1

                if visuals.inventory_info[1] is None:
                    self.gears[n] = None
                elif visuals.inventory_info[1] is not None and name == gears_list[visuals.inventory_info[1]][1]:
                    self.gears[n] = visuals.inventory_info[1]
                    visuals.inventory_info[1] = None

                '''
        ('items-gears', (140, 140, 140), (200, 355, 50, 50), (150, 150, 150), 'rect',
            [['P', 225, 380, SARPANCHBOLD[25]]],
            [])'''

            elif 810 <= x <= 840 and 135 <= y <= 165:
                visuals.page = 'main'

        if visuals.page in ['crafting-gear', 'crafting-aura', 'crafting-item', 'crafting-potion', 'crafting-pocket']:
            if 20 <= x <= 250 and 375 <= y <= 525:
                if 4 <= mode <= 5:
                    visuals.crafting_info['scroll_left'] += (mode * 2 - 9) * -3
                    total_height = cUIm.get_crafting_scroll_total_height(visuals.crafting_info['selected'])
                    if visuals.crafting_info['scroll_left'] <= total_height + 135:
                        visuals.crafting_info['scroll_left'] = total_height + 135
                    elif visuals.crafting_info['scroll_left'] > 0:
                        visuals.crafting_info['scroll_left'] = 0
            elif 735 <= x <= 975 and 240 <= y <= 555:
                if 4 <= mode <= 5:
                    visuals.crafting_info['scroll_right'] += (mode * 2 - 9) * -3
                    total_height = len(crafting_list) * -70
                    if visuals.crafting_info['scroll_right'] <= total_height + 315:
                        visuals.crafting_info['scroll_right'] = total_height + 315
                    elif visuals.crafting_info['scroll_right'] > 0:
                        visuals.crafting_info['scroll_right'] = 0

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
