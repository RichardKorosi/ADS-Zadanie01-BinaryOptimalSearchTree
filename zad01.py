import sys

sys.setrecursionlimit(10 ** 6)


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

    def __str__(self):
        return f'Node(Key:{self.key},Left:{self.left},Right{self.right})'


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
    lines = [[line[0] / full_freq, line[1]] for line in lines]
    keys_lines = [[line[0] / full_freq, line[1]] for line in keys_lines]

    qs.append(find_q0(keys_lines, lines))

    for key_line in keys_lines:
        qs.append(find_qi(keys_lines, lines, key_line))

    # print(f'My sum: {sum([key_line[0] for key_line in keys_lines]) + sum(qs)}')
    # print(f'Frequency sum: {full_freq}')
    #
    # print(f'Sum Qs:{sum(qs)}')
    # print(f'My Ps:{sum([key_line[0] for key_line in keys_lines])}')

    triplets.append(['', 0, qs[0]])
    for i in range(len(keys_lines)):
        triplets.append([keys_lines[i][1], keys_lines[i][0], qs[i + 1]])

    # print(f'Sum in triplets: {round(sum([triplet[1] + triplet[2] for triplet in triplets]), 12)}')

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


def calculate_tables(n, p, q):
    c = [[None for _ in range(n)] for _ in range(n)]
    w = [[None for _ in range(n)] for _ in range(n)]
    root = [[None for _ in range(n)] for _ in range(n)]

    for i in range(0, n):
        w[i][i] = q[i]
        c[i][i] = q[i]

    for l in range(1, n):
        for i in range(0, n - l):
            j = i + l
            c[i][j] = float('inf')
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i + 1, j + 1):
                t = c[i][r - 1] + c[r][j] + w[i][j]
                if t < c[i][j]:
                    c[i][j] = t
                    root[i][j] = r

    return c, root


def build_tree(r, words, i, j):
    if i == j:
        return None
    r_i = r[i][j]
    key = words[r_i]
    left = build_tree(r, words, i, r_i - 1)
    right = build_tree(r, words, r_i, j)
    return Node(key, left, right)



def binary_search(root, key):
    comparisons = 0
    current = root
    visited_nodes = [root.key]

    while current:
        comparisons += 1
        if key == current.key:
            print(f"TRUE: {current.key.ljust(12)}" + f"|{comparisons}|".ljust(7) + f"{visited_nodes}")
            return comparisons, current
        elif key < current.key:
            if current.left is not None:
                visited_nodes.append(current.left.key)
                current = current.left
            else:
                break  # Exit the loop if current.left is None
        else:
            if current.right is not None:
                visited_nodes.append(current.right.key)
                current = current.right
            else:
                break  # Exit the loop if current.right is None

    print(f"FALSE: {key.ljust(12)}" + f"|{comparisons}|".ljust(7) + f"{visited_nodes}")
    return comparisons, None



def main():
    triplets = create_triplets_k_p_q()
    words = [triplet[0] for triplet in triplets]
    p = [triplet[1] for triplet in triplets]
    q = [triplet[2] for triplet in triplets]
    n = len(words)

    c, r = calculate_tables(n, p, q)
    tree = build_tree(r, words, 0, n - 1)

    for word in words[1::]:
        binary_search(tree, word)
    binary_search(tree, "boob")
    return True



main()
