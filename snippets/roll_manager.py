import time as t
import random
from datetime import datetime

def roll_aura(luck, roll_info, aura_list, biome_list, biome, time, rolls, inventory, runes, visuals=None, is_real_roll=True):
    if (is_real_roll and t.time() - roll_info[0] > 0) or not is_real_roll:
        r_i = roll_info
        r = rolls
        if is_real_roll:
            r_i[0] = t.time() + r_i[1]

        for i in range(len(aura_list)):
            rarity = aura_list[i][1] / luck

            # If the aura is from glitch or dreamspace + it is not any of the biomes
            if len(aura_list[i]) == 3 and aura_list[i][2] != biome and biome != 0 and (aura_list[i][2] == 0 or aura_list[i][2] == 1):
                continue

            # If the aura is from limbo + it is not limbo OR the aura is not from limbo + it is limbo
            if (len(aura_list[i]) == 3 and aura_list[i][2] == 12 and biome != 12) or (len(aura_list[i]) != 3 and biome == 12) or (len(aura_list[i]) == 3 and aura_list[i][2] != 12 and biome == 12):
                continue

            # If the aura can be rolled w/o breakthrough in the biome
            if len(aura_list[i]) == 3 and ((aura_list[i][2] == biome or aura_list[i][2] == time) or aura_list[i][2] in runes):
                rarity /= manage_breakthrough(aura_list[i][2], biome, time, runes, biome_list)
                if rarity < luck:
                    continue

            # If you roll the aura OR there are no more auras below
            if random.randint(1, int(round(rarity, 3) * 1000)) <= 1000 or (i > 0 and aura_list[i - 1][1] < luck) or (aura_list[i][1] == 2 or aura_list[i][1] == 1):
                if is_real_roll:
                    r += 1
                    if not r_i[5]:
                        visuals.animate_roll(datetime.now(), r, luck, i, True)
                    else:
                        inventory.append([i, luck, r, datetime.now()])
                    r_i = manage_bonus_roll(True, r_i)
                if is_real_roll:
                    return aura_list[i], r_i, inventory, r
                else:
                    return aura_list[i]

def manage_bonus_roll(is_real_roll, roll_info):
    # If the current roll = the bonus roll number
    if roll_info[2] == roll_info[3]:
        if is_real_roll:
            roll_info[2] = 1
            return roll_info
        else:
            return True
    if is_real_roll:
        roll_info[2] += 1
        return roll_info
    return False

def manage_luck(roll_info, luck):
    if manage_bonus_roll(False, roll_info):
        return luck * 2
    return luck

def manage_breakthrough(aura_bt, biome, time, runes, biome_list):
    # If it is a biome, return the biome bt multiplier
    if aura_bt == biome or (aura_bt < 10 and aura_bt in runes):
        return biome_list[aura_bt][3]

    # If it is time, return 10
    elif aura_bt == time or (10 <= aura_bt <= 11 and aura_bt in runes):
        return 10
