def parse(inputfile, interest, families):
    with open(inputfile, 'r') as file:
        i, organisms, genes, last, noDuplications  = 0, [], [], "", True
        for line in file:
            blocks = line.split()
            geneID = blocks[3].strip()
            organism = blocks[5].strip()
            if blocks[1].strip() == last:
                if organism in interest:
                    if organism in organisms:
                        noDuplications = False
                    else:
                        genes.append(geneID)
                        organisms.append(organism)
            else:
                if noDuplications and len(organisms) == 5:
                    i += 1
                    families[i] = genes
                noDuplications = True
                if organism in interest:
                    organisms = [organism]
                    genes = [geneID]
                else:
                    organisms = []
                    genes = []
            last = blocks[1].strip()
        if noDuplications and len(organisms) == 5:
            i += 1
            families[i] = genes