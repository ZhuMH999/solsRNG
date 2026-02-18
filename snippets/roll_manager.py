import time as t
import random
from datetime import datetime

def roll_aura(luck, roll_info, biome, time, rolls, inventory, runes, aura_list, limbo_aura_list, biome_list, buffs, visuals=None, is_real_roll=True):
    if (is_real_roll and t.time() - roll_info[0] > 0) or not is_real_roll:
        r_i = roll_info
        r = rolls
        if is_real_roll:
            r_i[0] = t.time() + r_i[1]

        if biome != 14:
            aura_rolled, i = roll_main_aura(luck, biome, time, runes, aura_list, biome_list, buffs)
        else:
            aura_rolled, i = roll_limbo_aura(luck, limbo_aura_list)

        if is_real_roll:
            r += 1
            if not r_i[5]:
                visuals.animate_roll(biome, datetime.now(), r, luck, i, True)
                inv = inventory
            else:
                inv = add_aura_to_inv(biome, aura_rolled, inventory, luck, r, i)
            r_i = manage_bonus_roll(True, r_i)

            return aura_rolled, r_i, inv, r
        else:
            return aura_rolled

def roll_limbo_aura(luck, limbo_aura_list):
    for i in range(len(limbo_aura_list)):
        rarity = limbo_aura_list[i][1] / luck
        if random.randint(1, int(round(rarity, 3) * 1000)) <= 1000 or (i > 0 and limbo_aura_list[i - 1][1] < luck) or limbo_aura_list[i][1] == 1:
            return limbo_aura_list[i], i

def roll_main_aura(luck, biome, time, runes, aura_list, biome_list, buffs):
    for i in range(len(aura_list)):
        rarity = aura_list[i][1] / luck

        # If the aura is from glitch or dreamspace + it is not any of the biomes
        if len(aura_list[i]) == 3 and aura_list[i][2] != biome and biome != 0 and (aura_list[i][2] == 0 or aura_list[i][2] == 2):
            continue

        # If the aura can only / cannot be rolled in a specific biome
        if (len(aura_list[i]) == 3 and type(aura_list[i][2]) == str) and (('O' in aura_list[i][2] and aura_list[i][2].split('O')[1] == biome) or ('N' in aura_list[i][2] and aura_list[i][2].split('N')[1] == biome)):
            print(aura_list[i])
            continue

        # If the aura can only be rolled with a specific effect
        if len(aura_list[i]) == 3 and type(aura_list[i][2]) == str and 'B' in aura_list[i][2]:
            if check_for_buff(buffs, aura_list[i][2]):
                if random.randint(1, aura_list[i][1]) == 1:
                    return aura_list[i], i
            continue

        # If the aura can be rolled w/o breakthrough in the biome
        if len(aura_list[i]) == 3 and ((aura_list[i][2] == biome or aura_list[i][2] == time) or aura_list[i][2] in runes):
            rarity /= manage_breakthrough(aura_list[i][2], biome, time, runes, biome_list)
            if rarity < luck:
                continue

        # If you roll the aura OR there are no more auras below
        if random.randint(1, int(round(rarity, 3) * 1000)) <= 1000 or (188 > i > 2 and aura_list[i + 1][1] < luck) or aura_list[i][1] == 2:
            return aura_list[i], i

def add_aura_to_inv(biome, aura_rolled, inventory, luck, r, i, d=datetime.now()):
    if biome == 14 and len(aura_rolled) == 4:
        inventory.append([f'L{i},{aura_rolled[2]}', luck, r, d])
    elif biome == 14 and len(aura_rolled) == 3:
        inventory.append([aura_rolled[2], luck, r, d])
    else:
        inventory.append([i, luck, r, d])
    inv = sort_inventory(inventory)
    return inv

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
    if aura_bt == biome or (aura_bt < 13 and aura_bt in runes):
        return biome_list[aura_bt][3]

    # If it is time, return 10
    elif aura_bt == time or (13 <= aura_bt <= 14 and aura_bt in runes):
        return 10

def check_for_buff(buff_l, b):
    for buff in buff_l:
        if buff[0] == int(b.split('B')[1]):
            return True
    return False

def sort_key(x):
    if isinstance(x[0], str) and x[0].startswith("L"):
        # Put strings first (priority 0), sorted by their numeric part
        return int(x[0].split(',')[1])
    else:
        # Integers go second (priority 1)
        return x[0]

def sort_inventory(inventory):
    inventory.sort(key=sort_key)
    return inventory

def insert_before(inv, aura, before_num):
    for i, item in enumerate(inv):
        if item[0] == before_num:
            inv.insert(i, aura)
            break
    else:
        # If not found, append to the end
        inv.append(aura)
    return inv

