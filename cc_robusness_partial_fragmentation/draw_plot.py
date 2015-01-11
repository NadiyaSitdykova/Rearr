import matplotlib.pyplot as plt
import sys

inputfile = sys.argv[1]
step_size = int(sys.argv[2])
outputfile = sys.argv[3]
y = []
labels = []
with open(inputfile, 'r') as f:
    line1 = f.readline()
    while line1:
        labels.append(line1.strip())
	line2 = f.readline()
        y.append(list(map(lambda x: float(x), line2.split())))
        line1 = f.readline()

x = [i * step_size for i in range(0, len(y[0]))]

fig = plt.figure()
ax = plt.subplot(111)

for i in range(0, len(y)):
    ax.plot(x, y[i], label=labels[i])

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.xlabel("Number of breakage steps")
plt.ylabel("Number of connected components")
plt.savefig(outputfile + ".png")
plt.show()
