def prepare_dynamic_programming(lines):
    size = len(lines) + 1
    dp = [[None for _ in range(size)] for _ in range(size)]

    # 0 nodes in the tree
    for i in range(size):
        dp[i][i] = 0

    return dp


def get_w(dic, start, end):
    w = 0
    l = end - start
    for i in range(start, start + l):
        w += dic[i][0]
    return w


def get_c(start, end):
    pass


def get_combinations_of_c(m, l):
    tuples = [(x, x + l) for x in range(m - l)]
    return tuples


def dynamic_programming(dic, dp):
    size_dp = len(dp)
    for l in range(1, len(dp)):
        combs_c = get_combinations_of_c(size_dp, l)
        for c in combs_c:
            w = get_w(dic, c[0], c[1])
            min_cost = float('inf')
            for i in range(c[0], c[1]):
                cost = dp[c[0]][i] + dp[i + 1][c[1]] + w
                if cost < min_cost:
                    min_cost = cost
            dp[c[0]][c[1]] = min_cost

    return dp


def print_dp(dp):
    for row in dp:
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
    dp = prepare_dynamic_programming(lines)
    dp = dynamic_programming(lines, dp)
    print_dp(dp)


main()
