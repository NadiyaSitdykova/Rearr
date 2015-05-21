__author__ = 'nadya'
import os

#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_rodents_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/close_rodents_dataset/logs/"
#history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/close_primate_dataset/history/"
#log_path = "/home/nadya/Desktop/master/rearr/evaluation/close_primate_dataset/logs/"
history_path = "/home/nadya/Desktop/master/rearr/prepare_grimm_with_repeats/out/diverse_vertebrate_dataset/history/"
log_path = "/home/nadya/Desktop/master/rearr/evaluation/diverse_vertebrate_dataset/logs/"

def evaluation(length, identity):
    real_fragmentations = 0
    history = {}
    #process history files
    for history_filename in os.listdir(history_path + length + "_" + identity):
        with open(history_path + length + "_" + identity + "/" + history_filename, 'r') as history_file:
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
            u = blocks[1]
            v = blocks[2]
            if u in history[name] and history[name][u] == v or v in history[name] and history[name][v] == u:
                correct_assembly_fragments += 1
            else:
                incorrect_assembly_fragments += 1
    #print(real_fragmentations)
    #print(correct_assembly_fragments)
    #print(incorrect_assembly_fragments)
    if real_fragmentations == 0:
        tp = 100
        fp = 100
    else:
        tp = (correct_assembly_fragments / real_fragmentations) * 100
        fp = (incorrect_assembly_fragments / real_fragmentations) * 100
    if fp > 100:
        fp = 100
    fn = 100 - tp
    return tp, fp, fn

xs = ["400", "600", "800", "1000", "1200", "1400", "1600", "1800", "2000", "2200", "2400", "2600", "2800", "3000"]
ys = ["70", "74", "78", "82", "86", "88", "90", "92", "94", "96", "98", "100"]
TP, FP, FN = [], [], []
for length in xs:
    tp_row = []
    fp_row = []
    fn_row = []
    for identity in ys:
        tp, fp, fn = evaluation(length, identity)
        tp_row.append(tp)
        fp_row.append(fp)
        fn_row.append(fn)
    TP.append(tp_row)
    FP.append(fp_row)
    FN.append(fn_row)

with open("True_positive.txt", 'w') as tp_out:
    with open("False_posititve.txt", 'w') as fp_out:
        with open("False_negative.txt", 'w') as fn_out:
            for i in range(0, len(xs)):
                for j in range(0, len(ys)):
                    tp_out.write(str(TP[i][j]) + " ")
                    fp_out.write(str(FP[i][j]) + " ")
                    fn_out.write(str(FN[i][j]) + " ")
                tp_out.write("\n")
                fp_out.write("\n")
                fn_out.write("\n")
