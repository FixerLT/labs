from my_graph import LabGraph
from generate_lab58_graph import get_graph_for_topic_1
from docx_helper import Reporter
from logs_helpers import get_log_for_edge


def limit_nodes_by_degrees(graph, limit):
    if len(graph.nodes) <= limit:
        return
    degrees = graph.get_node_degrees()
    degrees = sorted(enumerate(degrees), key=lambda e: e[1])
    graph.remove_nodes([e[0] for e in degrees[limit:]])


def find_start_end(graph, must_differ=False):
    outcoming_edges = [sum(len(e) for e in arr if e is not None) for arr in graph.edges]
    incoming_edges = []
    for i in range(len(graph.nodes)):
        incoming_edges.append(sum([len(graph.edges[j][i]) for j in range(len(graph.nodes)) if graph.edges[j][i] is not None]))
    start, end = outcoming_edges.index(max(outcoming_edges)), incoming_edges.index(max(incoming_edges))
    if must_differ and end == start:
        incoming_edges[end] = -100500
        end = incoming_edges.index(max(incoming_edges))
    return start, end


def get_common_prefix(iterable1, iterable2):
    min_len = min(len(iterable1), len(iterable2))
    result = []
    for i1, i2 in zip(iterable1[:min_len], iterable2[:min_len]):
        if i1 == i2:
            result.append(i1)
        else:
            break
    return result


def save_graph_for_path(path, folder, index, nodes_amount, flow=1, pref='', prev_path=()):
    edges = [(path[i], path[i+1], flow) for i in range(len(path) - 1)]
    common_prefix_len = len(get_common_prefix(path, prev_path))
    if common_prefix_len > 0:
        common_prefix_len -= 1
    edges, stash_edges = edges[:common_prefix_len], edges[common_prefix_len:]
    path_graph = LabGraph([str(e) for e in range(nodes_amount)], edges_list=edges)
    path_graph.add_to_stash(e_stash_list=stash_edges)
    path_graph.save_plot(folder, pref + 'step_' + str(index) + '_path')


def log_for_iteration(graph, path, flow, f, folder, index, reporter):
    graph.save_plot(folder, 'step_' + str(index) + '_graph')
    save_graph_for_path(path, folder, index, nodes_amount=len(graph.nodes), flow=f)
    reduced = []
    increased = []
    for e1, e2 in zip(path[:-1], path[1:]):
        reduced.append(get_log_for_edge((e1, e2)))
        increased.append(get_log_for_edge((e2, e1)))
    reporter.add_page(header='Новый Путь', image_path=folder + 'step_' + str(index) + '_path.png',
                      comment='Величина потока: {}\nУменьшены рёбра: {}\nУвеличины рёбра: {}'
                      .format(f, reduced, increased))

    reporter.add_page(header='Исходный Граф', image_path=folder + 'step_' + str(index) + '_graph.png',
                      comment='Результирующий поток: {}'.format(flow))


# TODO add marks
def solve_flows(graph, log_folder=None, start=None, end=None, different_start_end=None):
    if start is None or end is None:
        start, end = find_start_end(graph, must_differ=different_start_end)
    #print(str(start) + ' -> ' + str(end))
    reporter = Reporter()
    if log_folder is not None:
        graph.save_plot(log_folder, 'source')
        reporter.add_page(header='Поиск Максимального Потока\nИз {} в {}'.format(start, end),
                          image_path=log_folder + 'source.png',
                          comment='Будем находить пути из {} в {} и уменьшать поток в каждом ребре на минимальный поток'
                                  ' пути, таким образом ребро с данным минимальным потоком будет обнуляться. Рёбра с '
                                  'нулевым потоком будем удалять. Одновременно с этим обратные потоки будем увеличивать'
                                  ' обратные потоки на ту же величину минимального потока. Продолжим это, пока пути не '
                                  'закончатся'.format(start, end))
    graph.apply_fn_to_edges(lambda e: [sum(e)] if e is not None else None)
    if log_folder is not None:
        graph.save_plot(log_folder, 'source_sum')
        reporter.add_page(header='Поиск Максимального Потока\nИз {} в {}'.format(start, end),
                          image_path=log_folder + 'source.png',
                          comment='Заменили кратные рёбра на одно с суммарной пропускной способностью')
    flow = 0
    path, f = graph.get_shortest_path_by_edges_amount(start, end)
    it = 0
    while path is not None:
        flow += f
        deleted = graph.reduce_edges(path, f, should_add_to_stash=True)
        if log_folder is not None:
            log_for_iteration(graph, path, flow, f, log_folder, it, reporter)
        graph.clear_stash()
        graph.increase_edges(list(reversed(path)), f)
        it += 1
        path, f = graph.get_shortest_path_by_edges_amount(start, end)
    if log_folder is not None:
        reporter.save_report(path=log_folder, report_name='max_flow_report')
    return flow


def solve(source_graph, log_folder):
    graph = source_graph.copy()
    limit_nodes_by_degrees(graph, 10)
    print(solve_flows(graph, log_folder=log_folder))

