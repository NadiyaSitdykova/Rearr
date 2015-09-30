#!/usr/bin/env pytnon
# vim: set fileencoding=utf-8 ts=4 sw=4 expandtab:
import pylab as pl
import numpy as np
from matplotlib import rc
import sys, os

rc('font',**{'family':'serif'})
rc('text', usetex=True)
rc('text.latex',unicode=True)
rc('text.latex',preamble='\usepackage[utf8]{inputenc}')
rc('text.latex',preamble='\usepackage[russian]{babel}')

PATH = sys.argv[1]
X_START = 400
X_END = 3000
X_MULT = 200
Y_START = 90
Y_END = 100
Y_MULT = 2

if __name__ == '__main__':
    xs_count = int((X_END - X_START) / X_MULT) + 1
    ys_count = int((Y_END - Y_START) / Y_MULT) + 1
    x = np.array([(i * X_MULT + X_START) for i in range(xs_count)])
    y = np.array([(i * Y_MULT + Y_START) for i in range(ys_count)])
    X, Y = np.meshgrid(x, y)

    for filename in os.listdir(PATH):
        if filename.endswith(".txt"):
            full_name = PATH + filename
            zs = []
            with open(full_name, 'r') as file:
                for line in file.readlines():
                    row = map(lambda x: float(x), line.split())
                    row.append(0.0)
                    zs.append(row)
            zs.append(row)
            Z = np.array(zs)

            pl.pcolor(X, Y, Z.T)
            pl.axis([x.min(), x.max(), y.min(), y.max()])
            pl.xlabel(u"Минимальная длина повтора")
            pl.ylabel(u"Минимальная идентичность повтора")
            pl.colorbar()
            pl.savefig(full_name[:-4] + "_2d.png")
            pl.clf()
