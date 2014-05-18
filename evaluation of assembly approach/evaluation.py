from random import seed, randint
from subprocess import Popen, PIPE
import sys

class ReturnedError(Exception): pass

def run(command, input="", binaryout=False, encoding="UTF-8",
        stdin=PIPE, stdout=PIPE, stderr=PIPE):

    if hasattr(command, "split"):
        command = command.split()

    process = Popen(command, stdin=stdin, stdout=stdout, stderr=stderr)
    output, err = process.communicate(input)

    if not binaryout:
        output = output.decode(encoding)

    if err:
        print("err")
        print(err)
        print("out")
        print(output)
        e = ReturnedError(err)
        e.output = output
        raise e

    return output

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
                    names.append(line.strip()[1:])
                    g.append([])
                else:
                    j += 1
                    g[i].append([])
                    for k in range(0, len(blocks) - 1):
                        g[i][j].append(blocks[k])

def write_genomes(output, g, names):
    with open(output, 'w') as out:
        for i in range(0, len(g)):
            print(">" + names[i], file=out)
            for j in range(0, len(g[i])):
                s = ""
                for k in range(0, len(g[i][j])):
                    s += g[i][j][k] + " "
                print(s + "$", file=out)
            print(file=out)

def get_left(s):
    if s[0] == '-':
        return s[1:] + 't'
    else:
        return s + 'h'

def get_right(s):
    if s[0] == '-':
        return s[1:] + 'h'
    else:
        return s + 't'

def get_initial_fragment_ends():
    g, names = [], []
    read_genomes(source_data, g, names)
    initial_fragment_ends = [{} for i in range(0, len(g))]
    for i in range(0, len(g)): #genome
        for j in range(0, len(g[i])): #chromosome
            initial_fragment_ends[i][get_right(g[i][j][0])] = True # left end of chromosome
            initial_fragment_ends[i][get_left(g[i][j][len(g[i][j]) - 1])] = True # right end of chromosome
    return initial_fragment_ends

def process_logfile(g, names):
    positive = [[{} for _ in range(0, len(g))] for _ in range(0, 2)]
    with open("mgra.log") as file:
        stage_number = 0
        cur_line_is_fusions_info_on_stage12 = False
        cur_line_is_fusion_info_on_stage1 = False
        cur_line_is_2break_info_on_stage2 = False
        for line in file:
            if line.strip() == "Stage 12: Merging double VTconcistent irregular edges":
                    cur_line_is_fusions_info_on_stage12 = True

            elif line.strip() == "Stage: 1":
                    stage_number = 1

            elif line.strip() == "Stage: 2":
                    stage_number = 2
                    cur_line_is_2break_info_on_stage2 = True

            elif stage_number == 1 and line.strip() == "... semi-cycle, fusion applied":
                cur_line_is_fusion_info_on_stage1 = True

            elif cur_line_is_fusions_info_on_stage12:
                if line.strip() != "0 2-breaks performed":
                    blocks = line.split()
                    for i in range(0, len(blocks) - 3):
                        X = blocks[i].split('x')
                        label1 = X[0].split(',')[0][1:]
                        tmp = X[1].split(':')
                        label2 = tmp[0].split(',')[0][1:]
                        genome = names.index(tmp[1][1])
                        if stage_number == 0:
                            positive[0][genome][label1] = label2
                        else:
                            positive[1][genome][label1] = label2
                cur_line_is_fusions_info_on_stage12 = False

            elif cur_line_is_fusion_info_on_stage1:
                blocks = line.split()
                X = blocks[0].split('x')
                label1 = X[0][4:(len(X[0]) - 1)]
                tmp = X[1].split(':')
                label2 = tmp[0][4:(len(tmp[0]) - 1)]
                genome = names.index(tmp[1][1])
                positive[1][genome][label1] = label2
                cur_line_is_fusion_info_on_stage1 = False

            elif cur_line_is_2break_info_on_stage2:
                if len(line.split()) > 1:
                    cur_line_is_2break_info_on_stage2 = False
                else:
                    X = line.split('x')
                    label1 = X[0].split(',')[0][2:]
                    tmp = X[1].split(':')
                    label2 = tmp[0].split(',')[0][1:]
                    genome = names.index(tmp[1][1])
                    if X[0].split(',')[1] == "oo)" and tmp[0].split(',')[1] == "oo)":
                        positive[1][genome][label1] = label2
    return positive

def breakage(g, real_breakages):
    for x in range(0, len(g)):
        y = randint(0, len(g[x]) - 1)    #number of chromosome
        while len(g[x][y]) == 1:
            y = randint(0, len(g[x]) - 1)
        if len(g[x][y]) == 2:
            z = 1
        else:
            z = randint(1, len(g[x][y]) - 1) #point of breakage
        real_breakages[x][get_left(g[x][y][z - 1])] = get_right(g[x][y][z])
        real_breakages[x][get_right(g[x][y][z])] = get_left(g[x][y][z - 1])
        g[x].append(g[x][y][z:])
        g[x][y] = g[x][y][:z]


def iteration():
    g, names = [], []
    tp, fp, fn = [0 for _ in range(0, 3)], [0 for _ in range(0, 3)], [0 for _ in range(0, 3)]
    read_genomes(source_data, g, names)
    real_breakages = [{} for _ in range(0, len(g))]
    count_of_breakages = randint(30, 1200)

    #generate breakages
    for _ in range(0, count_of_breakages):
        breakage(g, real_breakages)
    write_genomes("blocks.txt", g, names)

    run("mgra_assembly_my/src/mgra.bin mam6.cfg")

    #parse log and compute tp, fp, fn
    positive = process_logfile(g, names)

    for i in range(0, 2):
        for j in range(0, len(g)):
            for label1, label2 in positive[i][j].items():
                if label1 in real_breakages[j] and real_breakages[j][label1] == label2:
                    tp[i] += 1
                    tp[2] += 1
                elif label1 in initial_fragment_ends[j] and label2 in initial_fragment_ends[j] or label1 in real_breakages[j] and label2 in real_breakages:
                    fp[i] += 1
                    fp[2] += 1

    for i in range(0, 3):
        fn[i] = count_of_breakages * 6 - tp[i]

    tp = list(map(lambda x: float(x * 100)/(6 * count_of_breakages), tp))
    fp = list(map(lambda x: float(x * 100)/(6 * count_of_breakages), fp))
    fn = list(map(lambda x: float(x * 100)/(6 * count_of_breakages), fn))

    return tp, fp, fn

count_of_iterations = 100
source_data = "MRDQHC.txt"

TP, FP, FN = [], [], []
initial_fragment_ends = get_initial_fragment_ends()
for i in range(0, count_of_iterations):
    print(i)
    tp, fp, fn = iteration()
    TP.append(tp)
    FP.append(fp)
    FN.append(fn)

    tp = list(map(lambda x: sum(x)/count_of_iterations, list(zip(*TP))))
    fp = list(map(lambda x: sum(x)/count_of_iterations, list(zip(*FP))))
    fn = list(map(lambda x: sum(x)/count_of_iterations, list(zip(*FN))))

with open("statistic.txt", 'w') as out:
    print("True positive: " + str(tp), file=out)
    print("False positive: " + str(fp), file=out)
    print("False negative: " + str(fn), file=out)








