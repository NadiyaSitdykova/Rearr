from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
import numpy as np
import sys

if __name__ == '__main__':
    name = sys.argv[1]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x_start = 400
    x_end = 3000
    x_mult = 200
    xs_count =int((x_end - x_start) / x_mult) + 1
    ys_count = 12
    xs_list = []
    ys_list = []
    for i in range(0, xs_count):
        x_list = []
        y_list = [70, 74, 78, 82, 86, 88, 90, 92, 94, 96, 98, 100]
        for j in range(0, ys_count):
            x_list.append(i * x_mult + x_start)
        xs_list.append(x_list)
        ys_list.append(y_list)
    xs = np.array(xs_list)
    ys = np.array(ys_list)
    zs = []
    with open(name + ".txt", 'r') as file:
        for line in file.readlines():
            zs.append(map(lambda x: float(x), line.split()))
    surf = ax.plot_surface(xs, ys, zs, rstride=1, cstride=1, cmap=cm.spectral,linewidth=0, antialiased=False)
    ax.set_zlim(0, 100)
    ax.zaxis.set_major_locator(LinearLocator(11))
    fig.colorbar(surf, shrink=0.8, aspect=10)
    ax.set_xlabel('Repeat min length')
    ax.set_ylabel('Repeat min identity')
    ax.set_zlabel(name)
    plt.savefig(name + ".png")



