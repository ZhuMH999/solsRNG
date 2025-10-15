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

        self.time = 1
        self.biome = None
        self.biome_timer = time.time()
        self.luck = 150000

    def roll_aura(self, visuals=None, is_real_roll=True):
        for i in range(len(self.aura_list)):
            rarity = self.aura_list[i][1] / self.luck

            if len(self.aura_list[i]) == 3 and self.aura_list[i][2] != self.biome and (self.aura_list[i][2] == 0 or self.aura_list[i][2] == 1 or self.aura_list == 12):
                continue

            if len(self.aura_list[i]) == 3 and (self.aura_list[i][2] == self.biome or self.aura_list[i][2] == time):
                rarity /= self.biome_list[self.biome][2]

            if random.randint(1, int(round(rarity, 3)*1000)) <= 1000 or (self.aura_list[i-1][1] < self.luck and i > 0) or (self.aura_list[i][1] == 2 or self.aura_list[i][1] == 1):
                if is_real_roll:
                    visuals.animate_roll(self.aura_list[i][0], True)
                return self.aura_list[i]

    def roll_biome(self):
        if time.time() - self.biome_timer > 1:
            for i in range(len(self.biome_list)):
                if random.randint(1, self.biome_list[i][1]) == 1:
                    self.biome = self.biome_list[i]
            self.biome_timer = time.time()
            return None

    def check_where_clicked(self, x, y, visuals):
        if 325 <= x <= 475 and 510 <= y <= 580:
            print(self.roll_aura(visuals))