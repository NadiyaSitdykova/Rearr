def read_grimm(input, g, names):
    with open (input, 'r') as file:
        i = -1
        for line in file:
            blocks = line.split()
            if len(blocks) > 0:
                if blocks[0][0] == '>':
                    i += 1
                    names.append(blocks[0][1:])
                    g.append([])
                else:
                    g[i].append(blocks[:-1])

def write_grimm(output, g, names):
    with open(output, 'w') as out:
        for i in range(0, len(g)):
            out.write(">" + names[i] + "\n")
            for j in range(0, len(g[i])):
                s = ""
                for k in range(0, len(g[i][j])):
                    s += g[i][j][k] + " "
                out.write(s + "$\n")
