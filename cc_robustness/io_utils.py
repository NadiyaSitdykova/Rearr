def read_genomes(input, g, names):
    with open (input, 'r') as file:
        i = -1
        j = -1
        for line in file:
            blocks = line.split()
            if len(blocks) > 0:
                if blocks[0][0] == '>':
                    i += 1
                    j = -1
                    names.append(line.strip())
                    g.append([])
                else:
                    j += 1
                    g[i].append([])
                    for k in range(0, len(blocks) - 1):
                        g[i][j].append(blocks[k])

def write_genomes(output, g, names):
    with open(output, 'w') as out:
        for i in range(0, len(g)):
            print(names[i], file=out)
            for j in range(0, len(g[i])):
                s = ""
                for k in range(0, len(g[i][j])):
                    s += g[i][j][k] + " "
                print(s + "$", file=out)
            print(file=out)

def read_complete_multiedges(filename, dictionary):
    with open(filename, 'r') as file:
        for i in range(0, 8):
            line = file.readline()
        blocks = line.split()
        for i in range(3, len(blocks) - 2):
            labels = blocks[i].split('~')
            dictionary[labels[0]] = labels[1]
            dictionary[labels[1]] = labels[0]

def read_count_of_cc(filename):
    with open(filename, 'r') as file:
        for i in range(0, 8):
            line = file.readline()
        res = -1 * int(line.split()[-1][0:-1])
        line = file.readline()
        blocks = line.split()
        for i in range(3, len(blocks)):
            res += int(blocks[i].split('^')[1])
    return res



