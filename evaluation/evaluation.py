__author__ = 'nadya'

#FIRST THREE CASES HAVE LOGS WITHOUT ASSEMBLY SCORE!!

#targets = ["tree_shrew", "rat", "guinea_pig", "rabbit"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_rodents_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/close_rodents_dataset/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/close_rodents_dataset/"
#targets = ["human", "gorilla", "chimp", "orangutan"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_primate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/close_primate_dataset/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/close_primate_dataset/"
#targets = ["human", "chimp", "rat", "dog", "opossum"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/diverse_vertebrate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/diverse_vertebrate_dataset/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/diverse_vertebrate_dataset/"

#targets = ["human"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_primate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/primate-human/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/primate-human/"
#targets = ["human"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/diverse_vertebrate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/vertebrate-human/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/vertebrate-human/"

#targets = ["human"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/extended_primate/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human/"

targets = ["human", "chimp", "gorilla"]
history_path = "/home/nadya/Desktop/master/prepare_data/extended_primate/history/"
log_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human_chimp_gorilla/logs/"
out_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human_chimp_gorilla/"

def evaluation(length, identity):
    real_fragmentations = 0
    history = {}
    #process history files
    #for history_filename in os.listdir(history_path + length + "_" + identity):
    for genome in targets:
        with open(history_path + length + "_" + identity + "/" + genome + ".txt", 'r') as history_file:
            name = history_file.readline().strip()[1:]
            history[name] = {}
            line = history_file.readline()
            while line:
                blocks = line.split()
                u = blocks[0]
                v = blocks[2]
                history[name][u] = v
                real_fragmentations += 1
                line = history_file.readline()
    #process assembly log
    with open(log_path + length + "_" + identity + "_assembly_log.txt", 'r') as log_file:
        correct_assembly_fragments = 0
        incorrect_assembly_fragments = 0
        for line in log_file.readlines():
            blocks = line.split()
            name = blocks[0]
            #if int(blocks[1]) > 1:
            if True:
                #u = blocks[1]
                #v = blocks[2]
                u = blocks[2]
                v = blocks[3]
                if name in history and (u in history[name] and history[name][u] == v or v in history[name] and history[name][v] == u):
                    correct_assembly_fragments += 1
                else:
                    incorrect_assembly_fragments += 1
    #print(real_fragmentations)
    #print(correct_assembly_fragments)
    #print(incorrect_assembly_fragments)
    if real_fragmentations == 0:
        tpr = 100
    else:
        tpr = (correct_assembly_fragments / real_fragmentations) * 100
    fdr = (incorrect_assembly_fragments / (correct_assembly_fragments + incorrect_assembly_fragments)) * 100
    fnr = 100 - tpr
    return tpr, fdr, fnr

xs = ["400", "600", "800", "1000", "1200", "1400", "1600", "1800", "2000", "2200", "2400", "2600", "2800", "3000"]
ys = ["70", "74", "78", "82", "86", "88", "90", "92", "94", "96", "98", "100"]
TPR, FDR, FNR = [], [], []
for length in xs:
    tpr_row = []
    fdr_row = []
    fnr_row = []
    for identity in ys:
        tpr, fdr, fnr = evaluation(length, identity)
        tpr_row.append(tpr)
        fdr_row.append(fdr)
        fnr_row.append(fnr)
    TPR.append(tpr_row)
    FDR.append(fdr_row)
    FNR.append(fnr_row)

with open(out_path + "True_positive_rate.txt", 'w') as tpr_out:
    with open(out_path + "False_discovery_rate.txt", 'w') as fdr_out:
        with open(out_path + "False_negative_rate.txt", 'w') as fnr_out:
            for i in range(0, len(xs)):
                for j in range(0, len(ys)):
                    tpr_out.write(str(TPR[i][j]) + " ")
                    fdr_out.write(str(FDR[i][j]) + " ")
                    fnr_out.write(str(FNR[i][j]) + " ")
                tpr_out.write("\n")
                fdr_out.write("\n")
                fnr_out.write("\n")

