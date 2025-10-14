import random

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
        self.luck = 1

    def roll_aura(self, biome, time, luck):
        for i in range(len(self.aura_list)):
            rarity = self.aura_list[i][1]

            if len(self.aura_list[i]) == 3 and self.aura_list[i][2] != biome and (self.aura_list[i][2] == 0 or self.aura_list[i][2] == 1):
                continue

            if len(self.aura_list[i]) == 3 and (self.aura_list[i][2] == biome or self.aura_list[i][2] == time):
                rarity /= self.biome_list[biome][2]

            if random.randint(1, round(rarity, 3)*1000) <= 1000 or self.aura_list[i-1][1] < luck or self.aura_list[i][1] == 2:
                return self.aura_list[i]

    def roll_biome(self):
        for i in range(len(self.biome_list)):
            if random.randint(1, self.biome_list[i][1]) == 1:
                return self.biome_list[i][1]
        return None

    def check_where_clicked(self, x, y):
        if 325 <= x <= 475 and 510 <= y <= 580:
            print(self.roll_aura(self.biome, self.time, self.luck))