from my_graph import LabGraph
from generate_lab58_graph import get_graph_for_topic_1


def limit_nodes_by_degrees(graph, limit):
    if len(graph.nodes) <= limit:
        return
    degrees = graph.get_node_degrees()
    degrees = sorted(degrees.items(), key=lambda e: e[1])
    graph.remove_nodes([e[0] for e in degrees[limit:]])


def find_start_end(graph, must_differ=False):
    outcoming_edges = [sum(len(e) for e in arr) for arr in graph.edges]
    incoming_edges = []
    for i in range(len(graph.nodes)):
        incoming_edges.append(sum([len(graph.edges[j][i]) for j in range(len(graph.nodes))]))
    start, end = outcoming_edges.index(max(outcoming_edges)), incoming_edges.index(max(incoming_edges))
    if must_differ and end == start:
        incoming_edges[end] = -100500
        end = incoming_edges.index(max(incoming_edges))
    return start, end


def log_for_iteration(graph, path, flow, folder, index):
    graph.save_plot(folder, 'step_' + str(index) + '_graph')
    edges = [(path[i], path[i+1], flow) for i in range(len(path) - 1)]
    path_graph = LabGraph(graph.nodes, edges_list=edges)
    path_graph.save_plot(folder, 'step_' + str(index) + '_path')


def solve(graph, log_folder=None, different_start_end=True):
    start, end = find_start_end(graph, must_differ=different_start_end)
    print(str(start) + ' -> ' + str(end))
    flow = 0
    path, f = graph.get_shortest_path_by_edges_amount(start, end)
    it = 0
    while path is not None:
        flow += f
        graph.reduce_edges(path, f)
        if log_folder is not None:
            log_for_iteration(graph, path, f, log_folder, it)
        it += 1
        path, f = graph.get_shortest_path_by_edges_amount(start, end)
    return flow


graph = get_graph_for_topic_1()
limit_nodes_by_degrees(graph, 10)
print(solve(graph, log_folder='/home/san/Documents/university/babakov/lab8/'))
