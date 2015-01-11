import sys

def read_genomes(inputfile):
    genomes = {}
    with open(inputfile, 'r') as f:
        name = ""
        line = f.readline()
        while line:
            if line[0] == '>':
                name = line[1:].strip()
                genomes[name] = {}
            else:
                chrome = [abs(int(i)) for i in line.split()[0:-1]]
                for block in chrome:
                    genomes[name][block] = True
            line = f.readline()
    return genomes

def get_shared(genomes):
    shared = {}
    first_name = list(genomes.keys())[0]
    for block in genomes[first_name]:
        is_shared = True
        for _, blocks in genomes.items():
            if block not in blocks:
                is_shared = False
                break
        if is_shared:
            shared[block] = True
    return shared

def get_indels(genomes, shared):
    indels = {}
    for name, blocks in genomes.items():
        for block in blocks:
            if block not in shared:
                indels[block] = True
    return indels


def get_shared_indels1(genomes, indels, subset):
    indels_in_subset = []
    shared_indels = []
    for block, _ in indels.items():
        if block in genomes[subset]:
            indels_in_subset.append(block)

    for block in indels_in_subset:
        for name, blocks in genomes.items():
            if name != subset:
                if block in blocks:
                    shared_indels.append(block)
                    break

    return  shared_indels


def get_shared_indels2(genomes, indels, subset):
    indels_in_subset = []
    shared_indels = []
    for block, _ in indels.items():
        if block in genomes[subset[0]] and block in genomes[subset[1]]:
            indels_in_subset.append(block)

    for block in indels_in_subset:
        for name, blocks in genomes.items():
            if name != subset[0] and name != subset[1]:
                if block in blocks:
                    shared_indels.append(block)
                    break

    return shared_indels


inputfile = sys.argv[1]
dataset = sys.argv[2]

genomes = read_genomes(inputfile)
shared = get_shared(genomes)
indels = get_indels(genomes, shared)
shared_indels = []
if len(dataset) == 1:
    shared_indels = get_shared_indels1(genomes, indels, dataset)
if len(dataset) == 2:
    shared_indels = get_shared_indels2(genomes, indels, dataset)

print(dataset)
#print("shared blocks: "+ str(len(shared)))
#print("all indels: " + str(len(indels)))
print("indels in subset and somewhere else: " + str(len(shared_indels)))
print


