from my_graph import LabGraph, table_to_edges_list
import os
import json
import docx_helper
from docx_helper import Reporter, PageReport
from logs_helpers import get_log_for_path, get_log_for_distance


def bfs_solve(graph, node, log_folder=None):
    reporter = Reporter()
    log_step = 'С вершины {} есть ребро в непосещённую вершину {}\nРасстояние до новой вершины: {}\n'
    log_update = 'Начинаем поиск с вершины {}\n'
    log_finished = 'Больше нет непосещённых вершин среди соседей {}\n'
    file_template = 'bfs_step_{}'
    header_template = 'Поиск в Ширину. Шаг {}'
    logs = []
    log = ''
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(
            PageReport(header='Алгоритм Поиска в Ширину. Исходный Граф', image_path=log_folder + 'source_graph.png'))
    paths = [None] * len(graph.nodes)
    paths[node] = [node]
    visited = {node}
    to_visit = [node]
    bfs_graph = LabGraph(graph.nodes, edges_list=[])
    search_index = 0
    distance = {node: 0}
    while len(visited) < len(graph.nodes) and search_index < len(to_visit):
        new_node = to_visit[search_index]
        neighbours = graph.get_neighbours(new_node)
        log += log_update.format(new_node)
        for neighbour in neighbours:
            if neighbour not in visited:
                paths[neighbour] = paths[new_node] + [neighbour]
                distance[neighbour] = distance[new_node] + 1
                to_visit.append(neighbour)
                visited.add(neighbour)
                bfs_graph.add_to_stash(e_stash_list=[(new_node, neighbour, 1)])
                bfs_graph.apply_stash()
                if log_folder is not None:
                    bfs_graph.save_plot(log_folder, file_template.format(len(distance) - 2))
                    log += log_step.format(new_node, neighbour, distance[neighbour])
                    reporter.add_page(PageReport(header=header_template.format(len(distance)-2),
                                                 image_path=log_folder + file_template.format(len(distance)-2) + '.png',
                                                 comment=log))
                    log = ''
        search_index += 1
        to_visit.pop(0)
        log += log_finished.format(new_node)
    if log_folder is not None:
        with open(log_folder + 'logs.txt', 'w+') as f:
            json.dump(logs, f)
        if len(log) > 0:
            reporter.add_page(PageReport(comment=log))
        result = ''
        for i in sorted(distance.keys()):
            if i != node:
                result += get_log_for_distance(i, distance[i])
                result += get_log_for_path(paths[i])
        reporter.add_page(PageReport(header='Результат поиска в ширину', comment=result))
        reporter.save_report(path=log_folder, report_name='bfs_report')
    return distance, paths


def dijkstra_solve(graph, node, log_folder=None):
    reporter = Reporter()
    log_step = 'С вершины {} есть ребро в вершину {}\nДлина ребра: {}; расстояние до вершины уменьшено с {} до {}\n'
    log_update = 'Минимальное расстояние до вершины №{} равно {}. Фиксируем её и обновляем кратчайшие расстояния до остальных вершин\n'
    log_finished = 'Больше нет непосещённых вершин среди соседей {}\n'
    log = ''
    file_template = 'dijkstra_step_{}'
    header_template = 'Алгоритм Дейкстры. Шаг {}'
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(
            PageReport(header='Алгоритм Дейкстры. Исходный Граф', image_path=log_folder + 'source_graph.png'))

    graph.apply_fn_to_edges(lambda e: [min(e)] if e is not None else None)
    distances = [-1] * len(graph.nodes)  # TODO change -1 to None for proper display of distances in log
    parents = [-1] * len(graph.nodes)
    distances[node] = 0
    visited = []
    visit_index = 0
    dijkstra_g = LabGraph(graph.nodes, edges_list=[])
    while len([(i, e) for i, e in enumerate(distances) if (e != -1 and i not in visited)]) > 0:
        visited.append(min([(i, e) for i, e in enumerate(distances) if (e != -1 and i not in visited)], key=lambda x: x[1])[0])
        current = visited[visit_index]
        visit_index += 1
        if current != node:
            log += log_update.format(current, distances[current])
            dijkstra_g.add_to_stash(e_stash_list=[(parents[current], current, graph.edges[parents[current]][current][0])])
            dijkstra_g.apply_stash()
            dijkstra_g.save_plot(log_folder, file_template.format(visit_index-2))
            if log_folder is not None:
                reporter.add_page(PageReport(header=header_template.format(visit_index-2),
                                             image_path=log_folder + file_template.format(visit_index-2) + '.png',
                                             comment=log))
            log = ''
        for i, d in [(i, d[0]) for i, d in enumerate(graph.edges[current]) if d is not None]:
            if distances[i] == -1 or distances[i] > distances[current] + d:
                log += log_step.format(current, i, d, 'infinity' if distances[i] is None else distances[i], distances[current] + d)
                distances[i] = distances[current] + d
                parents[i] = current
        log += log_finished.format(current)
    if log_folder is not None and len(log) > 0:
        reporter.add_page(PageReport(comment=log))
    paths = [[i] for i in range(len(parents))]
    for path in paths:
        while parents[path[-1]] != -1:
            path.append(parents[path[-1]])
    paths = [list(reversed(e)) for e in paths]

    if log_folder is not None:
        result = ''
        for i in range(len(graph.nodes)):
            if i != node:
                result += get_log_for_distance(i, distances[i])
                result += get_log_for_path(paths[i])
        reporter.add_page(PageReport(header='Результат поиска в ширину', comment=result))
        reporter.save_report(path=log_folder, report_name='dijkstra_report')

    return distances, paths


# TODO понижение весов на каждом шагу
# TODO iteration no relaxation report
def bellman_ford_solve(graph, node, log_folder=None):
    reporter = Reporter()
    file_template = 'bellman_ford_relaxation_{}'
    header_template = 'Алгоритм Беллмана-Форда. Шаг {}'
    log_template = 'Путь в вершину {} равен {}, релаксируем до {}\nРасстояние до {} равно {}, а длина ребра {}, {} - {}'
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(
            PageReport(header='Алгоритм Беллмана-Форда\nИсходный Граф', image_path=log_folder + 'source_graph.png'))
    graph.apply_fn_to_edges(lambda e: [min(e)] if e is not None else None)
    graph.edges_list = table_to_edges_list(graph.edges)
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph_min')
        reporter.add_page(
            PageReport(header='Алгоритм Беллмана-Форда\nГраф с минимальными весами кратных рёбер', image_path=log_folder + 'source_graph_min.png'))
    graph.edges_list = table_to_edges_list(graph.edges)
    distances = [None] * len(graph.nodes)
    parents = [None] * len(graph.nodes)
    paths = [None] * len(graph.nodes)
    parents[node] = node
    distances[node] = 0
    paths[node] = [node]
    bellman_ford_g = LabGraph(graph.nodes, edges_list=[])
    relaxation_counter = 0
    flags = [False, False]
    loops = set()
    for x in range(len(graph.nodes) - 1):
        reporter.extend_last_comment('Итерируем все вершины')
        if flags[1]:
            reporter.add_page(comment='При последнем обходе вершин релаксации не получилось. Завершаем итерации')
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
                        bellman_ford_g.save_plot(log_folder, file_template.format(relaxation_counter))
                        if log_folder is not None:
                            reporter.add_page(PageReport(header=header_template.format(relaxation_counter),
                                                         image_path=log_folder +
                                                                    file_template.format(relaxation_counter) + '.png',
                                                         comment=log_template.format(edge[1], distances[edge[1]],
                                                                                     distances[edge[0]] + edge[2],
                                                                                     edge[0], distances[edge[0]],
                                                                                     edge[0], edge[1], edge[2])))
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
    if log_folder is not None:
        result = ''
        for i in range(len(graph.nodes)):
            if i != node:
                result += get_log_for_distance(i, distances[i])
                result += get_log_for_path(paths[i])
        reporter.add_page(PageReport(header='Результат поиска алгоритмом Беллмана-Форда', comment=result))
        reporter.save_report(path=log_folder, report_name='bellman-ford_report')
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


# TODO single graph copy, don't create new graphs
def solve(source_graph, log_folder):
    sub_folders = ['bfs/', 'dijkstra/', 'bellman-ford/']
    for e in sub_folders:
        if not os.path.exists(log_folder + e):
            os.mkdir(log_folder + e)

    graph = source_graph.copy()
    graph.save_plot(log_folder, 'source_graph')
    graph.unorientate()
    graph.apply_fn_to_edges(lambda e: [1] if e is not None else None)
    distances, paths = bfs_solve(graph, 0, log_folder + sub_folders[0])  # TODO взять вершину с максимальной кратностью
    save_log(log_folder + sub_folders[0] + 'bfs_report.txt', distances, paths)

    graph = source_graph.copy()
    graph.apply_fn_to_edges(lambda e: [abs(k) for k in e] if e is not None else None)
    distances, paths = dijkstra_solve(graph, max(enumerate(graph.count_nodes_outcoming_edges()), key=lambda kv: kv[1])[0], log_folder + sub_folders[1])
    save_log(log_folder + sub_folders[1] + 'dijkstra_report.txt', distances, paths)

    graph = source_graph.copy()
    graph.add_to_stash(e_stash_list=[(0, 1, -5), (5, 2, -1)])  # TODO взять вершины с отрицательным весом со смыслом
    graph.apply_stash()
    distances, paths, loops = bellman_ford_solve(graph, max(enumerate(graph.count_nodes_outcoming_edges()), key=lambda kv: kv[1])[0], log_folder=log_folder+sub_folders[2])
    save_log(log_folder + sub_folders[2] + 'bellman_ford_report.txt', distances, paths, loops=loops)


if __name__ == "__main__":
    solve('/home/san/Documents/university/babakov/lab6/')
