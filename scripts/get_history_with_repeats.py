PATH = "/home/nadya/Desktop/master/prepare_data/extended_vertebrate/"
NAMES = ["human", "chimp", "rat", "dog", "opossum", "cat", "mouse"]
X_START = 400
Y_START = 70
X_END = 3000
Y_END = 100
X_MULT = 100
Y_MULT = 2

def get_left(gene):
    if gene > 0:
        return str(gene) + "h"
    return str(-1 * gene) + "t"

def get_right(gene):
    if gene > 0:
        return str(gene) + "t"
    return str(-1 * gene) + "h"

def is_repeat(block):
    return (len(block) >= 8 and block[-8:] == "__repeat")

if __name__ == '__main__':
    xs_count = int((X_END - X_START) / X_MULT) + 1
    ys_count = int((Y_END - Y_START) / Y_MULT) + 1
    for genome in NAMES:
        for i in range(0, xs_count):
            for j in range(0, ys_count):
                with open(PATH + "grimm_with_repeat/" + str(X_START + i * X_MULT) + "_" + str(Y_START + j * Y_MULT) + "/" + genome + ".txt", 'r') as grimm:
                    with open(PATH + "history_with_repeat/" + str(X_START + i * X_MULT) + "_" + str(Y_START + j * Y_MULT) + "/" + genome + ".txt", 'w') as history_out:
                        history_out.write(">" + genome + "\n")
                        line = grimm.readline()
                        line = grimm.readline()
                        count_of_chromes = 0
                        left, right, repeat = "0", "0", "0"
                        while line:
                            count_of_chromes += 1
                            chrome = line.split()[:-1]
                            if len(chrome) > 1:
                                if is_repeat(chrome[0]):
                                    right =  get_right(int(chrome[1]))
                                    repeat = chrome[0]
                                else:
                                    right = "0"
                                if left != "0" and right != "0":
                                    repeat_id = int(repeat.split("__")[0])
                                    if repeat_id < 0:
                                        history_out.write(right + " ~ " + left + " " + str(abs(repeat_id)) + "\n")
                                    else:
                                        history_out.write(left + " ~ " + right + " " + str(repeat_id) + "\n")
                                if is_repeat(chrome[-1]):
                                    left = get_left(int(chrome[-2]))
                                else:
                                    left = "0"
                            line = grimm.readline()
                        history_out.write(str(count_of_chromes))