import sys
import node

class Gene_info(object):
    def __init__(self, id, start, end, strand, is_repeat):
        self.id = id
        self.start = start
        self.end = end
        self.strand = strand
        self.mid = (start + end) / 2
        self.is_repeat = is_repeat

def read_gene_data_file(filename, gene_to_label, genomes, genome_name):
    with open(filename, 'r') as file:
        if genome_name not in genomes:
            genomes[genome_name] = {}
        for line in file.readlines():
            blocks = line.split()
            if blocks[0] != "Ensembl":
                gene_to_label[blocks[0]] = 0
                if blocks[1] not in genomes[genome_name]:
                    genomes[genome_name][blocks[1]] = []
                genomes[genome_name][blocks[1]].append(Gene_info(blocks[0], int(blocks[2]), int(blocks[3]), int(blocks[4]), False))

def read_repeats_file(filename, repeat_to_label, genomes, genome_name):
    with open(filename, 'r') as file:
        if genome_name not in genomes:
            genomes[genome_name] = {}
        for line in file.readlines():
            blocks = line.split()
            if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                repeat_to_label[blocks[9]] = 0
                if blocks[4][3:] not in genomes[genome_name]: # chr1, chrX format of chromosome name
                    #print(blocks[4])
                    #genomes[genome_name][blocks[4][3:]] = []
                    continue
                strand = 1
                if blocks[8] == 'C':
                    strand = -1
                genomes[genome_name][blocks[4][3:]].append(Gene_info(blocks[9], int(blocks[5]), int(blocks[6]), strand, True))



def process_paralogs(filename, nodes, gene_to_num):
    with open(filename, 'r') as file:
        for line in file.readlines():
            blocks = line.split()
            if blocks[0] != "Ensembl":
                if len(blocks) == 1:
                    continue
                if blocks[1] in gene_to_num: #some paralogs could be from additional chromosomes
                    i = gene_to_num[blocks[0]]
                    j = gene_to_num[blocks[1]]
                    node.join(nodes, i, j)


def process_orthologs(filename, nodes, gene_to_num):
    with open(filename, 'r') as file:
        for line in file.readlines():
            blocks = line.split();
            if blocks[0] != "Ensembl":
                i = gene_to_num[blocks[0]]
                for gene in blocks:
                    if gene in gene_to_num: #some orthologs could be from additional chromosomes
                        j = gene_to_num[gene]
                        node.join(nodes, i, j)

if __name__ == '__main__':
    gene_to_label = {}
    repeat_to_label = {}
    repeats = {}
    genomes = {}
    names = ["human", "chimp", "mouse", "rat", "dog", "cat", "opossum"]
    gene_data_files = ["data/diverse_vertebrate_dataset/Human/gene_data.txt", "data/diverse_vertebrate_dataset/Chimp/gene_data.txt", "data/diverse_vertebrate_dataset/Mouse/gene_data.txt", "data/diverse_vertebrate_dataset/Rat/gene_data.txt", "data/diverse_vertebrate_dataset/Dog/gene_data.txt", "data/diverse_vertebrate_dataset/Cat/gene_data.txt", "data/diverse_vertebrate_dataset/Opossum/gene_data.txt"]
    paralogs_files = ["data/diverse_vertebrate_dataset/Human/paralogs.txt", "data/diverse_vertebrate_dataset/Chimp/paralogs.txt", "data/diverse_vertebrate_dataset/Mouse/paralogs.txt", "data/diverse_vertebrate_dataset/Rat/paralogs.txt", "data/diverse_vertebrate_dataset/Dog/paralogs.txt", "data/diverse_vertebrate_dataset/Cat/paralogs.txt", "data/diverse_vertebrate_dataset/Opossum/paralogs.txt"]
    orthologs_files = ["data/diverse_vertebrate_dataset/Human/orthologs.txt", "data/diverse_vertebrate_dataset/Chimp/orthologs.txt", "data/diverse_vertebrate_dataset/Mouse/orthologs.txt", "data/diverse_vertebrate_dataset/Rat/orthologs.txt", "data/diverse_vertebrate_dataset/Dog/orthologs.txt", "data/diverse_vertebrate_dataset/Cat/orthologs.txt", "data/diverse_vertebrate_dataset/Opossum/orthologs.txt"]
    repeats_files = ["data/diverse_vertebrate_dataset/Human/300_hg38.fa.out", "data/diverse_vertebrate_dataset/Chimp/300_panTro4.fa.out", "data/diverse_vertebrate_dataset/Mouse/300_mm10.fa.out", "data/diverse_vertebrate_dataset/Rat/300_rn5.fa.out", "data/diverse_vertebrate_dataset/Dog/300_canFam3.fa.out", "data/diverse_vertebrate_dataset/Cat/300_felCat5.fa.out", "data/diverse_vertebrate_dataset/Opossum/300_monDom5.fa.out"]
    nodes = []

    for i in range(0, len(names)):
        read_gene_data_file(gene_data_files[i], gene_to_label, genomes, names[i])
        read_repeats_file(repeats_files[i], repeats, genomes, names[i])

    i = 0
    gene_to_num = {}
    for k, v in gene_to_label.items():
        nodes.append(node.Node(i, k))
        gene_to_num[k] = i
        i += 1

    for i in range(0, len(names)):
        print(names[i])
        process_paralogs(paralogs_files[i], nodes, gene_to_num)
        process_orthologs(orthologs_files[i], nodes, gene_to_num)

    cur_label = 1
    for repeat, v in repeats.items():
        repeat_to_label[repeat] = cur_label
        cur_label += 1
    #print(len(repeat_to_label))

    processed = {}
    cur_label = 1
    for i in range(0, len(nodes)):
        n = nodes[node.find(nodes, i)]
        if n.gene_names[0] not in processed:
            for gene in n.gene_names:
                processed[gene] = True
                gene_to_label[gene] = cur_label
            cur_label += 1

    #print(len(gene_to_num))
    #print(cur_label)

    for genome, chromes in genomes.items():
        for chrome, genes in chromes.items():
            genes.sort(key=lambda x: x.mid)

    with open("out.txt", 'w') as out:
        for genome, chromes in genomes.items():
            out.write(">" + genome)
            for chrome, genes in chromes.items():
                s = ""
                for gene in genes:
                    if gene.is_repeat:
                        s += str(gene.strand * repeat_to_label[gene.id]) + "_repeat "
                    else:
                        s += str(gene.strand * gene_to_label[gene.id]) + " "
                s += "$"
                out.write(s)











