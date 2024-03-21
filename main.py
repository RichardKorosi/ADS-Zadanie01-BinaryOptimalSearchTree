import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

    def __str__(self):
        return f'Node(Key:{self.key},Left:{self.left},Right{self.right})'


def prepare_dp_arrays(lines):
    #  size + 1. pretoze chceme aj pripad ked je 0 uzlov v strome
    size = len(lines) + 1
    dp_cost = [[None for _ in range(size)] for _ in range(size)]
    dp_root = [[None for _ in range(size)] for _ in range(size)]

    # Diagonala nul, kde nemame ziadne uzly
    for i in range(size):
        dp_cost[i][i] = 0

    return dp_cost, dp_root


def get_w(dic, start, end):
    # dic je pole kde kazdy prvok je tuple (frekvencia/pravdepodobnost, slovo)
    # start a end su indexy do pola dic
    # l je pocet uzlov v strome
    w = 0
    l = end - start
    for i in range(start, start + l):
        w += dic[i][0]
    return w


def get_combinations_of_c(m, l):
    # vytvor dvojice s rozdielom medzi prvkami l
    # m je maximalny index v poli
    # napr pre m = 4 a l = 2 vytvori [(0, 2), (1, 3), (2, 4)]
    tuples = [(x, x + l) for x in range(m - l + 1)]
    return tuples


def min_cost(dic, dp_cost, dp_root, c):
    cl, cr = c[0], c[1]
    w = get_w(dic, cl, cr)
    mini = float('inf')
    mini_root = None

    for i in range(cl, cr):
        cost = dp_cost[cl][i] + dp_cost[i + 1][cr] + w
        if cost < mini:
            mini = cost
            mini_root = i
    dp_cost[cl][cr] = mini
    dp_root[cl][cr] = mini_root


def create_dp_arrays(dic):
    dp_cost, dp_root = prepare_dp_arrays(dic)
    for l in range(1, len(dp_cost)):
        combs_c = get_combinations_of_c(len(dic), l)
        for c in combs_c:
            min_cost(dic, dp_cost, dp_root, c)
    return dp_cost, dp_root


def print_dp(dp_cost, dp_root):
    for row in dp_cost:
        for element in row:
            if element is None:
                print('None'.ljust(9), end='')
            else:
                print(str(round(element, 3)).ljust(9), end='')
        print()
    print()
    for row in dp_root:
        for element in row:
            if element is None:
                print('None'.ljust(9), end='')
            else:
                print(str(round(element, 3)).ljust(9), end='')
        print()


def build_tree(dp_root, lines, start, end):
    if start == end:
        return None
    root_index = dp_root[start][end]
    key = lines[root_index][1]
    left = build_tree(dp_root, lines, start, root_index)
    right = build_tree(dp_root, lines, root_index + 1, end)
    return Node(key, left, right)


def plot_tree(root, x=0, y=0, spacing=100, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.axis('off')

    if root is not None:
        ax.plot(x, y, 'o', color='black')  # Plot the current node
        ax.text(x, y, str(root.key), verticalalignment='bottom', horizontalalignment='center')

        if root.left is not None:
            # Plot left child and edge
            new_spacing = spacing / 2
            ax.plot([x, x - new_spacing], [y, y - spacing], '-', color='black')
            plot_tree(root.left, x - new_spacing, y - spacing, new_spacing, ax)

        if root.right is not None:
            # Plot right child and edge
            new_spacing = spacing / 2
            ax.plot([x, x + new_spacing], [y, y - spacing], '-', color='black')
            plot_tree(root.right, x + new_spacing, y - spacing, new_spacing, ax)


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


def plot_tree_2(tree):
    G = nx.DiGraph()
    pos = add_nodes_edges(G, tree)
    nx.draw(G, pos, with_labels=True, node_color='white', font_size=6, arrows=False)
    plt.show()


def main():
    file_path = 'dictionary.txt'
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    lines = [line.strip().split(' ') for line in lines]
    lines = [[int(line[0]), line[1]] for line in lines]
    sum_freq = sum([line[0] for line in lines])
    lines = [line for line in lines if line[0] > 50000]
    lines = sorted(lines, key=lambda x: x[1])
    lines = [[line[0] / sum_freq, line[1]] for line in lines]
    dp_cost, dp_root = create_dp_arrays(lines)
    # print_dp(dp_cost, dp_root)

    root = build_tree(dp_root, lines, 0, len(lines))
    plot_tree_2(root)
    print(dp_cost[0][len(lines)])


main()
