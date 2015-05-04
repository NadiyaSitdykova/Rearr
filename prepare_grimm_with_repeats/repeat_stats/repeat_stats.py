import sys

class Gene_info(object):
    def __init__(self, id, start, end, strand, identity, is_repeat):
        self.id = id
        self.start = start
        self.end = end
        self.strand = strand
        self.length = abs(end - start) - 1
        self.mid = (start + end) / 2
        self.identity = identity
        self.is_repeat = is_repeat

def read_gene_data_file(filename, genomes, genome_name):
    with open(filename, 'r') as file:
        if genome_name not in genomes:
            genomes[genome_name] = {}
        for line in file.readlines():
            blocks = line.split()
            if blocks[0] != "Ensembl":
                if blocks[1] not in genomes[genome_name]:
                    genomes[genome_name][blocks[1]] = []
                genomes[genome_name][blocks[1]].append(Gene_info(blocks[0], int(blocks[2]), int(blocks[3]), int(blocks[4]), 100, False))

def read_repeats_file(filename, genomes, genome_name):
    with open(filename, 'r') as file:
        if genome_name not in genomes:
            genomes[genome_name] = {}
        for line in file.readlines():
            blocks = line.split()
            if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                if blocks[4][3:] not in genomes[genome_name]: # chr1, chrX format of chromosome name
                    continue
                strand = 1
                if blocks[8] == 'C':
                    strand = -1
                identity = 100 - (float(blocks[1]) + float(blocks[2]) + float(blocks[3]))
                genomes[genome_name][blocks[4][3:]].append(Gene_info(blocks[9], int(blocks[5]), int(blocks[6]), strand, identity, True))


if __name__ == '__main__':
    genomes = {}
    names = ["human", "chimp", "mouse", "rat", "dog", "cat", "opossum"]
    gene_data_files = ["../data/diverse_vertebrate_dataset/Human/gene_data.txt", "../data/diverse_vertebrate_dataset/Chimp/gene_data.txt", "../data/diverse_vertebrate_dataset/Mouse/gene_data.txt", "../data/diverse_vertebrate_dataset/Rat/gene_data.txt", "../data/diverse_vertebrate_dataset/Dog/gene_data.txt", "../data/diverse_vertebrate_dataset/Cat/gene_data.txt", "../data/diverse_vertebrate_dataset/Opossum/gene_data.txt"]
    repeats_files = ["../data/diverse_vertebrate_dataset/Human/filtered_hg38.fa.out", "../data/diverse_vertebrate_dataset/Chimp/filtered_panTro2.fa.out", "../data/diverse_vertebrate_dataset/Mouse/filtered_mm10.fa.out", "../data/diverse_vertebrate_dataset/Rat/filtered_rn5.fa.out", "../data/diverse_vertebrate_dataset/Dog/filtered_canFam3.fa.out", "../data/diverse_vertebrate_dataset/Cat/filtered_felCat5.fa.out", "../data/diverse_vertebrate_dataset/Opossum/filtered_monDom5.fa.out"]

    #read gene_data and repeatmasker's files
    for i in range(0, len(names)):
        #print(names[i])
        read_gene_data_file(gene_data_files[i], genomes, names[i])
        read_repeats_file(repeats_files[i], genomes, names[i])

    #sort genes inside chromosomes
    for genome, chromes in genomes.items():
        for chrome, genes in chromes.items():
            genes.sort(key=lambda x: x.mid)

    #compute and print stat data
    x_start = 400
    y_start = 70
    x_end = 3000
    y_end = 100
    x_mult = 100
    y_mult = 1
    xs_count = int((x_end - x_start) / x_mult) + 1
    ys_count = int((y_end - y_start) / y_mult) + 1
    ys_count = int((y_end - y_start) / y_mult) + 1
    with open("stats.out", 'w') as out:
        for genome, chromes in genomes.items():
            #print(genome)
            out.write(">" + genome + "\n")
            lens = [[0 for _ in range(0, ys_count)] for _ in range(0, xs_count)]
            count = [[0 for _ in range(0, ys_count)] for _ in range(0, xs_count)]
            average = [[0 for _ in range(0, ys_count)] for _ in range(0, xs_count)]
            for chrome, genes in chromes.items():
                prev_is_repeat = [[True for _ in range(0, ys_count)] for _ in range(0, xs_count)]
                for gene in genes:
                    if not gene.is_repeat:
                        prev_is_repeat = [[False for _ in range(0, ys_count)] for _ in range(0, xs_count)]
                        for i in range(0, len(lens)):
                            for j in range(0, len(lens[i])):
                                lens[i][j] += 1
                    else:
                        #define minimal length and identity indecies for which this repeat is considered
                        length_index = int((gene.length - x_start) / x_mult) + 1
                        identity_index = int((gene.identity - y_start) / y_mult) + 1
                        for i in range(0, min(length_index, len(count))):
                            for j in range(0, min(identity_index, len(count[i]))):
                                if not prev_is_repeat[i][j]:
                                    count[i][j] += 1
                                    prev_is_repeat[i][j] = True

                for i in range(0, len(prev_is_repeat)):
                    for j in range(0, len(prev_is_repeat[i])):
                        if not prev_is_repeat[i][j]:
                            count[i][j] += 1

            out.write("Count:\n")
            for i in range(0, len(count)):
                for j in range(0, len(count[i])):
                    out.write(str(count[i][j]) + " ")
                out.write("\n")

            out.write("Average length:\n")
            for i in range(0, len(count)):
                for j in range(0, len(count[i])):
                    average[i][j] = float(lens[i][j]) /count[i][j]
                    out.write(str(average[i][j]) + " ")
                out.write("\n")















