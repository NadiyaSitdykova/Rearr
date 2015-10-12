__author__ = 'nadya'


TARGET = ["chimp"]
HISTORY_PATH = "/home/nadya/Desktop/master/prepare_data/extended_vertebrate/history/"
LOG_PATH = "/home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-chimp/ragout/out/logs/"
OUT_PATH = "/home/nadya/Desktop/master/rearr/evaluation/90+/vertebrate/no_repeats/7-chimp/ragout/stats/"
XS = ["400", "600", "800", "1000", "1200", "1400", "1600", "1800", "2000", "2200", "2400", "2600", "2800", "3000"]
YS = ["90", "92", "94", "96", "98"]


def evaluation(length, identity):
    real_fragmentations = {}
    chromes = {}
    history = {}
    #process history files
    for genome in TARGET:
        with open(HISTORY_PATH + length + "_" + identity + "/" + genome + ".txt", 'r') as history_file:
            name = history_file.readline().strip()[1:]
            history[name] = {}
            real_fragmentations[name] = 0
            line = history_file.readline()
            while line:
                blocks = line.split()
                if len(blocks) == 1: #end of file
                    count_of_chromes = int(blocks[0])
                    chromes[name] = count_of_chromes
                else:
                    u = blocks[0]
                    v = blocks[2]
                    history[name][u] = v
                    real_fragmentations[name] += 1
                line = history_file.readline()

    #process assembly log
    with open(LOG_PATH + length + "_" + identity + "_ragout_log.txt", 'r') as log_file:
        correct_assembly_fragments = {}
        incorrect_assembly_fragments = {}
        for name in TARGET:
            correct_assembly_fragments[name] = 0
            incorrect_assembly_fragments[name] = 0
        for line in log_file.readlines():
            blocks = line.split()
            name = blocks[0]
            if int(blocks[1]) > 1:
                u = blocks[1]
                v = blocks[2]
                if name in history and (u in history[name] and history[name][u] == v or v in history[name] and history[name][v] == u):
                    correct_assembly_fragments[name] += 1
                else:
                    incorrect_assembly_fragments[name] += 1
    tpr, fdr, tnr = {}, {}, {}
    for key in real_fragmentations.keys():
        """if real_fragmentations[key] == 0:
            tpr[key] = 100
        else:
            tpr[key] = (correct_assembly_fragments[key] / real_fragmentations[key]) * 100
        if (correct_assembly_fragments[key] + incorrect_assembly_fragments[key]) == 0:
            fdr[key] = 0
        else:
            fdr[key] = (incorrect_assembly_fragments[key] / (correct_assembly_fragments[key] + incorrect_assembly_fragments[key])) * 100"""
        tpr[key] = (correct_assembly_fragments[key] / real_fragmentations[key]) * 100
        fdr[key] = (incorrect_assembly_fragments[key] / real_fragmentations[key]) * 100
        tn = chromes[key] * (chromes[key] - 1) - real_fragmentations[key]
        tnr[key] = tn / (tn + incorrect_assembly_fragments[key])
    return tpr, fdr, tnr

tpr_array, fdr_array, tnr_array = [], [], []
for length in XS:
    tpr_row = []
    fdr_row = []
    tnr_row = []
    for identity in YS:
        tpr, fdr, fnr = evaluation(length, identity)
        tpr_row.append(tpr)
        fdr_row.append(fdr)
        tnr_row.append(fnr)
    tpr_array.append(tpr_row)
    fdr_array.append(fdr_row)
    tnr_array.append(tnr_row)

for key in tpr_array[0][0].keys():
    with open(OUT_PATH + key.split("_")[0] + "_TPR.txt", 'w') as tpr_out:
        with open(OUT_PATH + key.split("_")[0] + "_FDR.txt", 'w') as fdr_out:
            with open(OUT_PATH + key.split("_")[0] + "_TNR.txt", 'w') as tnr_out:
                for i in range(0, len(XS)):
                    for j in range(0, len(YS)):
                        print("%0.7f" %(tpr_array[i][j][key]), end=" ", file=tpr_out)
                        print("%0.7f" %(fdr_array[i][j][key]), end=" ", file=fdr_out)
                        print("%0.7f" %(tnr_array[i][j][key]), end=" ", file=tnr_out)
                    print(file=tpr_out)
                    print(file=fdr_out)
                    print(file=tnr_out)
