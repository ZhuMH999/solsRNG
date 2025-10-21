import random
import time

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
        self.aura_list = parse_file("assets/auras.txt", True)
        self.biome_list = parse_file("assets/biomes.txt", True)
        self.potions_list = parse_file("assets/items.txt")
        self.buffs_list = parse_file("assets/buffs.txt")

        self.rolls = 0
        self.time = 10
        self.biome = 0
        self.runes = []
        self.biome_timer = time.time() + 1000
        self.time_timer = time.time() + 75
        self.luck = 1.0
        self.roll_info = [time.time()-1000, 3.2, 1, 10]

        self.inventory = []
        self.buffs = []
        self.add_buffs(42)

    def roll_aura(self, luck, visuals=None, is_real_roll=True):
        if (is_real_roll and time.time() - self.roll_info[0] > 0) or not is_real_roll:
            if is_real_roll:
                self.roll_info[0] = time.time() + self.roll_info[1]

            for i in range(len(self.aura_list)):
                rarity = self.aura_list[i][1] / luck

                # If the aura is from glitch, dreamspace or limbo biome, and it is not any of the biomes
                if len(self.aura_list[i]) == 3 and self.aura_list[i][2] != self.biome and (self.aura_list[i][2] == 0 or self.aura_list[i][2] == 1 or self.aura_list[i][2] == 12):
                    continue

                # If the aura can be rolled w/o breakthrough in the biome
                if len(self.aura_list[i]) == 3 and ((self.aura_list[i][2] == self.biome or self.aura_list[i][2] == self.time) or self.aura_list[i][2] in self.runes):
                    rarity /= self.manage_breakthrough(self.aura_list[i][2])
                    print(self.aura_list[i])

                # If you roll the aura OR there are no more auras below
                if random.randint(1, int(round(rarity, 3)*1000)) <= 1000 or (self.aura_list[i-1][1] < luck and i > 0) or (self.aura_list[i][1] == 2 or self.aura_list[i][1] == 1):
                    if is_real_roll:
                        visuals.animate_roll(luck, self.aura_list[i][0], True)
                        self.manage_bonus_roll(True)
                        self.rolls += 1
                    return self.aura_list[i]

    def manage_bonus_roll(self, is_real_roll):
        # If the current roll = the bonus roll number
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

    def manage_buffs(self, add_or_remove, buff):
        # Effect in this case is referring to something like "1.5L"
        effect = self.buffs_list[buff][1]

        # True means add, False means remove
        # L means luck, S means rollspeed, B means rune
        for e in effect.split(';'):
            if add_or_remove:
                if 'L' in e:
                    self.luck += float(e.split('L')[0])
                elif 'S' in e:
                    pass
                elif 'B' in e:
                    self.runes.append(int(e.split('B')[0]))
                    print(self.runes)
            else:
                if 'L' in e:
                    self.luck -= float(e.split('L')[0])
                elif 'S' in e:
                    pass
                elif 'B' in e:
                    self.runes.remove(int(e.split('B')[0]))

    def manage_breakthrough(self, aura_bt):
        # If it is a biome, return the biome bt multiplier
        if aura_bt == self.biome or (aura_bt < 10 and aura_bt in self.runes):
            return self.biome_list[aura_bt][3]

        # If it is time, return 10
        elif aura_bt == self.time or (10 <= aura_bt <= 11 and aura_bt in self.runes):
            return 10

    def add_buffs(self, item_used):
        item = self.potions_list[item_used]

        # Splits the buffs up, so if there are multiple buffs they will all be handled
        for t in item[1].split(';'):
            # If the item needs to randomise a buff (e.g. strange potion)
            if 'R' in t:
                buff = int(random.choice(item[1].split('R')[1].split('-')))
            else:
                buff = int(t)

            # Checks if the buff is already existing
            result = self.check_if_buff_is_in_list(buff)

            if result is not None:
                self.buffs[result][1] += int(item[2].split('S')[0].split('R')[0])
            else:
                if 'S' in item[2]:
                    self.buffs.append([buff, time.time() + int(item[2].split('S')[0].split('R')[0]), 'S'])
                else:
                    self.buffs.append([buff, self.rolls + int(item[2].split('S')[0].split('R')[0]), 'R'])
                self.manage_buffs(True, buff)

    def check_if_buff_is_in_list(self, buff):
        for b in range(len(self.buffs)):
            if self.buffs[b][0] == buff:
                return b
        return None

    def check_buffs_and_remove(self):
        for b in self.buffs:
            if ('S' in b and b[1] <= time.time()) or ('R' in b and self.rolls >= b[1]):
                self.manage_buffs(False, b[0])
                self.buffs.remove(b)

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
                self.time_timer = time.time() + 150
            elif self.time == 11:
                self.time = 10
                self.time_timer = time.time() + 150

    def check_where_clicked(self, x, y, visuals):
        if 325 <= x <= 475 and 510 <= y <= 580:
            rolled = self.roll_aura(self.manage_luck(), visuals)
            print(rolled)

    def handle_game_tick(self):
        self.roll_biome()
        self.check_buffs_and_remove()