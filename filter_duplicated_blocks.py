#python3
import sys

inputfile = sys.argv[1]
dup = {}

with open(inputfile, 'r') as f:
    genomes = {}
    name = ""
    line = f.readline()
    while line:
        if line[0] == '>':
            name = line.strip()
            genomes[name] = {}
        else:
            chrome = [abs(int(i)) for i in line.split()[0:-1]]
            for block in chrome:
                if block in genomes[name]:
                     dup[block] = True
                else:
                    genomes[name][block] = True
        line = f.readline()

with open(inputfile, 'r') as f:
    outputfile = inputfile.split('.')[0] + "_filtered.txt"
    with open(outputfile, 'w') as out:
        line = f.readline()
        while line:
            if line[0] != '>':
                chrome = [int(i) for i in line.split()[0:-1]]
                new_chrome = []
                for block in chrome:
                    if abs(block) not in dup:
                        new_chrome.append(block)
                if len(new_chrome) != 0:
                    out.write(line)
                for block in new_chrome:
                    out.write(str(block) + " ")
                out.write("$\n" )
            else:
                out.write(line)
            line = f.readline()

