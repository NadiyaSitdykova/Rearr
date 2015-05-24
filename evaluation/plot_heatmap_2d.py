import pylab as pl
import numpy as np
import sys

x = np.array([200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000])
y = np.array([68, 70, 74, 78, 82, 86, 88, 90, 92, 94, 96, 98, 100])
X, Y = np.meshgrid(x, y)

zs = []
full_name = sys.argv[1]
with open(full_name, 'r') as file:
    for line in file.readlines():
        row = map(lambda x: float(x), line.split())
        row.append(0.0)
        zs.append(row)
zs.append(row)
Z = np.array(zs)

pl.pcolor(X, Y, Z.T)
pl.axis([x.min(), x.max(), y.min(), y.max()])
pl.title(full_name.split("/")[-1][:-4])
pl.xlabel("Repeat min length(bp)")
pl.ylabel("Repeat min identity(%)")
pl.colorbar()
pl.savefig(full_name[:-4] + "_2d.png")
#pl.show()

