def next_combination(cur_combination, n):
    k = len(cur_combination)
    for i in range(k - 1, -1, -1):
        if cur_combination[i] < n - k + i + 1:
            cur_combination[i] += 1
            for j in range(i + 1, k):
                cur_combination[j] = cur_combination[j - 1] + 1
            return True
    return False

def subset_by_combination(combination, set):
    subset = ""
    for i in range(0, len(combination)):
        subset += set[combination[i]]
    return subset

def get_list_of_subsets(k, dataset):
    n = len(dataset)
    cur_combination = [i for i in range(0, k)]
    res = [subset_by_combination(cur_combination, dataset)]
    while next_combination(cur_combination, n - 1):
        res.append(subset_by_combination(cur_combination, dataset))
    return res

def generate_blocks_for_subset(subset, inputfile, outputfile):
    with open(inputfile, 'r') as input:
        with open(outputfile, 'w') as out:
            line = input.readline()
            while line:
                if line[0] == '>':
                    cur_name = line[1:].strip()
                    if cur_name in subset:
                        print(line, file=out, end='')
                else:
                    if cur_name in subset:
                        print(line, file=out, end='')
                line = input.readline()

#NB this function generate config with some tree, which doesn't matter now, but could be later
def generate_cfg_for_subset(subset, outputfile):
    with open(outputfile, 'w') as out:
        print("[Genomes]", file=out)
        for i in range(0, len(subset)):
            print(subset[i], file=out)
        print("[Blocks]", file=out)
        print("format grimm", file=out)
        print("file tmp.txt", file=out)
        print("[Trees]", file=out)
        if len(subset) == 3:
            print("((" + subset[0] + "," + subset[1] + ")," + subset[2] + ")", file=out)
        elif len(subset) == 4:
            print("((" + subset[0] + "," + subset[1] + "),(" + subset[2] + "," + subset[3] + "))", file=out)
        elif len(subset) == 5:
            print("(((" + subset[0] + "," + subset[1] + ")," + subset[2] + "),(" + subset[3] + "," + subset[4] + "))", file=out)
        else:
            print("(((" + subset[0] + "," + subset[1] + ")," + subset[2] + "),(" + subset[3] + ",(" + subset[4] + "," + subset[5] + ")))", file=out)
        print("[Algorithm]", file=out)
        print("stages 0", file=out)




