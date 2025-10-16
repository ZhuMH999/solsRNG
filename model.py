import random
import time

def parse_file(filename):
    with open(filename, 'r') as file:
        result = []
        for line in file:
            parts = line.strip().split(',')
            if len(parts) > 1:
                converted = [parts[0]] + [int(x) for x in parts[1:] if x]
            else:
                converted = parts
            result.append(converted)
        return result

class Model:
    def __init__(self):
        self.aura_list = parse_file("assets/auras.txt")
        self.biome_list = parse_file("assets/biomes.txt")

        self.time = 10
        self.biome = None
        self.biome_timer = time.time()
        self.time_timer = time.time() + 300
        self.luck = 1
        self.roll_info = [time.time()-1000, 3.2, 1, 10]

        self.inventory = []

    def roll_aura(self, luck, visuals=None, is_real_roll=True):
        if (is_real_roll and time.time() - self.roll_info[0] > 0) or not is_real_roll:
            if is_real_roll:
                self.roll_info[0] = time.time() + self.roll_info[1]

            print(f"{luck}, rolled {is_real_roll}")

            for i in range(len(self.aura_list)):
                rarity = self.aura_list[i][1] / luck

                if len(self.aura_list[i]) == 3 and self.aura_list[i][2] != self.biome and (self.aura_list[i][2] == 0 or self.aura_list[i][2] == 1 or self.aura_list[i][2] == 12):
                    continue

                if len(self.aura_list[i]) == 3 and (self.aura_list[i][2] == self.biome or self.aura_list[i][2] == time):
                    rarity /= self.biome_list[self.biome][3]

                if random.randint(1, int(round(rarity, 3)*1000)) <= 1000 or (self.aura_list[i-1][1] < luck and i > 0) or (self.aura_list[i][1] == 2 or self.aura_list[i][1] == 1):
                    if is_real_roll:
                        visuals.animate_roll(luck, self.aura_list[i][0], True)
                        self.manage_bonus_roll(True)
                    return self.aura_list[i]

    def manage_bonus_roll(self, is_real_roll):
        if self.roll_info[2] == self.roll_info[3]:
            if is_real_roll:
                self.roll_info[2] = 1
            return True
        if is_real_roll:
            self.roll_info[2] += 1
        return False

    def manage_luck(self):
        if self.manage_bonus_roll(False):
            return self.luck * 2
        return self.luck

    def roll_biome(self):
        if time.time() - self.biome_timer > 0:
            self.biome_timer = time.time() + 1
            self.biome = None
            for i in range(len(self.biome_list)):
                if random.randint(1, self.biome_list[i][1]) == 1:
                    self.biome = self.biome_list[i]
                    self.biome_timer = time.time() + self.biome_list[i][2]
                    print(self.biome)
                    break

    def change_time(self):
        if time.time() - self.time_timer > 0:
            if self.time == 10:
                self.time = 11
                self.time_timer = time.time() + 660
            elif self.time == 11:
                self.time = 10
                self.time_timer = time.time() + 600

    def check_where_clicked(self, x, y, visuals):
        if 325 <= x <= 475 and 510 <= y <= 580:
            rolled = self.roll_aura(self.manage_luck(), visuals)
            print(rolled)