from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
import numpy as np
import sys, os

PATH = sys.argv[1]
X_START = 400
X_END = 3000
X_MULT = 200
Y_START = 90
Y_END = 100
Y_MULT = 2

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    xs_count = int((X_END - X_START) / X_MULT) + 1
    ys_count = int((Y_END - Y_START) / Y_MULT) + 1
    xs_list = []
    ys_list = []
    for i in range(0, xs_count):
        x_list = [(i * X_MULT + X_START) for _ in range(ys_count)]
        y_list = [(j * Y_MULT + Y_START) for j in range(ys_count)]
        xs_list.append(x_list)
        ys_list.append(y_list)
    xs = np.array(xs_list)
    ys = np.array(ys_list)
    fig = plt.figure()

    for filename in os.listdir(PATH):
        if filename.endswith(".txt"):
            ax = fig.add_subplot(111, projection='3d')
            full_name = PATH + filename
            zs = []
            with open(full_name, 'r') as file:
                for line in file.readlines():
                    zs.append(map(lambda x: float(x), line.split()))
            surf = ax.plot_surface(xs, ys, zs, rstride=1, cstride=1, cmap=cm.spectral,linewidth=0, antialiased=False)
            ax.zaxis.set_major_locator(LinearLocator(11))
            fig.colorbar(surf, shrink=0.8, aspect=10)
            ax.set_xlabel('Repeat min length')
            ax.set_ylabel('Repeat min identity')
            ax.set_zlabel(full_name.split("/")[-1][:-4])
            plt.savefig(full_name[:-4] + ".png")
            plt.clf()



