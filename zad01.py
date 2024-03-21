def create_triplets_k_p_q(file_path='dictionary.txt'):
    triplets = []
    qs = []
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    lines = [line.strip().split(' ') for line in lines]
    lines = [[int(line[0]), line[1]] for line in lines]
    lines = sorted(lines, key=lambda x: x[1])
    keys_lines = [line for line in lines if line[0] > 50000]

    full_freq = sum([line[0] for line in lines])
    # lines = [[line[0] / full_freq, line[1]] for line in lines]
    # keys_lines = [[line[0] / full_freq, line[1]] for line in keys_lines]

    qs.append(find_q0(keys_lines, lines))

    for key_line in keys_lines:
        qs.append(find_qi(keys_lines, lines, key_line))

    print(f'My sum: {sum([key_line[0] for key_line in keys_lines]) + sum(qs)}')
    print(f'Frequency sum: {full_freq}')

    triplets.append(['', 0, qs[0]])
    for i in range(len(keys_lines)):
        triplets.append([keys_lines[i][1], keys_lines[i][0], qs[i + 1]])

    print(f'Sum in triplets: {sum([triplet[1] + triplet[2] for triplet in triplets])}')

    return triplets


def find_q0(key_lines, lines):
    q0 = 0
    current = lines[0]
    while not any(current[1] == key_line[1] for key_line in key_lines):
        q0 += current[0]
        current = lines[lines.index(current) + 1]
    return q0


def find_qi(key_lines, lines, key_line):
    q = 0
    current_word = key_line[1]
    if key_lines.index(key_line) + 1 < len(key_lines):
        end_word = key_lines[key_lines.index(key_line) + 1][1]
        current_index = find_index_based_on_key(current_word, lines)
        end_index = find_index_based_on_key(end_word, lines)
    else:
        end_word = lines[-1][1]
        current_index = find_index_based_on_key(current_word, lines)
        end_index = find_index_based_on_key(end_word, lines) + 1

    for i in range(current_index + 1, end_index):
        q += lines[i][0]
    return q


def find_index_based_on_key(key, lines):
    for line in lines:
        if line[1] == key:
            return lines.index(line)
    return -1


def abduls_triplets():
    keys = ['10', '20', '30', '40']
    pi = [3, 3, 1, 1]
    qi = [3, 1, 1, 1]
    triplets = [['', 0, 2]]
    for i in range(len(keys)):
        triplets.append([keys[i], pi[i], qi[i]])
    return triplets


def main():
    # triplets = create_triplets_k_p_q()
    abdul = abduls_triplets()
    print(abdul)


main()
