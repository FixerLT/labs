from generate_lab58_graph import get_graph_for_topic_1
from my_graph import LabGraph
from data_structures import DisjointSetUnion
from lab_8 import limit_nodes_by_degrees, save_graph_for_path
import os


def prima_solve(graph, log_folder=None):
    graph.unorientate()
    graph.apply_fn_to_edges(fn_connections=lambda e: [min(e)] if e is not None else None)
    prima_g = LabGraph(graph.nodes, edges_list=[])
    distances = {}  # key is target node, value is tuple(distance, src node)
    prima_g_connected = [0]
    while len(prima_g_connected) < len(graph.nodes):
        node = prima_g_connected[-1]
        node_min_distances = graph.get_node_min_distances_to_neighbours(node)
        for k, v in node_min_distances.items():
            if k not in prima_g_connected and (k not in distances or v < distances[k][0]):
                distances[k] = (v, node)
        if len(distances) == 0:
            return
        new_node, (dist, parent) = min(distances.items(), key=lambda e: e[1][0])
        distances.pop(new_node)
        prima_g.add_to_stash(e_stash_list=[(parent, new_node, dist)])
        prima_g.apply_stash()
        prima_g_connected.append(new_node)
        if log_folder is not None:
            prima_g.save_plot(log_folder, str(len(prima_g_connected) - 2) + '_tree_step')


def kruskal_solve(graph, log_folder=None):
    graph.unorientate()
    graph.apply_fn_to_edges(fn_connections=lambda e: [min(e)] if e is not None else None)
    kruskal_g = LabGraph(graph.nodes, edges_list=[])
    edges = sorted(graph.edges_list, key=lambda e: e[2])
    dsu = DisjointSetUnion()
    for i in range(len(graph.nodes)):
        dsu.make_set(i)
    for edge in edges:
        if dsu.find_set(edge[0]) != dsu.find_set(edge[1]):
            kruskal_g.add_to_stash(e_stash_list=[edge])
            kruskal_g.apply_stash()
            if log_folder is not None:
                kruskal_g.save_plot(log_folder, str(len(graph.nodes) - dsu.num_sets) + '_tree_step')
            dsu.union_sets(edge[0], edge[1])
            if dsu.num_sets == 1:
                break


def euler_path(graph, log_folder=None, orientated=False):
    if not orientated:
        graph.unorientate()
    graph.apply_fn_to_edges(fn_connections=lambda e: [1] if e is not None else None)
    degrees = graph.get_node_degrees(orientated=orientated)
    odds = [i for i, e in enumerate(degrees) if e % 2 == 1]
    g_type = 'non_euler'
    if len(odds) == 0:
        g_type = 'euler'
    elif len(odds) == 2:
        g_type = 'semi-euler'
    while len(odds) > 0:
        node1 = odds.pop()
        node2 = odds.pop()
        if graph.edges[node1][node2] is not None and len(graph.edges[node1][node2]) > 0:
            graph.add_to_stash(e_stash_list=[(node1, node2, 1)])
            graph.apply_stash()
        else:
            graph.edges[node1][node2].pop()
            if len(graph.edges[node1][node2]) == 0:
                graph.edges[node1][node2] = None
    path = [0]
    neighbour_sets = [graph.get_neighbours(i) for i in range(len(graph.nodes))]
    while sum([len(e) for e in neighbour_sets]) > 0:
        found = False
        node = path[-1]
        if node in neighbour_sets[node]:
            path.append(node)
            neighbour_sets[node].remove(node)
            graph.edges[node][node] = None
            found = True
        else:
            for e in neighbour_sets[node]:
                if not graph.is_bridge(node, e, orientated=orientated):
                    path.append(e)
                    neighbour_sets[node].remove(e)
                    graph.edges[node][e] = None
                    if not orientated:
                        graph.edges[e][node] = None
                        neighbour_sets[e].remove(node)
                    found = True
                    break
        if not found:
            print('errored')
            return g_type, None
    return g_type, path


def get_next_hamilton_node(graph, visited, start):
    for j in range(start, len(graph.nodes)):
        if graph.edges[visited[-1]][j] is not None and len(graph.edges[visited[-1]][j]) > 0 and j not in visited:
            return j, j+1
    return None, None


def hamilton_solve(graph, log_folder=None):
    ham_path = None
    ham_loop = None
    for e in range(len(graph.nodes)):
        visited = [e]
        starts = [0]
        iteration_counter = 0
        while len(visited) > 0:
            if len(visited) == len(graph.nodes):
                if graph.edges[visited[-1]][visited[0]] is not None and len(graph.edges[visited[-1]][visited[0]]) > 0:
                    next_node, next_start = visited[0], 0
                else:
                    next_node, next_start = None, None
            else:
                next_node, next_start = get_next_hamilton_node(graph, visited, starts[-1])
            if next_node is None:
                visited.pop()
                starts.pop()
            else:
                visited.append(next_node)
                starts[-1] = next_start
                starts.append(0)
                save_graph_for_path(visited, log_folder, iteration_counter, len(graph.nodes), pref='node_' + str(e) + '_')
                if len(visited) == len(graph.nodes):
                    ham_path = visited.copy()
                if len(visited) > len(graph.nodes):
                    ham_loop = visited.copy()
                    break
            iteration_counter += 1
        if ham_loop is not None:
            break
    if ham_loop is not None:
        return 'hamilton', ham_loop
    if ham_path is not None:
        return 'semi-hamilton', ham_path
    return 'non-hamilton', None


def solve(log_folder):
    graph = get_graph_for_topic_1()
    sub_folders = ['prima/', 'kruskal/', 'euler_not_orientated/', 'euler_orientated/', 'hamilton/']
    for e in sub_folders:
        if not os.path.exists(log_folder + e):
            os.mkdir(log_folder + e)
    prima_solve(graph, log_folder=log_folder + sub_folders[0])
    kruskal_solve(graph, log_folder=log_folder + sub_folders[1])
    graph = get_graph_for_topic_1()
    g_type, path = euler_path(graph, log_folder=log_folder + sub_folders[2], orientated=False)
    with open(log_folder + sub_folders[2] + 'euler_non_orientated_report.txt', 'w+') as f:
        f.write('the type of non orientated graph is ' + g_type + '\n')
        if path is not None:
            f.write('euler path is: ' + str(path) + '\n')
    graph = get_graph_for_topic_1()
    g_type, path = euler_path(graph, log_folder=log_folder + sub_folders[3], orientated=True)
    with open(log_folder + sub_folders[3] + 'euler_orientated_report.txt', 'w+') as f:
        f.write('the type of orientated graph is ' + g_type + '\n')
        if path is not None:
            f.write('euler path is: ' + str(path) + '\n')
    graph = get_graph_for_topic_1()
    limit_nodes_by_degrees(graph, 7)
    graph.unorientate()
    g_type, path = hamilton_solve(graph, log_folder=log_folder + sub_folders[4])
    with open(log_folder + sub_folders[3] + 'euler_orientated_report.txt', 'w+') as f:
        f.write('the type of graph is ' + g_type + '\n')
        if path is not None:
            f.write('hamilton path is: ' + str(path) + '\n')


if __name__ == "__main__":
    solve('/home/san/Documents/university/babakov/lab7/')

