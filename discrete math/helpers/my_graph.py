class Graph:
    nodes = []
    edges = None  # edges[i][j] is an array of distances from node i to node j
    edges_list = None  # for each edge in graph there is a tuple: (i, j, dist)

    def get_weightet_shortest_list(self):
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

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

