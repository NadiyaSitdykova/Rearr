__author__ = 'nadya'

#FIRST THREE CASES HAVE LOGS WITHOUT ASSEMBLY SCORE!!

#targets = ["tree_shrew", "rat", "guinea_pig", "rabbit"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_rodents_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/close_rodents_dataset/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/close_rodents_dataset/stats/"
#targets = ["human", "gorilla", "chimp", "orangutan"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_primate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/close_primate_dataset/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/close_primate_dataset/stats/"
#targets = ["human", "chimp", "rat", "dog", "opossum"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/diverse_vertebrate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/diverse_vertebrate_dataset/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/diverse_vertebrate_dataset/stats/"

#targets = ["human"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_primate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/primate-human/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/primate-human/stats/"
#targets = ["human"]
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/diverse_vertebrate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/vertebrate-human/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/vertebrate-human/stats/"

#targets = ["human"]
#history_path = "/home/nadya/Desktop/master/prepare_data/extended_primate/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human/stats/"
#targets = ["human"]
#history_path = "/home/nadya/Desktop/master/prepare_data/extended_vertebrate/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_vertebrate-human/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_vertebrate-human/stats/"

targets = ["human", "chimp", "gorilla"]
history_path = "/home/nadya/Desktop/master/prepare_data/extended_primate/history/"
log_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human_chimp_gorilla/logs/"
out_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_primate-human_chimp_gorilla/stats/"
#targets = ["human", "chimp", "rat"]
#history_path = "/home/nadya/Desktop/master/prepare_data/extended_vertebrate/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_vertebrate-human_chimp_rat/logs/"
#out_path = "/home/nadya/Desktop/master/rearr/evaluation/ext_vertebrate-human_chimp_rat/stats/"


def evaluation(length, identity):
    real_fragmentations = {}
    real_fragmentations["all"] = 0
    real_fragmentations["all_filtered"] = 0
    chromes = {}
    chromes["all"] = 0
    chromes["all_filtered"] = 0
    history = {}
    #process history files
    #for history_filename in os.listdir(history_path + length + "_" + identity):
    for genome in targets:
        with open(history_path + length + "_" + identity + "/" + genome + ".txt", 'r') as history_file:
            name = history_file.readline().strip()[1:]
            history[name] = {}
            real_fragmentations[name] = 0
            real_fragmentations[name + "_filtered"] = 0
            line = history_file.readline()
            while line:
                blocks = line.split()
                if len(blocks) == 1: #end of file
                    count_of_chromes = int(blocks[0])
                    chromes["all"] += count_of_chromes
                    chromes["all_filtered"] += count_of_chromes
                    chromes[name] = count_of_chromes
                    chromes[name + "_filtered"] = count_of_chromes
                else:
                    u = blocks[0]
                    v = blocks[2]
                    history[name][u] = v
                    real_fragmentations["all"] += 1
                    real_fragmentations["all_filtered"] += 1
                    real_fragmentations[name] += 1
                    real_fragmentations[name + "_filtered"] += 1
                line = history_file.readline()

    #process assembly log
    with open(log_path + length + "_" + identity + "_assembly_log.txt", 'r') as log_file:
        correct_assembly_fragments = {}
        incorrect_assembly_fragments = {}
        correct_assembly_fragments["all"] = 0
        correct_assembly_fragments["all_filtered"] = 0
        incorrect_assembly_fragments["all"] = 0
        incorrect_assembly_fragments["all_filtered"] = 0
        for name in targets:
            correct_assembly_fragments[name] = 0
            correct_assembly_fragments[name + "_filtered"] = 0
            incorrect_assembly_fragments[name] = 0
            incorrect_assembly_fragments[name + "_filtered"] = 0
        for line in log_file.readlines():
            blocks = line.split()
            name = blocks[0]
            #if int(blocks[1]) > 1:
            if True:
                #score = 2
                #u = blocks[1]
                #v = blocks[2]
                score = int(blocks[1])
                u = blocks[2]
                v = blocks[3]
                if name in history and (u in history[name] and history[name][u] == v or v in history[name] and history[name][v] == u):
                    correct_assembly_fragments["all"] += 1
                    correct_assembly_fragments[name] += 1
                    if score > 1:
                        correct_assembly_fragments["all_filtered"] += 1
                        correct_assembly_fragments[name + "_filtered"] += 1
                else:
                    incorrect_assembly_fragments["all"] += 1
                    incorrect_assembly_fragments[name] += 1
                    if score > 1:
                        incorrect_assembly_fragments["all_filtered"] += 1
                        incorrect_assembly_fragments[name + "_filtered"] += 1
    tpr, fdr, tnr = {}, {}, {}
    for key in real_fragmentations.keys():
        if real_fragmentations[key] == 0:
            tpr[key] = 100
        else:
            tpr[key] = (correct_assembly_fragments[key] / real_fragmentations[key]) * 100
        if (correct_assembly_fragments[key] + incorrect_assembly_fragments[key]) == 0:
            fdr[key] = -1
        else:
            fdr[key] = (incorrect_assembly_fragments[key] / (correct_assembly_fragments[key] + incorrect_assembly_fragments[key])) * 100
        tn = chromes[key] * (chromes[key] - 1) - real_fragmentations[key]
        tnr[key] = tn / (tn + incorrect_assembly_fragments[key])
    return tpr, fdr, tnr

xs = ["400", "600", "800", "1000", "1200", "1400", "1600", "1800", "2000", "2200", "2400", "2600", "2800", "3000"]
ys = ["70", "74", "78", "82", "86", "88", "90", "92", "94", "96", "98", "100"]
TPR, FDR, TNR = [], [], []
for length in xs:
    tpr_row = []
    fdr_row = []
    tnr_row = []
    for identity in ys:
        tpr, fdr, fnr = evaluation(length, identity)
        tpr_row.append(tpr)
        fdr_row.append(fdr)
        tnr_row.append(fnr)
    TPR.append(tpr_row)
    FDR.append(fdr_row)
    TNR.append(tnr_row)

for key in TPR[0][0].keys():
    """print(key)
    print(len(key))
    if len(key) > 9:
        print(key[])"""
    if len(key) > 9 and key[-9:] == "_filtered":
        path = out_path + "filtered/"
    else:
        path = out_path
    with open(path + key.split("_")[0] + "_TPR.txt", 'w') as tpr_out:
        with open(path + key.split("_")[0] + "_FDR.txt", 'w') as fdr_out:
            with open(path + key.split("_")[0] + "_TNR.txt", 'w') as tnr_out:
                for i in range(0, len(xs)):
                    for j in range(0, len(ys)):
                        tpr_out.write(str(TPR[i][j][key]) + " ")
                        fdr_out.write(str(FDR[i][j][key]) + " ")
                        tnr_out.write(str(TNR[i][j][key]) + " ")
                    tpr_out.write("\n")
                    fdr_out.write("\n")
                    tnr_out.write("\n")

