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
            print(str(element).ljust(5), end='')
        print()
    print()
    for row in dp_root:
        for element in row:
            print(str(element).ljust(5), end='')
        print()


def main():
    file_path = 'easy.txt'
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    lines = [line.strip().split(' ') for line in lines]
    lines = [[int(line[0]), line[1]] for line in lines]
    # lines = [line for line in lines if line[0] >= 50000]
    lines = sorted(lines, key=lambda x: x[1])
    # sum_freq = sum([line[0] for line in lines])
    # lines = [[line[0] / sum_freq, line[1]] for line in lines]
    dp_cost, dp_root = create_dp_arrays(lines)
    print_dp(dp_cost, dp_root)


main()
