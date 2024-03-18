def main():
    file_path = 'dictionary.txt'
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    lines = [line.strip().split(' ') for line in lines]
    lines = [[int(line[0]), line[1]] for line in lines]
    lines = [line for line in lines if line[0] >= 50000]
    lines = sorted(lines, key=lambda x: x[1])
    sum_freq = sum([line[0] for line in lines])
    lines = [[line[0]/sum_freq, line[1]] for line in lines]
    dictionary = {line[1]: line[0] for line in lines}
    print(dictionary)


main()
