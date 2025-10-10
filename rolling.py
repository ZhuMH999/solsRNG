import random

def roll_aura(aura_list, biome_list, biome, time, luck):
    for i in range(len(aura_list)):
        rarity = aura_list[i][1]

        if len(aura_list[i]) == 3 and aura_list[i][2] != biome and (aura_list[i][2] == 0 or aura_list[i][2] == 1):
            continue

        if len(aura_list[i]) == 3 and (aura_list[i][2] == biome or aura_list[i][2] == time):
            rarity /= biome_list[biome][2]

        if random.randint(1, round(rarity, 3)*1000) <= 1000 or aura_list[i-1][1] < luck or aura_list[i][1] == 2:
            return aura_list[i]

def roll_biome(biome_list):
    for i in range(len(biome_list)):
        if random.randint(1, biome_list[i][1]) == 1:
            return biome_list[i][1]
    return None