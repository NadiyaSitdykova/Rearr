__author__ = 'nadya'
import sys

WORKDIR = "/home/nadya/Desktop/master/rearr/evaluation/90+/primate/no_repeats/6-3/ragout/gorilla/"
GRIMMDIR = "/home/nadya/Desktop/master/prepare_data/extended_primate/grimm/"
TARGET = "gorilla"
GENOMES = ["human", "chimp", "orangutan", "macaque", "marmoset"]
FRAGMENTED = ["human", "chimp"]

length = sys.argv[1]
identity = sys.argv[2]

def write_fasta_and_permutations(file, out_fasta, out):
    line = file.readline()
    name = line.strip()[1:]
    i = 1
    line = file.readline()
    while line:
        out_fasta.write(">" + name + "_seq" + str(i) + "\n")
        out.write(">" + name + "_seq" + str(i) + "\n")
        out.write(line)
        i += 1
        line = file.readline()


with open(WORKDIR + "out/sibelia-workdir/5000/genomes_permutations.txt", 'w') as out:
    for genome in GENOMES:
        #process unfragmented genomes
        if genome not in FRAGMENTED:
            with open(GRIMMDIR + genome + ".txt", 'r') as file:
                with open(WORKDIR + "references/" + genome + ".fasta", 'w') as out_fasta:
                    write_fasta_and_permutations(file, out_fasta, out)
    #process fragmented genomes
    for genome in FRAGMENTED:
        with open(GRIMMDIR + str(length) + "_" + str(identity) + "/" + genome + ".txt", 'r') as file:
            with open(WORKDIR + "references/" + genome + ".fasta", 'w') as out_fasta:
                write_fasta_and_permutations(file, out_fasta, out)
    #process target genome
    with open(GRIMMDIR + str(length) + "_" + str(identity) + "/" + TARGET + ".txt", 'r') as file:
        with open(WORKDIR + TARGET + "_contigs.fasta", 'w') as out_fasta:
            write_fasta_and_permutations(file, out_fasta, out)




