import random
import time
from snippets import buff_manager as buffm
from snippets import inventory_UI_manager as iUIm
from snippets import roll_manager as rollm

def parse_file(filename, int_or_not=False):
    with open(filename, 'r') as file:
        result = []
        for line in file:
            parts = line.strip().split(',')
            if len(parts) > 1 and int_or_not:
                converted = [parts[0]] + [int(x) for x in parts[1:] if x]
            else:
                converted = parts
            result.append(converted)
        return result

class Model:
    def __init__(self):
        self.aura_list = parse_file("files/game_data/auras.txt", True)
        self.biome_list = parse_file("files/game_data/biomes.txt", True)
        self.items_list = parse_file("files/game_data/items.txt")
        self.buffs_list = parse_file("files/game_data/buffs.txt")

        self.rolls = 0
        self.time = 10
        self.biome = None
        self.runes = []
        self.biome_timer = time.time()
        self.time_timer = time.time() + 30
        self.luck = 1
        self.roll_info = [time.time()-1000, 0, 1, 10, False, False]

        self.inventory = []
        self.buffs = []
        management, buffs = buffm.add_buffs(self.items_list, 17, self.buffs_list, self.runes, self.buffs, self.rolls)
        self.manage_buff_effects(management, buffs)

    def check_buffs_and_remove(self):
        for b in self.buffs:
            if ('S' in b and b[1] <= time.time()) or ('R' in b and self.rolls >= b[1]):
                management, buffs = buffm.manage_buffs(self.buffs_list, False, b[0], self.runes)
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

    def roll_biome(self):
        if time.time() - self.biome_timer > 0:
            self.biome_timer = time.time() + 1
            self.biome = None
            for i in range(9):
                if random.randint(1, self.biome_list[i][1]) == 1:
                    self.biome = i
                    print(self.biome_list[i])
                    self.biome_timer = time.time() + self.biome_list[i][2]
                    print(self.biome)
                    break

    def change_time(self):
        if time.time() - self.time_timer > 0:
            if self.time == 10:
                self.time = 11
                self.time_timer = time.time() + self.biome_list[self.time][2]
            elif self.time == 11:
                self.time = 10
                self.time_timer = time.time() + self.biome_list[self.time][2]

    def check_where_interact(self, x, y, visuals, mode):
        if 425 <= x <= 575 and 670 <= y <= 730 and mode == 1:
            self.handle_roll_outputs(rollm.roll_aura(rollm.manage_luck(self.roll_info, self.luck), self.roll_info, self.aura_list, self.biome_list, self.biome, self.time, self.rolls, self.inventory, self.runes, visuals))

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
        if visuals.page == 'inventory':
            if 385 <= x <= 845 and 245 <= y <= 620:
                if mode == 1:
                    visuals.inventory_info[1] = iUIm.get_clicked_inventory_cell((x, y), visuals, self.inventory, visuals.inventory_info[1])
                elif 4 <= mode <= 5:
                    visuals.inventory_info[0] += (mode * 2 - 9) * -3
                    visuals.inventory_info[0] = iUIm.cutoff_inv_scrolling(visuals.inventory_info[0], self.inventory)

    def handle_roll_outputs(self, output):
        print(output[0])
        self.roll_info = output[1]
        self.inventory = output[2]
        self.rolls = output[3]

    def handle_game_tick(self, visuals):
        self.roll_biome()
        self.change_time()
        self.check_buffs_and_remove()

        if self.roll_info[4]:
            self.handle_roll_outputs(rollm.roll_aura(rollm.manage_luck(self.roll_info, self.luck), self.roll_info, self.aura_list, self.biome_list, self.biome, self.time, self.rolls, self.inventory, self.runes, visuals))