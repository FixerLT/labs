from igraph import *

def add_edges_to_table(table, edges_list):
    for e in edges_list:
        if len(table) <= e[0] or len(table) <= e[1]:
            raise Exception('wrong list indexing')
        if table[e[0]][e[1]] is not None:
            table[e[0]][e[1]].append(e[2])
        else:
            table[e[0]][e[1]] = [e[2]]


def edges_list_to_table(edges_list, size):
    table = []
    for i in range(size):
        table.append([])
        for j in range(size):
            table[-1].append(None)
    add_edges_to_table(table, edges_list)
    return table


def table_to_edges_list(table):
    edges = []
    for i in range(len(table)):
        for j in range(len(table)):
            if table[i][j] is not None:
                for e in table[i][j]:
                    edges.append((i, j, e))
    return edges


def best_visual_style(g, edges_sz, stash_sz, vertexes_sz):
    visual_style = {}
    visual_style["vertex_size"] = 20
    visual_style["vertex_color"] = ['pink' for gender in range(vertexes_sz)]
    visual_style["vertex_label"] = g.vs["name"]
    visual_style["vertex_name"] = g.vs["name"]
    visual_style["edge_width"] = [0.1 * w for w in g.es['weight']]
    visual_style["layout"] = g.layout('large')
    visual_style["bbox"] = (1200, 1200)
    # shortest_length =
    visual_style['arrow_size'] = [0.5 for w in g.es['weight']]
    visual_style['edge_color'] = ['black' if i in range(edges_sz) else 'red' for i in range(edges_sz + stash_sz)]
    return visual_style


class LabGraph:
    nodes = []
    edges = None  # edges[i][j] is an array of distances from node i to node j
    edges_list = None  # for each edge in graph there is a tuple: (i, j, dist)
    edges_stash = None
    edges_stash_list = None

    def get_weighted_shortest_list(self):
        return [[min(e) if e is not None else None for e in arr] for arr in self.edges]

    def get_not_weighted_list(self):
        return [[1 if e is not None else None for e in arr] for arr in self.edges]

    def cnt_nodes(self):
        return len(self.nodes)

    def cnt_edges(self):
        cnt = 0
        for arr in self.edges:
            cnt += sum([len(e) if e is not None else 0 for e in arr])
        return cnt

    def max_neighbours_nodes(self):
        neighbours = {}
        for i in range(len(self.nodes)):
            neighbours[self.nodes[i]] = [self.nodes[j] for j in range(len(self.nodes)) if
                                         self.nodes[i][j] is not None and self.nodes[i][j]]
        return neighbours

    def add_to_stash(self, e_stash=None, e_stash_list=None, size=None):
        if e_stash is not None:
            if self.edges_stash is None:
                self.edges_stash = e_stash
                self.edges_stash_list = table_to_edges_list(e_stash)
            else:
                e_stash_list = table_to_edges_list(e_stash)
                add_edges_to_table(self.edges_stash, e_stash_list)
                self.edges_stash_list.extend(e_stash_list)
        else:
            if self.edges_stash is None:
                if size is None:
                    size = len(self.edges)
                self.edges_stash = edges_list_to_table(e_stash_list, size)
                self.edges_stash_list = e_stash_list
            else:
                add_edges_to_table(self.edges_stash, e_stash_list)
                self.edges_stash_list.extend(e_stash_list)

    def apply_stash(self):
        add_edges_to_table(self.edges, self.edges_stash_list)
        self.edges_list.extend(self.edges_stash_list)
        self.edges_stash = None
        self.edges_stash_list = None

    def save_plot(self, folder, filename):
        g = Graph().as_directed()
        g.add_vertices(len(self.nodes))
        weights = []
        for i in range(len(self.edges)):
            for j in range(len(self.edges[i])):
                if self.edges[i][j] is not None:
                    for e in self.edges[i][j]:
                        g.add_edges([(i, j)])
                        weights.append(e)
        if self.edges_stash is not None:
            for i in range(len(self.edges_stash)):
                for j in range(len(self.edges_stash[i])):
                    if self.edges_stash[i][j] is not None:
                        for e in self.edges_stash[i][j]:
                            g.add_edges([(i, j)])
                            weights.append(e)
        g.es['weight'] = weights
        g.vs['name'] = [str(e) for e in range(len(self.nodes))]
        # g.es['name'] = [str(e) for e in weights]
        # g.es['label'] = [str(e) for e in weights]
        visial_style = best_visual_style(g, len(self.edges), 0 if self.edges_stash is None else len(self.edges_stash), len(self.nodes))
        plot(g, folder+filename+'.png', **visial_style)

    def __init__(self, nodes, edges=None, edges_list=None, size=None):
        self.nodes = nodes
        if edges is not None:
            self.edges = []
            for e in edges:
                self.edges.append(e.copy())
            self.edges_list = table_to_edges_list(edges)
        else:
            self.edges = edges_list_to_table(edges_list, size)
            self.edges_list = edges_list.copy()

