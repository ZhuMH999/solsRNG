def decode_numbers(encoded: str):
    i = 0
    results = []
    pair = []

    while i < len(encoded) and encoded != '0':
        # first read the length digit
        length = int(encoded[i])
        i += 1

        # read the next `length` digits as number
        number = int(encoded[i:i + length])
        i += length

        # collect into pairs
        pair.append(number)
        if len(pair) == 2:
            results.append(pair)
            pair = []

    return results

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

crafting_list = parse_file('game_data_raw/crafting.txt')

insert_or_remove = input('Are you inserting a new aura, or deleting an aura? (i for insert, d for delete) > ')

print('For insersion, all auras INCLUDING and after the specified number aura will be shifted forward 1 number.\n'
      'For removal, all auras after the specified number will be shifted forward 1 number.')

aura_num = int(input('Please input the aura number that you are inserting / deleting into. > '))

final_str = ''

for j in range(len(crafting_list)):
    decoded = decode_numbers(crafting_list[j][2])
    encode_back = ''
    for i in range(len(decoded)):
        if decoded[i][0] >= aura_num:
            if insert_or_remove == 'i':
                decoded[i][0] += 1
            elif insert_or_remove == 'd':
                decoded[i][0] -= 1
        encode_back = encode_back + str(len(str(decoded[i][0]))) + str(decoded[i][0]) + str(len(str(decoded[i][1]))) + str(decoded[i][1])
    if encode_back == '':
        encode_back = '0'
    crafting_list[j][2] = encode_back
    final_str = final_str + crafting_list[j][0] + ',' + crafting_list[j][1] + ',' + crafting_list[j][2] + ',' + crafting_list[j][3] + '\n'

print(final_str)
print('\n\nPlease check that the above is correct before placing it in your script.')
