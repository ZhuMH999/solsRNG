run = True

with open('assets/auras.txt', 'r') as file:
    auras = [line.strip().split(',') for line in file]

while run:
    new_aura = input('Enter aura in the form NAME,RARITY').split(',')
    if new_aura == ['']:
        run = False
        break

    rarity_new_aura = int(new_aura[1])

    for i in range(len(auras)):
        if int(auras[i][1]) < rarity_new_aura:
            auras.insert(i, new_aura)
            break

print(auras)
if input('Is this correct? (y/n) >') == 'y':
    with open('assets/auras.txt', 'w') as file:
        for j in range(len(auras)):
            file.write(','.join(auras[j]) + '\n')