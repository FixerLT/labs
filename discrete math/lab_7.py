from generate_lab58_graph import get_graph_for_topic_1
from my_graph import LabGraph, table_to_edges_list
from data_structures import DisjointSetUnion
from lab_8 import limit_nodes_by_degrees, save_graph_for_path
from lab_6 import bfs_solve
from docx_helper import Reporter
from logs_helpers import get_log_for_path
import os
from logs_helpers import get_log_for_distance, get_log_for_path
# TODO: after reports done add semantic logs


# TODO: remove unorientate if needed
# TODO: work with connectivity component rather than all graph
def prima_solve(graph, log_folder=None, should_unorientate=True):
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(header='Алгоритм Прима. Исходный Граф', image_path=log_folder + 'source_graph.png')
    if should_unorientate:
        graph.unorientate()
        if log_folder is not None:
            graph.save_plot(log_folder, 'source_graph_unorientate')
            reporter.add_page(header='Исходный Граф', image_path=log_folder + 'source_graph_unorientate.png',
                              comment='Неориентированный')
    graph.apply_fn_to_edges(fn_connections=lambda e: [1] if e is not None else None)
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph_min_edge')
        reporter.add_page(header='Исходный Граф', image_path=log_folder + 'source_graph_min_edge.png',
                          comment='Кратные рёбра удалены')
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
        if log_folder is not None:
            prima_g.save_plot(log_folder, '{}_tree_step'.format(len(prima_g_connected) - 1))
            reporter.add_page(header='Алгоритм Прима\nШаг {}'.format(len(prima_g_connected)-1),
                              image_path=log_folder + '{}_tree_step.png'.format(len(prima_g_connected) - 1),
                              comment='Добавили вершину {}, её предок {}'.format(new_node, parent))
        prima_g.apply_stash()
        prima_g_connected.append(new_node)
    if log_folder is not None:
        prima_g.save_plot(log_folder, 'result')
        reporter.add_page(header='Результат Алгоритма Прима', image_path=log_folder + 'result.png')
        reporter.save_report(path=log_folder, report_name='prima_report')


def kruskal_solve(graph, log_folder=None, should_unorientate=True):
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(header='Алгоритм Крускала. Исходный Граф', image_path=log_folder + 'source_graph.png')
    if should_unorientate:
        graph.unorientate()
        if log_folder is not None:
            graph.save_plot(log_folder, 'source_graph_unorientate')
            reporter.add_page(header='Исходный Граф', image_path=log_folder + 'source_graph_unorientate.png',
                              comment='Неориентированный')
    graph.apply_fn_to_edges(fn_connections=lambda e: [min(e)] if e is not None else None)
    kruskal_g = LabGraph(graph.nodes, edges_list=[])
    edges = sorted(graph.edges_list, key=lambda e: e[2])
    dsu = DisjointSetUnion()
    for i in range(len(graph.nodes)):
        dsu.make_set(i)
    for edge in edges:
        if dsu.find_set(edge[0]) != dsu.find_set(edge[1]):
            kruskal_g.add_to_stash(e_stash_list=[edge])
            if log_folder is not None:
                kruskal_g.save_plot(log_folder, str(len(graph.nodes) - dsu.num_sets) + '_tree_step')
                reporter.add_page(header='Алгоритм Крускала\nШаг {}'.format(len(graph.nodes) - dsu.num_sets),
                                  image_path=log_folder + '{}_tree_step.png'.format(len(graph.nodes) - dsu.num_sets),
                                  comment='Объеденили вершины {} и {}'.format(edge[0], edge[1]))
            kruskal_g.apply_stash()
            dsu.union_sets(edge[0], edge[1])
            if dsu.num_sets == 1:
                break
    if log_folder is not None:
        kruskal_g.save_plot(log_folder, 'result')
        reporter.add_page(header='Результат Алгоритма Крускала', image_path=log_folder + 'result.png')
        reporter.save_report(path=log_folder, report_name='kruskal_report')


def merge_loops_into_one(loop, loops, start):
    if loop is None:
        return None, False
    loop_set = set(loop)
    j = start
    united_loops = False
    while j < len(loops):
        its = loop_set.intersection(set(loops[j]))
        if its is not None and len(its) > 0:  # TODO : check if second condition should be here
            its = list(its)[0]
            i_index = loop.index(its)
            j_index = loops[j].index(its)
            loop = loop[:i_index] + loops[j][j_index:] + loops[j][:j_index] + loop[i_index:]
            loops.pop(j)
            united_loops = True
        else:
            j += 1
    return loop, united_loops


# TODO optimize if possible
def merge_loops(loops):
    i = 0
    while i < len(loops):
        loops[i], united_loops = merge_loops_into_one(loops[i], loops, i+1)
        if not united_loops:
            i += 1


def extract_lines_loop(graph):
    starts = []
    for i in range(len(graph.nodes)):
        is_start = max(graph.cnt_outcoming_edges(i) - graph.cnt_incoming_edges(i), 0)
        while is_start > 0:
            starts.append(i)
            is_start -= 1
    if len(starts) == 0:
        return None, []
    new_edges = []
    path = []
    while len(starts) > 0:
        path.append(starts.pop())
        if len(path) > 0 and len(path) > 1:  # TODO: check second condition
            new_edges.append((path[-2], path[-1], 1))
        can_go = graph.get_neighbours_can_go(path[-1])
        while len(can_go) > 0:
            path.append(next(iter(can_go)))
            can_go = graph.get_neighbours_can_go(path[-1])
            graph.edges[path[-2]][path[-1]].pop()
            if len(graph.edges[path[-2]][path[-1]]) == 0:
                graph.edges[path[-2]][path[-1]] = None
    return path, new_edges


def extract_loops(graph, log_folder=None):
    if log_folder is not None and not os.path.exists(log_folder):
        os.mkdir(log_folder)
    graph.edges_list = table_to_edges_list(graph.edges)
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph_loops')
        reporter.add_page(header='Извлечение Циклв из Графа', image_path=log_folder + 'source_graph_loops.png')
    loops = []
    for node in range(len(graph.nodes)):
        while True:
            distances, paths = bfs_solve(graph, node)
            found = False
            for loop_end in range(len(graph.nodes)):
                if paths[loop_end] is not None and graph.edges[loop_end][node] is not None and len(graph.edges[loop_end][node]) > 0:
                    loops.append(paths[loop_end])
                    if log_folder is not None:
                        save_graph_for_path(loops[-1] + [node], log_folder, len(loops), len(graph.nodes))
                        reporter.add_page(header='Цикл {} Найден'.format(len(loops)),
                                          image_path=log_folder + 'step_' + str(len(loops)) + '_path.png')
                        # TODO: also save graph with path in stash for prettiness
                    graph.remove_loop(paths[loop_end])
                    found = True
                    break
            if not found:
                break
    graph.edges_list = table_to_edges_list(graph.edges)
    if log_folder is not None:
        graph.save_plot(log_folder, 'result_graph_loops')
        reporter.add_page(header='Из Графа Извлечено {} Циклов'.format(len(loops)),
                          image_path=log_folder +'result_graph_loops.png')
        reporter.save_report(log_folder, 'loops')
    return loops


def make_orientated_graph_eulerian_with_min_edges(graph, log_folder=None):
    if log_folder is not None and not os.path.exists(log_folder):
        os.mkdir(log_folder)
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(header='Сделать Граф Эйлеровым', image_path=log_folder + 'source_graph.png',
                          comment='Ориентированный')
    loops = extract_loops(graph, log_folder=log_folder + 'looops_extraction/')
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph_no_loops')
        reporter.add_page(header='Сделать Граф Эйлеровым\nИсходный Граф', image_path=log_folder + 'source_graph_no_loops.png',
                          comment='Циклов удалено: {}.'.format(len(loops)))
    merge_loops(loops)
    if log_folder is not None:
        comment = 'Циклы объеденены, теперь их {}:\n'.format(len(loops))
        for loop in loops:
            comment += get_log_for_path(loop) + '\n'
        reporter.add_page(header='Результат объединения извлечённых циклов', comment=comment)
    copy_of_graph = graph.copy()
    lines_loop, new_edges = extract_lines_loop(graph)
    if log_folder is not None:
        if lines_loop is not None:
            copy_of_graph.add_to_stash(e_stash_list=new_edges)
            copy_of_graph.save_plot(log_folder, 'graph_with_extra_edges')
            reporter.add_page(header='Сделан Последний Цикл', image_path=log_folder+'graph_with_extra_edges.png',
                              comment='К оставшимся рёбрам добавлено минимальное количество ребёр({}), '.format(len(new_edges)) +
                                      'чтобы они вместе образовывали один цикл.\nТеперь осталось объеденить все циклы в один')
            copy_of_graph.edges_stash_list = None
            copy_of_graph.edges_stash = None
        else:
            reporter.add_page(comment='Дополнительный цикл не требуется, ребёр после удаления цикла в графе не осталось')
    lines_loop, united = merge_loops_into_one(lines_loop, loops, 0)
    if lines_loop is not None:
        loops.append(lines_loop)
    if log_folder is not None:
        if united:
            reporter.add_page(comment='Некоторые циклы получилось добавить в последний цикл. '
                                      'Теперь всего {} непересекающихся циклов.'.format(len(loops)))
        else:
            reporter.add_page(comment='Циклы не получилось добавить в последний цикл. '
                                      'Теперь циклов всего {} непересекающихся циклов.'.format(len(loops)))
    euler_path = []
    if len(loops) > 0:
        for i, e in enumerate(loops):
            euler_path.extend(e)
            euler_path.append(e[0])  # because loop doesn't ends with first node, but there is edge e[-1], e[0]
            new_edges.append((e[0], loops[(i+1) % len(loops)][0], 1))
    else:
        euler_path = loops[0] + loops[0][0]
    if log_folder is not None:
        save_graph_for_path(euler_path, log_folder, 0, len(graph.nodes), prev_path=euler_path   )
        reporter.add_page(header='Эйлеров Путь Сформирован', image_path=log_folder + 'step_0_path.png',
                          comment='Всего добавлено {} новых рёбер\n'.format(len(new_edges)) + get_log_for_path(euler_path))
        reporter.save_report(path=log_folder, report_name='form_euler_graph')
    return new_edges, euler_path


def best_node_to_connect_in_component(component, degrees):
    return min(component, key=lambda i: -1 if degrees[i] % 2 == 1 else degrees[i])


def make_non_orientated_graph_eulerian_with_min_edges(graph, log_folder=None):
    if log_folder is not None and not os.path.exists(log_folder):
        os.mkdir(log_folder)
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(header='Сделать Граф Эйлеровым', image_path=log_folder + 'source_graph.png',
                          comment='Неориентированный')
    degrees = graph.get_node_degrees(orientated=False)
    unused = [i for i, e in enumerate(degrees) if e == 0]
    connectivity_components = []
    connected = set(unused)
    for e in range(len(graph.nodes)):
        if e in connected:
            continue
        distances, paths = bfs_solve(graph, e)
        component = {i for i, k in enumerate(distances) if k is not None}
        component.add(e)
        for k in component:
            connected.add(k)
        connectivity_components.append(component)
    if log_folder is not None:
        comment = 'Граф разделён на {} компонент связности:'.format(len(connectivity_components))
        for cmp in connectivity_components:
            comment += '\n' + str(cmp)
        reporter.add_page(comment=comment)
    new_edges = []
    while len(connectivity_components) > 1:
        node1 = best_node_to_connect_in_component(connectivity_components[-1], degrees)
        node2 = best_node_to_connect_in_component(connectivity_components[-2], degrees)
        degrees[node1] += 1
        degrees[node2] += 1
        connectivity_components[-2] = connectivity_components[-2].intersection(connectivity_components[-1])
        connectivity_components.pop()
        graph.add_to_stash(e_stash_list=[(node1, node2, 1), (node2, node1, 1)])
        new_edges.extend([(node1, node2, 1), (node2, node1, 1)])
        # graph.apply_stash()
    if log_folder is not None:
        if len(new_edges) > 0:
            graph.save_plot(folder=log_folder, filename='source_graph_connected')
            reporter.add_page(header='Сделать Граф Эйлеровым', image_path=log_folder + 'source_graph_connected.png',
                              comment='Добавлено {} новых рёбер, чтобы объеденить компоненты связности'.format(len(new_edges)/2))

    removed_edges = []
    if len(graph.nodes) % 2 == 0:
        max_odds = [i for i, e in enumerate(degrees) if e == len(graph.nodes)-1]
        if log_folder is not None and len(max_odds) > 0:
            reporter.add_page(comment='Есть {} вершин с максимальной степенью: {}\n{}\n'
                                      'Их степень необходимо понизить'.format(len(max_odds), len(graph.nodes)-1, max_odds))
        while len(max_odds) > 1:
            node1 = max_odds.pop()
            node2 = max_odds.pop()
            graph.edges[node1][node2] = None
            graph.edges[node2][node1] = None
            degrees[node1] -= 1
            degrees[node2] -= 1
            removed_edges.append((node1, node2, 1))
            removed_edges.append((node2, node1, 1))
        if len(max_odds) > 0:
            node1 = max_odds.pop()
            odds = [i for i, e in enumerate(degrees) if e % 2 == 1 and i != node1]
            node2 = (node1+1) % graph.nodes if len(odds) == 0 else odds[0]
            graph.edges[node1][node2] = None
            graph.edges[node2][node1] = None
            degrees[node1] -= 1
            degrees[node2] -= 1
            removed_edges.append((node1, node2, 1))
            removed_edges.append((node2, node1, 1))
        if log_folder is not None and len(removed_edges) > 0:
            removed_graph = LabGraph(edges_list=removed_edges)
            removed_graph.save_plot(log_folder, 'removed')
            reporter.add_page(header='Удалённые Рёбра', image_path=log_folder+'removed.png')

    odds = [i for i, e in enumerate(degrees) if e % 2 == 1]
    if log_folder is not None:
        if len(odds) > 0:
            reporter.add_page(comment='Осталось {} вершин с нечётными степенями:\n{}\n'.format(len(odds), odds) +
                              '\nСоеденим их')
    while len(odds) > 1:
        node1 = odds.pop()
        node2 = odds.pop()
        degrees[node1] += 1
        degrees[node2] += 1
        graph.add_to_stash(e_stash_list=[(node1, node2, 1), (node2, node1, 1)])
        new_edges.extend([(node1, node2, 1), (node2, node1, 1)])

    if log_folder is not None:
        graph.save_plot(folder=log_folder, filename='extended')
        reporter.add_page(header='Рёбра Добавлены. Граф Эйлеров', image_path=log_folder+'extended.png')
    graph.apply_stash()

    # TODO: review next copied code
    euler_path = [0]
    neighbour_sets = [graph.get_neighbours(i) for i in range(len(graph.nodes))]
    while sum([len(e) for e in neighbour_sets]) > 0:
        if log_folder is not None:
            cp = LabGraph(graph.nodes, edges_list=table_to_edges_list(graph.edges))
            for i in range(0, len(cp.edges)):
                for j in range(i, len(cp.edges)):
                    cp.edges[i][j] = None
            cp.save_plot(folder=log_folder + 'debug/', filename='remove_edges_{}'.format(len(euler_path)))
        node = euler_path[-1]
        if node in neighbour_sets[node]:
            euler_path.append(node)
            neighbour_sets[node].remove(node)
            graph.edges[node][node] = None
        else:
            for e in neighbour_sets[node]:
                if not graph.is_bridge(node, e, orientated=False):
                    degrees[node] -= 1
                    degrees[e] -= 1
                    euler_path.append(e)
                    graph.edges[node][e].pop()
                    if len(graph.edges[node][e]) == 0:
                        graph.edges[node][e] = None
                        neighbour_sets[node].remove(e)
                    graph.edges[e][node].pop()
                    if len(graph.edges[e][node]) == 0:
                        graph.edges[e][node] = None
                        neighbour_sets[e].remove(node)
                    break

    if log_folder is not None:
        reporter.add_page(comment='Эйлеров путь найден: {}'.format(euler_path))
        reporter.save_report(path=log_folder, report_name='euler_not_orientate')


# TODO make pretty log pictures on each step. (or not pretty)
# TODO if graph is not connected and orientated, solve problem for adding minimum edges
def euler_path(graph, log_folder=None, orientated=False):
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(header='Эйлеров Путь\nИсходный Граф', image_path=log_folder + 'source_graph.png')
    if not orientated:
        graph.unorientate()
        graph.apply_fn_to_edges(lambda e: [e[0]] if e is not None and len(e) > 0 else None)
        if log_folder is not None:
            graph.save_plot(log_folder, 'source_graph_unorientate')
            reporter.add_page(header='Эйлеров Путь\nНеориентированный Граф', image_path=log_folder + 'source_graph_unorientate.png')
    graph.apply_fn_to_edges(fn_connections=lambda e: [1] if e is not None else None)
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph_unique')
        reporter.add_page(header='Эйлеров Путь\nБез Кратных Рёбер', image_path=log_folder + 'source_graph_unique.png')
    for i in range(len(graph.nodes)):
        graph.edges[i][i] = None  # TODO learn to handle self-connected nodes
    degrees = graph.get_node_degrees(orientated=orientated)
    odds = [i for i, e in enumerate(degrees) if e % 2 == 1]
    if len(odds) == 0:
        g_type = 'euler'
        reporter.add_page(header='Эйлеров Путь', comment='Граф Эйлеров\n0 вершин с нечётной степенью')
    elif len(odds) == 2:
        g_type = 'semi-euler'
        reporter.add_page(header='Эйлеров Путь',
                          comment='Граф Полу-Эйлеров\n2 вершины с нечётной степенью\n' + str(odds))
    else:
        g_type = 'non_euler'
        reporter.add_page(header='Эйлеров Путь',
                          comment='Граф Полу-Эйлеров\nВершин с нечётной степенью: ' + str(len(odds)) + '\n' + str(odds))
    copy_of_graph = graph.copy()
    if orientated:
        make_orientated_graph_eulerian_with_min_edges(copy_of_graph, log_folder=log_folder + 'make_oriented/')
    else:
        make_non_orientated_graph_eulerian_with_min_edges(copy_of_graph, log_folder=log_folder + 'make_oriented/')
    if log_folder is not None and g_type is not 'euler':
        graph.save_plot(log_folder, 'source_graph_euler')
        reporter.add_page(header='Эйлеров Путь\nТеперь Эйлеров', image_path=log_folder + 'source_graph_euler.png')
        reporter.save_report(path=log_folder, report_name='euler_preruquisite')
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
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph')
        reporter.add_page(header='Поиск Гамильтонова Пути\nИсходный Граф', image_path=log_folder + 'source_graph.png')
    graph.apply_fn_to_edges(lambda e: [max(e)] if e is not None else None)
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_graph_max')
        reporter.add_page(header='Поиск Гамильтонова Пути\n', image_path=log_folder + 'source_graph_max.png',
                          comment='Кратные Рёбра заменены на одно')
    ham_path = None
    ham_loop = None
    prev_path = []
    log = ''
    log_return = 'Больше нет непосещённых соседей у вершины {}. Удаляем её с конца пути.\n'
    log_append = 'У последней в пути вершины {} есть непосещённый сосед {}. Добавляем его в конец пути.\n'
    appended = False
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
                if appended:
                    save_graph_for_path(visited, log_folder, iteration_counter, len(graph.nodes), pref='node_' + str(e) + '_', prev_path=prev_path)
                    reporter.add_page(image_path=log_folder + 'node_' + str(e) + '_step_' + str(iteration_counter) + '_path.png',
                                      comment=log)
                    log = ''
                    iteration_counter += 1
                prev_path = visited.copy()
                log += log_return.format(visited[-1])
                visited.pop()
                starts.pop()
                appended = False

            else:
                appended = True
                log += log_append.format(visited[-1], next_node)
                visited.append(next_node)
                starts[-1] = next_start
                starts.append(0)
                if len(visited) == len(graph.nodes):
                    ham_path = visited.copy()
                if len(visited) > len(graph.nodes):
                    ham_loop = visited.copy()
                    break
        if ham_loop is not None:
            break
    if ham_loop is not None:
        save_graph_for_path(ham_loop, log_folder, '0', len(graph.nodes))
        reporter.add_page(header='Гамильтонов Цикл Найден!', image_path=log_folder + 'step_0_path.png', comment=log)
        reporter.save_report(path=log_folder, report_name='hamilton_report')
        return 'hamilton', ham_loop
    if ham_path is not None:
        save_graph_for_path(ham_path, log_folder, '0', len(graph.nodes))
        reporter.add_page(header='Гамильтонов Путь Найден!', image_path=log_folder + 'step_0_path.png', comment=log)
        reporter.save_report(path=log_folder, report_name='hamilton_report')
        return 'semi-hamilton', ham_path
    reporter.add_page(header='Гамильтонов Пути не Существует!', comment=log)
    reporter.save_report(path=log_folder, report_name='hamilton_report')
    return 'non-hamilton', None


def solve(source_graph, log_folder):
    graph = source_graph.copy()
    sub_folders = ['prima/', 'kruskal/', 'euler_not_orientated/', 'euler_orientated/', 'hamilton/']
    for e in sub_folders:
        if not os.path.exists(log_folder + e):
            os.mkdir(log_folder + e)
    prima_solve(graph, log_folder=log_folder + sub_folders[0])
    kruskal_solve(graph, log_folder=log_folder + sub_folders[1])
    # TODO MAKE FUCKING REPORTS FOR EULER
    graph = source_graph.copy()
    g_type, path = euler_path(graph, log_folder=log_folder + sub_folders[2], orientated=False)
    with open(log_folder + sub_folders[2] + 'euler_non_orientated_report.txt', 'w+') as f:
        f.write('the type of non orientated graph is ' + g_type + '\n')
        if path is not None:
            f.write('euler path is: ' + str(path) + '\n')
    graph = source_graph.copy()
    g_type, path = euler_path(graph, log_folder=log_folder + sub_folders[3], orientated=True)
    with open(log_folder + sub_folders[3] + 'euler_orientated_report.txt', 'w+') as f:
        f.write('the type of orientated graph is ' + g_type + '\n')
        if path is not None:
            f.write('euler path is: ' + str(path) + '\n')
    graph = source_graph.copy()
    limit_nodes_by_degrees(graph, 7)
    graph.unorientate(duplicate=False)
    g_type, path = hamilton_solve(graph, log_folder=log_folder + sub_folders[4])
    with open(log_folder + sub_folders[4] + 'hamilton_report.txt', 'w+') as f:
        f.write('the type of graph is ' + g_type + '\n')
        if path is not None:
            f.write('hamilton path is: ' + str(path) + '\n')


if __name__ == '__main__':
    solve(LabGraph(), '')