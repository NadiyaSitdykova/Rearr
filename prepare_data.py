import sys
import raw_data_to_grimm

if len(sys.argv) != 2:
    print("rawDataToGrimm have one parameter <config>")

def read_cfg_line(cfg):
    line = cfg.readline()
    while(line[0] == '#' or line[0] == '\n'):
        line = cfg.readline()
    return line

#parse config with input information
gff_inputs, interest = [], []
with open(sys.argv[1], 'r') as cfg:
    subtree_name = read_cfg_line(cfg).strip()
    number_of_genomes = int(read_cfg_line(cfg))
    for i in range(0, number_of_genomes):
        blocks = read_cfg_line(cfg).split()
        interest.append(blocks[0].strip())
        gff_inputs.append(blocks[1].strip())
    tabtext_input = read_cfg_line(cfg).strip()

grimm_file_name = subtree_name + ".txt"

#create grimm file for mgra
raw_data_to_grimm.raw_data_to_grimm(number_of_genomes, interest, gff_inputs, tabtext_input, grimm_file_name)

#create config for mgra
with open(subtree_name + ".cfg", 'w') as out:
    print("""### Problem description
### section names enclosed in [...]; comments start with '#'; empty lines are ignored

### Given genomes aliases: one genome per line, multiple aliases possible, first alias must be a single unique letter
[Genomes]""", file=out)

    for i in range(0, number_of_genomes):
        print(chr(ord('A') + i) + " " + interest[i], file=out)

    print("""
### Description of synteny blocks
[Blocks]
## Currently supported input formats are `grimm' and `infercars'
format grimm""", file=out)
    print("file " + grimm_file_name, file=out)


    print("""
### Known subtrees of the phylogenetic tree of the above genomes in Newick format
### If no trees are given, MGRA assumes that only terminal branches are known (as in MGR)
[Trees]



### Options affecting algorithmic performance of MGRA.
[Algorithm]


## The number of stages to perform. Higher values correspond to less reliable heuristics.
## The highest value is 4 and usually it still requires manual completion (see below).
## Smaller values require `target' specification to produce ancestral reconstruction.
## It is not recommended to have stages higher than 3 if no complete phylogenetic tree is known.
stages 3


## By default, MGRA reconstructs all ancestral genomes but it first has to complete transformation into an identity breakpoint graph.
## If `target' is specified, MGRA focuses on reconstruction of the specified ancestral genome
## and can produce a partial reconstruction at any point (even if the transformation is not complete).
#target MRD



### Output breakpoint graphs before and after each stage
[Graphs]

## Breakpoint graphs will be saved as `stage0.dot' (initial graph), `stage1.dot' (after MGRA Stage 1), `stage2.dot' (after MGRA Stages 1-2), etc.
filename stage

## Edge coloring scheme. For colorscheme names see http://graphviz.org/doc/info/colors.html
colorscheme set19


### Manual (human-assisted) completion of T-consistent transformation (the last stage of MGRA).
### Each row contains exactly five terms: `a b c d E' denoting a 2-break operating on the \\vec{T}-consistent multicolor E,
### replacing the multiedges (a,b) and (c,d) with the multiedges (a,c) and (b,d).
### `oo' stands for a chromosome end.
### Manual completion can be derived from visual inspection of the breakpoint graph after MGRA Stage 3.
[Completion]""", file=out)
