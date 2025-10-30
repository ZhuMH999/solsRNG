'''Luck Glove
Desire Glove
Lunar Device
Gemstone Gauntlet
Frozen Gauntlet
Solar Device
Dark Matter Device
Aqua Device
Shining Star
Eclipse Device
Jackpot Gauntlet
Exo Gauntlet
Windstorm device
Flesh Device
Subzero Device
Galatic Device
Volcanic Device
Exoflex Device
Hologrammer
Ragnaröker
Gravitational Device
Darkshader
Starshaper
Neuralyzer
Pole Light Core Device
Genesis Drive
Gear Basing
Strange Controller
Biome Randomizer
Bank
Item Collector
Eclipse'''

def parse_file(filename, int_or_not=False):
    with open(filename, 'r') as file:
        result = []
        for line in file:
            parts = line.strip().split(',')
            converted = parts[0]
            result.append(converted)
        return result

auras = parse_file('game_data/auras.txt')
print(auras)

name = input('Enter glove name > ')
final_gear = ''
final_aura = ''

while True:
    new_crafting_gear = input('Enter gear number > ')
    if new_crafting_gear == '':
        break
    gear_num = input('Enter amount of gear needed > ')

    final_gear = final_gear + str(len(new_crafting_gear)) + new_crafting_gear + str(len(gear_num)) + gear_num

while True:
    aura = input('Enter aura name > ')
    if aura == '':
        break
    new_crafting_aura = str(auras.index(aura))
    aura_num = input('Enter amount of aura needed > ')

    final_aura = final_aura + str(len(new_crafting_aura)) + new_crafting_aura + str(len(aura_num)) + aura_num


with open('game_data/crafting.txt', 'a') as file:
    file.write(f'{name},{final_gear},{final_aura}\n')
