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

def get_table(names1, names2, connections):
    tab = max([len(e) for e in names1]) + 3
    shift = 3
    starts = []
    ends = []
    sm = tab+shift
    for e in names2:
        starts.append(sm)
        sm += len(e)
        ends.append(sm)
        sm += shift
    positions = []
    for start, end in zip(starts, ends):
        positions.append(int((start + end)/2))
    sm -= shift
    result = ' ' * tab
    for e in names2:
        result += ' ' * shift
        result += e
    for e, i in zip(names1, range(len(names1))):
        result += '\n'
        result += e + ' ' * (tab - len(e))
        for e2, j in zip(names2, range(len(names2))):
            result += ' ' * shift
            pos = int((len(e2)+1) / 2)
            result += ' ' * (pos - 1)
            result += '1' if connections[i][j] else '0'
            result += ' ' * (len(e2) - pos) if pos!=0 else ''
    # for i in range(len(names1)):
    #     for j in range(len(names2)):
    #         result[(sm+1) * (j+1) + positions[i]] = '1' if connections[i][j] else '0'
    return result

n1 = ['asdf', 'aa', 'asdf3', 'a', '228']
n2 = ['123', '11', '1', '134134', '555', '12341234']
names1 = [str(e) for e in range(5)]
names2 = [str(e) for e in range(6)]
connections = []
for e in range(5):
    connections.append([])
    for k in range(6):
        connections[e].append((e+k)%3 == 1)
print(get_table(n1, n2, connections))
print(get_table(names1, names2, connections))
print('a' * 0)
print('hui')
