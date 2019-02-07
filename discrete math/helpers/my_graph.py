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
    visual_style["vertex_size"] = 40#20
    visual_style["vertex_color"] = ['gray' for i in range(vertexes_sz)]
    visual_style["vertex_label"] = g.vs["name"]
    visual_style["vertex_label_size"] = 28
    visual_style["vertex_name"] = g.vs["name"]
    visual_style["edge_width"] = [1 + 0.2 * abs(w) for w in g.es['weight']]
    visual_style["layout"] = g.layout('circle')
    visual_style["edge_label_size"] = 20
    visual_style["edge_label_dist"] = 0
    visual_style["bbox"] = (1200, 1200)
    visual_style['arrow_size'] = [0.5 for _ in range(edges_sz + stash_sz)]
    visual_style['edge_color'] = ['black' if i in range(edges_sz) else 'red' for i in range(edges_sz + stash_sz)]
    for i, e in enumerate(g.es['weight']):
        if e < 0:
            visual_style['edge_color'][i] = 'blue'
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
        neighbours = []
        for i in range(len(self.nodes)):
            neighbours.append([])
            neighbours[-1] = [j for j in range(len(self.nodes)) if
                              self.nodes[i][j] is not None or self.nodes[j][i] is not None]
        return neighbours

    def get_node_degrees(self, orientated=True):
        degrees = []
        for i in range(len(self.nodes)):
            degrees.append([])
            degrees[-1] = sum([len(e if e is not None else []) for e in self.edges[i]])
            if orientated:
                degrees[-1] += sum([len(self.edges[j][i] if self.edges[j][i] is not None else []) for j in range(len(self.nodes))])
            else:
                if self.edges[i][i] is not None:
                    degrees[-1] += len(self.edges[i][i])
        return degrees

    def cnt_incoming_edges(self, node):
        return sum([len(self.edges[j][node]) for j in range(len(self.nodes)) if self.edges[j][node] is not None])

    def cnt_outcoming_edges(self, node):
        return sum([len(self.edges[node][j]) for j in range(len(self.nodes)) if self.edges[node][j] is not None])

    def count_nodes_outcoming_edges(self):
        return [sum([len(e) for e in self.edges[i] if e is not None]) for i in range(len(self.nodes))]

    def get_node_min_distances_to_neighbours(self, node):
        distances = {}
        for i in range(len(self.nodes)):
            if self.edges[node][i] is not None and len(self.edges[node][i]) > 0:
                distances[i] = min(self.edges[node][i])
        return distances

    def get_neighbours(self, node):
        neighbours = set()
        for i in range(len(self.nodes)):
            if (self.edges[node][i] is not None and len(self.edges[node][i]) > 0) or \
                    (self.edges_stash is not None and self.edges_stash[node][i] is not None and len(self.edges_stash[node][i]) > 0):
                neighbours.add(i)
        return neighbours

    def get_neighbours_can_go(self, node):
        return {i for i in range(len(self.nodes)) if self.edges[node][i] is not None and len(self.edges[node][i]) > 0}

    def is_bridge(self, node1, node2, orientated=False):
        if sum([1 for e in self.edges[node1] if e is None or len(e) == 0]) >= len(self.nodes)-1:
            return False
        to_visit = [node2]
        visited = set(to_visit)
        while len(to_visit) > 0:
            node = to_visit.pop()
            for neighbour in self.get_neighbours(node):
                if orientated or not(node == node2 and neighbour == node1):
                    if neighbour == node1:
                        return False
                    if neighbour not in visited:
                        to_visit.append(neighbour)
                        visited.add(neighbour)
        return True

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

    def unorientate(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if i == j:
                    continue
                if self.edges[i][j] is not None and self.edges[j][i] is not None:
                    sum_arr = self.edges[i][j] + self.edges[j][i]
                    self.edges[i][j] = sum_arr.copy()
                    self.edges[j][i] = sum_arr.copy()
                    # self.edges[i][j], self.edges[j][i] = self.edges[i][j] + self.edges[j][i], self.edges[i][j] + self.edges[j][i]
                elif self.edges[j][i] is not None:
                    self.edges[i][j] = self.edges[j][i].copy()
                elif self.edges[i][j] is not None:
                    self.edges[j][i] = self.edges[i][j].copy()

    def apply_fn_to_edges(self, fn_connections):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.edges[i][j] is not None:
                    self.edges[i][j] = fn_connections(self.edges[i][j])

    def remove_nodes(self, nodes):  # not appliable to stash
        new_indexes = {}
        for i in range(len(self.nodes)):
            if i not in nodes:
                new_indexes[i] = len(new_indexes)
        new_edges_list = []
        for edge in self.edges_list:
            if not (edge[0] in nodes or edge[1] in nodes):
                new_edges_list.append((new_indexes[edge[0]], new_indexes[edge[1]], edge[2]))
        self.nodes = [e for i, e in enumerate(self.nodes) if i not in nodes]
        self.edges_list = new_edges_list
        self.edges = edges_list_to_table(self.edges_list, len(self.nodes))


    def save_plot(self, folder, filename, override_visual_style=None):
        g = Graph().as_directed()
        g.add_vertices(len(self.nodes))
        weights = []
        for i in range(len(self.edges)):
            for j in range(len(self.edges[i])):
                if self.edges[i][j] is not None:
                    for e in self.edges[i][j]:
                        g.add_edges([(i, j)])
                        weights.append(e)
        edges_sz = len(weights)
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
        visial_style = best_visual_style(g, edges_sz, len(weights) - edges_sz, len(self.nodes))
        if override_visual_style is not None:
            for k, v in override_visual_style.items():
                visial_style[k] = v
        plot(g, folder+filename+'.png', **visial_style)

    def get_shortest_path_by_edges_amount(self, start, end):
        to_visit = [start]
        visited = set()
        parents = {start: None}
        while len(to_visit) > 0:
            node = to_visit[0]
            to_visit.pop(0)
            visited.add(node)
            for neighbour in self.get_neighbours(node):
                if neighbour == end:
                    path = [end, node]
                    while parents[node] is not None:
                        node = parents[node]
                        path.append(node)
                    path = list(reversed(path))
                    smallest = sum(self.edges[path[0]][path[1]])
                    for i in range(1, len(path)-1):
                        smallest = min(smallest, sum(self.edges[path[i]][path[i+1]]))
                    return path, smallest
                if neighbour not in visited and neighbour not in to_visit:
                    to_visit.append(neighbour)
                    parents[neighbour] = node
        return None, None

    def reduce_edges(self, path, val):
        for i in range(len(path) - 1):
            edge_from = path[i]
            edge_to = path[i+1]
            val_cp = val
            while val_cp > 0:
                if self.edges[edge_from][edge_to][-1] > val_cp:
                    self.edges[edge_from][edge_to][-1] -= val_cp
                    val_cp = 0
                else:
                    val_cp -= self.edges[edge_from][edge_to][-1]
                    self.edges[edge_from][edge_to].pop(-1)
            if len(self.edges[edge_from][edge_to]) == 0:
                self.edges[edge_from][edge_to] = None

    def __init__(self, nodes, edges=None, edges_list=None):
        self.nodes = nodes
        if edges is not None:
            self.edges = []
            for e in edges:
                self.edges.append(e.copy())
            self.edges_list = table_to_edges_list(edges)
        else:
            self.edges = edges_list_to_table(edges_list, len(nodes))
            self.edges_list = edges_list.copy()

