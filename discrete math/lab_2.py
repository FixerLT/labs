import random
import igraph
from igraph import *
print(igraph.__version__)
def print_graph(names, connections, folder = '/home/san/Documents/university/babakov/lab2/testing/', filename = 'test0'):
    g = Graph().as_directed()
    g.add_vertices(len(names))
    # g.vs['label'] = names
    for i in range(len(connections)):
        for j in range(len(connections[0])):
            if connections[i][j]:
                g.add_edges([(i, j)])
    arrow_size = [1 for e in g. get_edgelist()]
    print(arrow_size)
    plot(g, folder+filename+'.pdf', layout=g.layout('fr'), vertex_label=names, edge_arrow_size=arrow_size, arrow_size=arrow_size, edge_arrow_width=arrow_size)

print_graph(['a', 'b', 'c'], [[0, 1, 0], [1, 0, 0], [0, 0, 0]])


names = range(50)
connections = []
for i in range(50):
    connections.append([])
    for j in range(50):
        if random.random() > 0.95:
            connections[i].append(1)
        else:
            connections[i].append(0)
print_graph(names, connections)
