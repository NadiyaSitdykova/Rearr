from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

def draw_count(xs, ys, zs, name):
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(xs, ys, zs)
    ax.set_xlabel('Repeat min length')
    ax.set_ylabel('Repeat min identity')
    ax.set_zlabel('Count of fragments')
    plt.savefig("count/" + name + ".png")
    plt.clf()

def draw_average_length(xs, ys, zs, name):
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(xs, ys, zs)
    ax.set_xlabel('Repeat min length')
    ax.set_ylabel('Repeat min identity')
    ax.set_zlabel('Avg length of fragments')
    plt.savefig("avg/" + name + ".png")
    plt.clf()

if __name__ == '__main__':
    x_start = 400
    x_end = 3000
    y_start = 70
    y_end = 100
    x_mult = 100
    y_mult = 1
    xs_count =int((x_end - x_start) / x_mult) + 1
    ys_count = int((y_end - y_start) / y_mult) + 1

    #generate grid of xs and ys
    xs_list = []
    ys_list = []
    for i in range(0, xs_count):
        x_list = []
        y_list = []
        for j in range(0, ys_count):
            x_list.append(i * x_mult + x_start)
            y_list.append(j * y_mult + y_start)
        xs_list.append(x_list)
        ys_list.append(y_list)
    xs = np.array(xs_list)
    ys = np.array(ys_list)
    fig = plt.figure()

    with open("stats.out", 'r') as file:
        i = -1
        count_zs, avg_len_zs = [], []
        is_count = False
        for line in file.readlines():
            if line[0] == ">":
                if len(count_zs) > 0:
                    draw_count(xs, ys, count_zs, name)
                    draw_average_length(xs, ys, avg_len_zs, name)
                    count_zs, avg_len_zs = [], []
                name = line.strip()[1:]
            elif line.split()[0] == "Count:":
                is_count = True
            elif line.split()[0] == "Average":
                is_count = False
            elif is_count:
                count_zs.append(map(lambda x: int(x), line.split()))
            else:
                avg_len_zs.append(map(lambda x: float(x), line.split()))
        draw_count(xs, ys, count_zs, name)
        draw_average_length(xs, ys, avg_len_zs, name)
