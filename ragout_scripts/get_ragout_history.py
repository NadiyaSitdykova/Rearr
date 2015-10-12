import sys

WORKDIR = "/home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-chimp/ragout/out/"

def get_left(gene):
    if gene > 0:
        return str(gene) + "h"
    return str(-1 * gene) + "t"

def get_right(gene):
    if gene > 0:
        return str(gene) + "t"
    return str(-1 * gene) + "h"

blocks_file = WORKDIR + "sibelia-workdir/5000/genomes_permutations.txt"
scaffolds_file = WORKDIR + "scaffolds.ord"
length = sys.argv[1]
identity = sys.argv[2]

seqs = {}
with open(blocks_file, 'r') as file:
    line1 = file.readline()
    line2 = file.readline()
    while line1:
        seqs[line1.strip()[1:]] = line2.split()[:-1]
        line1 = file.readline()
        line2 = file.readline()

with open(WORKDIR + "logs/" + str(length) + "_" + str(identity) + "_ragout_log.txt", 'w') as out:
    with open(scaffolds_file, 'r') as file:
        line1 = file.readline().strip()
        line2 = file.readline().strip()
        while line2:
            if line1[0] != ">" and line2[0] != ">":
                out.write(line1[1:].split("_")[0] + " ")
                if line1[0] == "+":
                    out.write(get_left(int(seqs[line1[1:]][-1])) + " ")
                else:
                    out.write(get_left(-1 * int(seqs[line1[1:]][0])) + " ")
                if line2[0] == "+":
                    out.write(get_right(int(seqs[line2[1:]][0])) + "\n")
                else:
                    out.write(get_right(-1 * int(seqs[line2[1:]][-1])) + "\n")
            line1 = line2
            line2 = file.readline().strip()