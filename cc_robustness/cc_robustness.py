from random import seed, randint
from subprocess import Popen, PIPE
import sys
import io_utils
import prepare_data

count_of_steps = 20 # 24
count_of_iterations = 10
count_of_breakages_by_step = 5 #50

class ReturnedError(Exception): pass

def run(command, input="", binaryout=False, encoding="UTF-8",
        stdin=PIPE, stdout=PIPE, stderr=PIPE):
    """Returns result of running 'command'.
    'command' can be string (will be split) or a list."""

    #Deal with unicode
    #If you want some other encoding, send us bytes.
    #if isinstance(input, unicode):
    #    input = input.encode(encoding)

    #Subprocess wants a list of commands
    if hasattr(command, "split"):
        command = command.split()

    process = Popen(command, stdin=stdin, stdout=stdout, stderr=stderr)
    output, err = process.communicate(input)

    if not binaryout:
        output = output.decode(encoding)

    #Raise errors, but make the output salvagable
    if err:
        print("err")
        print(err)
        print("out")
        print(output)
        e = ReturnedError(err)
        e.output = output
        raise e

    return output

def get_left(s):
    if s[0] == '-':
        return s[1:] + 't'
    else:
        return s[1:] + 'h'

def get_right(s):
    if s[0] == '-':
        return s[1:] + 'h'
    else:
        return  s[1:] + 't'

def forbidden(g, x, y, z, complete_multiedges):
    if len(g[x][y]) == 1:
        return True
    left = get_left(g[x][y][z - 1])
    if left in complete_multiedges and complete_multiedges[left] == get_right(g[x][y][z]):
        return True
    else:
        return False

def breakage(x, g, complete_multiedges):
    #x = number of genome
    y = randint(0, len(g[x]) - 1)    #number of chromosome
    if len(g[x][y]) <= 2:
        z = 1
    else:
        z = randint(1, len(g[x][y]) - 1) #point of breakage
    while forbidden(g, x, y, z, complete_multiedges):
        y = randint(0, len(g[x]) - 1)
        if len(g[x][y]) <= 2:
            z = 1
        else:
            z = randint(1, len(g[x][y]) - 1) #point of breakage
    g[x].append(g[x][y][z:])
    g[x][y] = g[x][y][:z]

def step(n, g, names, complete_multiedges, cfg_file, path_to_mgra):
    for _ in range(0, n):
        for i in range(0, len(g)):
            breakage(i, g, complete_multiedges)
    io_utils.write_genomes("blocks.txt", g, names)
    run(path_to_mgra + " -c " + cfg_file + " -g blocks.txt -o out")
    cc_count = io_utils.read_count_of_cc("out/stats.txt")
    return int(cc_count)

def iteration(blocks_file, cfg_file, complete_multiedges, path_to_mgra):
    g, names, y = [], [], []
    io_utils.read_genomes(blocks_file, g, names)
    y.append(step(0, g, names, complete_multiedges, cfg_file, path_to_mgra))
    for _ in range(0, count_of_steps):
        y.append(step(count_of_breakages_by_step, g, names, complete_multiedges, cfg_file, path_to_mgra))
    return y


def subset_processing(blocks_file, cfg_file, path_to_mgra):
    seed(5)
    g, names = [], []
    io_utils.read_genomes(blocks_file, g, names)
    io_utils.write_genomes("blocks.txt", g, names)
    #prepare stats.txt to get complete multiedges
    run(path_to_mgra + " -c " + cfg_file + " -g blocks.txt -o out")

    complete_multiedges = {}
    io_utils.read_complete_multiedges("out/stats.txt", complete_multiedges)

    ys = []
    for i in range(0, count_of_iterations):
        #print(i)
        ys.append(iteration(blocks_file, cfg_file, complete_multiedges, path_to_mgra))

    mean = list(map(lambda x: float(sum(x))/count_of_iterations, list(zip(*ys))))

    return mean


if len(sys.argv) < 5:
    print("Usage: python3 cc_robustness.py <dataset_name> <size_of_subset> <file_with_blocks> <path_to_mgra>")
    print("Example: python3 cc_rubustness.py MRDQHC 4 mgra/examples/mam6/blocks.txt mgra/build/mgra")
    exit()
dataset = sys.argv[1] # string of letters, which represnt genomes (MRDQHC)
k = int(sys.argv[2]) # size of subset
filename = sys.argv[3] # file with blocks for all genomes
path_to_mgra = sys.argv[4]
subsets = prepare_data.get_list_of_subsets(k, dataset)
ys = []
for subset in subsets:
    #print(subset)
    prepare_data.generate_blocks_for_subset(subsets[0], filename, "tmp.txt")
    prepare_data.generate_cfg_for_subset(subsets[0], "tmp.cfg")
    ys.append(subset_processing("tmp.txt", "tmp.cfg", path_to_mgra))

mean = list(map(lambda x: float(sum(x))/len(subsets), list(zip(*ys))))

with open("mean.txt", 'w') as out:
        s = ""
        for i in range(0, len(mean)):
            s += str(round(mean[i], 4)) + " "
        print(s, file=out)