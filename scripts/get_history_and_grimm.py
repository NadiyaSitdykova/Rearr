PATH = "/home/nadya/Desktop/master/prepare_data/extended_primate/"
NAMES = ["human", "chimp", "gorilla", "orangutan", "macaque", "marmoset"]
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
    count = {}
    lens = {}

    #process grimm_with_repeats to generate grimm and history without repeats
    for genome in NAMES:
        lens[genome] = [[0 for _ in range(0, ys_count)] for _ in range(0, xs_count)]
        count[genome] = [[0 for _ in range(0, ys_count)] for _ in range(0, xs_count)]
        for i in range(0, xs_count):
            print(genome, i)
            for j in range(0, ys_count):
                with open(PATH + "grimm_with_repeats/" + str(X_START + i * X_MULT) + "_" + str(Y_START + j * Y_MULT) + "/" + genome + ".txt", 'r') as grimm:
                    with open(PATH + "history/" + str(X_START + i * X_MULT) + "_" + str(Y_START + j * Y_MULT) + "/" + genome + ".txt", 'w') as history_out:
                        with open(path + "grimm/" + str(x_start + i * x_mult) + "_" + str(y_start + j * y_mult) + "/" + genome + ".txt", 'w') as grimm_out:
                            history_out.write(">" + genome + "\n")
                            grimm_out.write(">" + genome + "\n")
                            line = grimm.readline()
                            line = grimm.readline()
                            count_of_chromes = 0
                            left, right = "0", "0"
                            while line:
                                count_of_chromes += 1
                                chrome = line.split()[:-1]
                                if len(chrome) > 1:
                                    s = ""
                                    count[genome][i][j] += 1
                                    for block in chrome:
                                        if not is_repeat(block):
                                            lens[genome][i][j] += 1
                                            s += block + " "
                                    grimm_out.write(s + "$\n")
                                    if is_repeat(chrome[0]):
                                        right = get_right(int(chrome[1]))
                                    else:
                                        right = "0"
                                    if left != "0" and right != "0":
                                        history_out.write(left + " ~ " + right + "\n")
                                    if is_repeat(chrome[-1]):
                                        left = get_left(int(chrome[-2]))
                                    else:
                                        left = "0"
                                line = grimm.readline()
                            history_out.write(str(count_of_chromes))

    #print stats: count of chromes/avg len after fragmentation by repeats
    with open(PATH + "stats.out", 'w') as stats_out:
        for name in NAMES:
            stats_out.write(">" + name + "\n")
            stats_out.write("Count:\n")
            for i in range(0, xs_count):
                for j in range(0, ys_count):
                    stats_out.write(str(count[name][i][j]) + " ")
                stats_out.write("\n")

            stats_out.write("Average length:\n")
            for i in range(0, len(count[name])):
                for j in range(0, len(count[name][i])):
                    average = float(lens[name][i][j]) /count[name][i][j]
                    stats_out.write(str(average) + " ")
                stats_out.write("\n")