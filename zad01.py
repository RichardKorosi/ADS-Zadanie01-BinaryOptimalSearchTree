import matplotlib.pyplot as plt
import networkx as nx
import sys

sys.setrecursionlimit(999999999)


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


def abduls_triplets():
    keys = ['10', '20', '30', '40']
    pi = [3, 3, 1, 1]
    qi = [3, 1, 1, 1]
    triplets = [['', 0, 2]]
    for i in range(len(keys)):
        triplets.append([keys[i], pi[i], qi[i]])
    return triplets


def calculate_tables(n, p, q):
    c = [[0 for _ in range(n)] for _ in range(n)]
    w = [[0 for _ in range(n)] for _ in range(n)]
    root = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(0, n):
        w[i][i] = q[i]

    for l in range(1, n):
        for i in range(0, n - l):
            j = i + l
            c[i][j] = float('inf')
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j):
                t = c[i][r] + c[r + 1][j] + w[i][j]
                if t < c[i][j]:
                    c[i][j] = t
                    root[i][j] = r

    return c, root


def calculate_tables2(n, p, q):
    e = [[0 for _ in range(n + 2)] for _ in range(n + 2)]
    w = [[0 for _ in range(n + 2)] for _ in range(n + 2)]
    root = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    for l in range(1, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            e[i][j] = float('inf')
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j]:
                    e[i][j] = t
                    root[i][j] = r

    return e, root


def build_tree(dp_root, lines, start, end):
    if start == end:
        return None
    root_index = dp_root[start][end]
    key = lines[root_index][0]
    left = build_tree(dp_root, lines, start, root_index)
    right = build_tree(dp_root, lines, root_index + 1, end)
    return Node(key, left, right)


def build_tree2(dp_root, lines, start, end):
    if start > end:
        return None
    root_index = dp_root[start][end] - 1  # Adjust for 0-based indexing
    key = lines[root_index][0]
    left = build_tree2(dp_root, lines, start, root_index - 2)  # Adjust indices accordingly
    right = build_tree2(dp_root, lines, root_index + 2, end)  # Adjust indices accordingly
    return Node(key, left, right)


def add_nodes_edges(G, node, pos=None, x=0, y=0, layer=1):
    if pos is None:
        pos = {}
    pos[node.key] = (x, y)
    if node.left is not None:
        G.add_edge(node.key, node.left.key)
        pos = add_nodes_edges(G, node.left, pos, x - 1 / layer, y - 1, layer * 2)
    if node.right is not None:
        G.add_edge(node.key, node.right.key)
        pos = add_nodes_edges(G, node.right, pos, x + 1 / layer, y - 1, layer * 2)
    return pos


def print_tree(tree):
    G = nx.DiGraph()
    pos = add_nodes_edges(G, tree)
    nx.draw(G, pos, with_labels=True, node_color='white', font_size=6, arrows=False)
    plt.show()


def compare_trees(tree, tree2):
    if tree is None and tree2 is None:
        return True
    if tree is None or tree2 is None:
        return False
    return compare_trees(tree.left, tree2.left) and compare_trees(tree.right, tree2.right)


def binary_search(tree, word, comparisons=0):
    if tree is None:
        return False, comparisons
    comparisons += 1
    if tree.key == word:
        return True, comparisons
    if tree.key > word:
        return binary_search(tree.left, word, comparisons)
    return binary_search(tree.right, word, comparisons)


def main():
    triplets = create_triplets_k_p_q()
    triplets_to_print = triplets.copy()
    triplets_to_print.pop(0)
    c1, root1 = calculate_tables(len(triplets) - 1, [triplet[1] for triplet in triplets],
                                 [triplet[2] for triplet in triplets])

    print(c1[0][-1])

    c2, root2 = calculate_tables2(len(triplets) - 1, [triplet[1] for triplet in triplets],
                                  [triplet[2] for triplet in triplets])

    print(c2[1][-2]) \
        # remove first element in root2
    root2 = root2[1:]
    for i in range(len(root2)):
        for j in range(len(root2[i])):
            root2[i][j] -= 1

    tree = build_tree(root1, triplets_to_print, 0, len(triplets_to_print) - 1)
    print_tree(tree)
    tree2 = build_tree(root2, triplets_to_print, 0, len(triplets_to_print) - 1)
    print_tree(tree2)

    print(compare_trees(tree, tree2))
    for word in triplets:
        print(word[0], binary_search(tree, word[0]))

    return True


main()
