from generate_lab58_graph import get_graph_for_topic_1
from my_graph import LabGraph, table_to_edges_list
import os


def bfs_solve(graph, node, log_folder=None):
    paths = [None for i in range(len(graph.nodes))]
    paths[node] = [node]
    visited = {node}
    to_visit = [node]
    bfs_graph = LabGraph(graph.nodes, edges_list=[])
    search_index = 0
    distance = {node: 0}
    while len(visited) < len(graph.nodes) and search_index<len(to_visit):
        new_node = to_visit[search_index]
        neighbours = graph.get_neighbours(new_node)
        for neighbour in neighbours:
            if neighbour not in visited:
                paths[neighbour] = paths[new_node] + [neighbour]
                distance[neighbour] = distance[new_node] + 1
                to_visit.append(neighbour)
                visited.add(neighbour)
                bfs_graph.add_to_stash(e_stash_list=[(new_node, neighbour, 1)])
                bfs_graph.apply_stash()
                if log_folder is not None:
                    bfs_graph.save_plot(log_folder, 'bfs_step_' + str(len(distance)-1))
        search_index += 1
        to_visit.pop(0)
    return distance, paths


def dijkstra_solve(graph, node, log_folder=None):
    graph.apply_fn_to_edges(lambda e: [min(e)] if e is not None else None)
    distances = [-1 for i in range(len(graph.nodes))]  # TODO change -1 to None for proper display of distances in log
    parents = [-1 for i in range(len(graph.nodes))]
    distances[node] = 0
    to_visit = []
    visit_index = 0
    dijkstra_g = LabGraph(graph.nodes, edges_list=[])
    while len([(i, e) for i, e in enumerate(distances) if (e != -1 and i not in to_visit)]) > 0:
        to_visit.append(min([(i, e) for i, e in enumerate(distances) if (e != -1 and i not in to_visit)], key=lambda x: x[1])[0])
        current = to_visit[visit_index]
        visit_index += 1
        if current != node:
            dijkstra_g.add_to_stash(e_stash_list=[(parents[current], current, graph.edges[parents[current]][current][0])])
            dijkstra_g.apply_stash()
            dijkstra_g.save_plot(log_folder, 'dijkstra_step_' + str(visit_index-1))
        for i, d in [(i, d[0]) for i, d in enumerate(graph.edges[current]) if d is not None]:
            if distances[i] == -1 or distances[i] > distances[current] + d:
                distances[i] = distances[current] + d
                parents[i] = current
    paths = [[i] for i in range(len(parents))]
    for path in paths:
        while parents[path[-1]] != -1:
            path.append(parents[path[-1]])
    paths = [list(reversed(e)) for e in paths]
    return distances, paths


# TODO понижение весов на каждом шагу
def bellman_ford_solve(graph, node, log_folder=None):
    graph.apply_fn_to_edges(lambda e: [min(e)] if e is not None else None)
    graph.edges_list = table_to_edges_list(graph.edges)
    distances = [None for i in range(len(graph.nodes))]
    parents = [None for i in range(len(graph.nodes))]
    paths = [None for i in range(len(graph.nodes))]
    parents[node] = node
    distances[node] = 0
    paths[node] = [node]
    bellman_ford_g = LabGraph(graph.nodes, edges_list=[])
    relaxation_counter = 0
    flags = [False, False]
    loops = set()
    for x in range(len(graph.nodes) - 1):
        if flags[1]:
            break
        flags[1] = flags[0]
        flag = True
        for edge in graph.edges_list:
            if distances[edge[0]] is not None:
                if distances[edge[1]] is None or (distances[edge[1]] > distances[edge[0]] + edge[2] \
                        and (parents[edge[1]] is None or parents[edge[1]] != edge[0])):
                    if edge[1] in paths[edge[0]]:
                        loops.add(tuple(paths[edge[0]][paths[edge[0]].index(edge[1]):] + [edge[1]]))
                    else:
                        distances[edge[1]] = distances[edge[0]] + edge[2]
                        if parents[edge[1]] is not None:
                            bellman_ford_g.edges[parents[edge[1]]][edge[1]] = None
                        bellman_ford_g.edges[edge[0]][edge[1]] = [edge[2]]
                        bellman_ford_g.save_plot(log_folder, 'bellman_ford_relaxation_' + str(relaxation_counter))
                        relaxation_counter += 1
                        parents[edge[1]] = edge[0]
                        paths[edge[1]] = paths[edge[0]] + [edge[1]]
                        flag = False
        flags[0] = flag
    paths = [[i] for i in range(len(parents))]
    for path in paths:
        while parents[path[-1]] is not None and parents[path[-1]] not in path:
            path.append(parents[path[-1]])
    paths = [list(reversed(e)) for e in paths]
    return distances, paths, loops


def save_log(file_name, distances, paths, loops=None):
    with open(file_name, 'w+') as f:
        for i, d in enumerate(distances):
            f.write('distance to node ' + str(i) + ' is ' + str(d) + '\n')
        f.write('\n')
        for i, path in enumerate(paths):
            f.write('path to ' + str(i) + ' is ' + str(path) + '\n')
        f.write('\n')
        if loops is not None:
            for loop in loops:
                f.write('loop found: ' + str(loop) + '\n')


def solve(log_folder):
    sub_folders = ['bfs/', 'dijkstra/', 'bellman-ford/']
    for e in sub_folders:
        if not os.path.exists(log_folder + e):
            os.mkdir(log_folder + e)

    graph = get_graph_for_topic_1()
    graph.unorientate()
    distances, paths = bfs_solve(graph, 0, log_folder + sub_folders[0])  # TODO взять вершину с максимальной кратностью
    save_log(log_folder + sub_folders[0] + 'bfs_report.txt', distances, paths)

    graph = get_graph_for_topic_1()
    graph.apply_fn_to_edges(lambda e: [abs(k) for k in e] if e is not None else None)
    distances, paths = dijkstra_solve(graph, max(enumerate(graph.count_nodes_outcoming_edges()), key=lambda kv: kv[1])[0], log_folder + sub_folders[1])
    save_log(log_folder + sub_folders[1] + 'dijkstra_report.txt', distances, paths)

    graph = get_graph_for_topic_1()
    graph.add_to_stash(e_stash_list=[(0, 1, -5), (5, 2, -1)])  # TODO взять вершины с отрицательным весом со смыслом
    graph.apply_stash()
    distances, paths, loops = bellman_ford_solve(graph, max(enumerate(graph.count_nodes_outcoming_edges()), key=lambda kv: kv[1])[0], log_folder=log_folder+sub_folders[2])
    save_log(log_folder + sub_folders[2] + 'bellman_ford_report.txt', distances, paths, loops=loops)


if __name__ == "__main__":
    solve('/home/san/Documents/university/babakov/lab6/')
