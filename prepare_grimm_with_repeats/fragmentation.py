import io_utils
from random import seed, randint

def do_fragmentation(x, g, assistent, forbidden):
    #x = number of genome
    y = randint(0, len(g[x]) - 1)    #number of chromosome
    if len(g[x][y]) <= 2:
        z = 1
    else:
        z = randint(1, len(g[x][y]) - 1) #point of breakage
    while forbidden(g, x, y, z):
        y = randint(0, len(g[x]) - 1)
        if len(g[x][y]) <= 2:
            z = 1
        else:
            z = randint(1, len(g[x][y]) - 1) #point of breakage
    g[x].append(g[x][y][z:])
    if assistent:
        g[x][y] = g[x][y][:(z + 1)]
        g[x][-1][0] += "_break"
        g[x][y][z] += "_break"
    else:
        g[x][y] = g[x][y][:z]

def chrome_len_one(g, x, y, z):
    return len(g[x][y]) == 1

def is_not_repeat(g, x, y, z):
    return chrome_len_one(g, x, y, z) or len(g[x][y][z]) < 6 or g[x][y][z][-6:] != "repeat"

def remove_repeats(g):
    new_g = []
    for genome in g:
        new_genome = []
        for chrome in genome:
            new_chrome = []
            for block in chrome:
                if len(block) < 6 or block[-6:] != "repeat":
                    new_chrome.append(block)
            if len(new_chrome) > 0:
                new_genome.append(new_chrome)
        new_g.append(new_genome)
    return  new_g

def fragmentation(type, num, input, output):
    g = []
    names = []
    io_utils.read_grimm(input, g, names)
    if type == "random":
        g = remove_repeats(g)
    for _ in range(0, num):
        for i in range(0, len(g)):
            if type == "random":
                do_fragmentation(i, g, False, chrome_len_one)
            elif type == "plain":
                do_fragmentation(i, g, False, is_not_repeat)
            elif type == "assisted":
                do_fragmentation(i, g, True, is_not_repeat)
            else:
                print("Type should be random, plain or assisted")
    if type == "plain":
        g = remove_repeats(g)
    elif type == "assisted":
        g = remove_repeats(g)
    io_utils.write_grimm(output, g, names)

if __name__ == '__main__':
    fragmentation("random", 10, "out.txt", "random.txt")
    fragmentation("plain", 10, "out.txt", "plain.txt")
    fragmentation("assisted", 10, "out.txt", "assisted.txt")

