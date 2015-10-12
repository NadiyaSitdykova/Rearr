class Node:
    def __init__(self, i, name):
        self.parent = i
        self.rank = 1
        self.index = i
        self.gene_names = [name]

def find(nodes, i):
    if nodes[i].parent != i:
        nodes[i].parent = find(nodes, nodes[i].parent)
    return nodes[i].parent

def join(nodes, i, j):
    x = nodes[find(nodes, i)]
    y = nodes[find(nodes, j)]
    if x.index != y.index:
        if x.rank == y.rank:
            x.rank += 1
        if x.rank < y.rank:
            x.parent = y.index
            y.gene_names += x.gene_names
        else:
            y.parent = x.index
            x.gene_names += y.gene_names
    nodes[x.index] = x
    nodes[y.index] = y
