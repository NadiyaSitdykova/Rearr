def parse(inputfile, interest, families, gff):
    with open(inputfile, 'r') as file:
        dict = {}
        for i in range(0, len(interest)):
            dict[interest[i]] = i
        all = 0
        observed = 0
        most = 0
        least = 0
        is_obs = False
        i, organisms, genes, last, noDuplications  = 0, [], [], "", True
        for line in file:
            blocks = line.split()
            geneID = blocks[3].strip()
            organism = blocks[5].strip()
            if blocks[1].strip() == last:
                if organism in interest and geneID in gff[dict[organism]]:
                    is_obs = True
                    if organism in organisms:
                        noDuplications = False
                    else:
                        genes.append(geneID)
                        organisms.append(organism)
            else:
                all += 1
                if noDuplications and len(organisms) == 5:
                    i += 1
                    families[i] = genes
                if noDuplications:
                    most += 1
                if len(organisms) == 5:
                    least += 1
                noDuplications = True
                if is_obs:
                    observed += 1
                is_obs = False
                if organism in interest:
                    organisms = [organism]
                    genes = [geneID]
                    is_obs = True
                else:
                    organisms = []
                    genes = []
            last = blocks[1].strip()
        if noDuplications and len(organisms) == 5:
            i += 1
            families[i] = genes
        if noDuplications:
            most += 1
        if len(organisms) == 5:
            least += 1
        if is_obs:
            observed += 1
    with open("stat_of_genes_filtration.txt", 'w') as out:
        print("all ", all - 1, file=out)
        print("observed ", observed, file=out)
        print("at most once ", most - 1, file=out)
        print("at least once ", least, file=out)
        print("exactly once ", len(families), file=out)


