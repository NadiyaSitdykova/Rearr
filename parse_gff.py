def median_parsegff(inputfile, d):
    with open(inputfile, 'r') as file:
        geneID, seqID, direction, coordinates = "trash", "", "", [0]
        for line in file:
            blocks = line.split()
            if blocks[10].strip() in d:
                coordinates.append((float(blocks[3]) + float(blocks[4]))/2)
            else:
                d[geneID] = (seqID, sum(coordinates)/len(coordinates), direction)
                geneID = blocks[10].strip()
                seqID = blocks[0].strip()
                coordinates = [(float(blocks[3]) + float(blocks[4]))/2]
                direction = blocks[6].strip()
        d[geneID] = (seqID, sum(coordinates)/len(coordinates), direction)


def process_gene(d, coordinates, seqID, geneID, direction):
    consequtive = True
    start = min(coordinates[0])
    end = max(coordinates[1])
    nonconsequtive = []
    for k, v in d.items():
        v_seqID, v_start, v_end, v_dir = v
        if seqID == v_seqID:
            if start > v_start and end < v_end:
                nonconsequtive.append(k)
            elif start > v_start and start < v_end or end > v_start and end < v_end:
                nonconsequtive.append(k)
                consequtive = False
    for k in nonconsequtive:
        d.pop(k, None)
    if consequtive:
        d[geneID] = (seqID, start, end, direction)

def consequtive_parsegff(inputfile, d):
    with open(inputfile, 'r') as file:
        geneID, seqID, direction, coordinates, last = "trash", "", "", [[0],[0]], ""
        for line in file:
            blocks = line.split()
            if blocks[10].strip() == last:
                coordinates[0].append(int(blocks[3]))
                coordinates[1].append(int(blocks[4]))
            else:
                process_gene(d, coordinates, seqID, geneID, direction)
                geneID = blocks[10].strip()
                seqID = blocks[0].strip()
                coordinates = [[int(blocks[3])], [int(blocks[4])]]
                direction = blocks[6].strip()
            last = blocks[10].strip()
        process_gene(d, coordinates, seqID, geneID, direction)
    for k, v in d.items():
        v_seqId, v_start, _, v_dir = v
        d[k] = (v_seqId, v_start, v_dir)
