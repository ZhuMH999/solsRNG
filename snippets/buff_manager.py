import time
import random

def manage_buffs(buffs_list, add_or_remove, buff, runes):
    # Effect in this case is referring to something like "1.5L"
    effect = buffs_list[buff][1]
    management = []

    # True means add, False means remove
    # L means luck, S means rollspeed, B means rune
    for e in effect.split(';'):
        if add_or_remove:
            if 'L' in e:
                management.append(['L', '+', float(e.split('L')[0])])
            elif 'S' in e:
                pass
            elif 'B' in e and int(e.split('B')[0]) not in runes:
                management.append(['B', '+', int(e.split('B')[0])])

        else:
            if 'L' in e:
                management.append(['L', '-', float(e.split('L')[0])])
            elif 'S' in e:
                pass
            elif 'B' in e:
                management.append(['B', '-', int(e.split('B')[0])])
    return management, None

def add_buffs(items_list, item_used, buffs_list, runes, buffs, rolls):
    item = items_list[item_used]
    management = []

    # Splits the buffs up, so if there are multiple buffs they will all be handled
    for t in item[1].split(';'):
        # If the item needs to randomise a buff (e.g. strange potion)
        if 'R' in t:
            buff = int(random.choice(item[1].split('R')[1].split('-')))
        else:
            buff = int(t)

        # Checks if the buff is already existing
        result = _check_if_buff_is_in_list(buff, buffs)

        if result is not None:  # If the buff is already there, just add the amount of time / rolls it lasts
            buffs[result][1] += int(item[2].split('S')[0].split('R')[0])
        else:
            # If the buff is not there
            if 'S' in item[2]:  # Add based on seconds
                buffs.append([buff, time.time() + int(item[2].split('S')[0].split('R')[0]), 'S'])
            else:  # Add based on rolls
                buffs.append([buff, rolls + int(item[2].split('S')[0].split('R')[0]), 'R'])
            manage, _ = manage_buffs(buffs_list, True, buff, runes)
            management.extend(manage)
    return management, buffs

def _check_if_buff_is_in_list(buff, buffs):
    for b in range(len(buffs)):
        if buffs[b][0] == buff:
            return b
    return None
