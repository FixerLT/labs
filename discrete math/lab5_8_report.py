from generate_lab58_graph import get_graph_for_topic_1, get_graph_from_txt
import lab_6
import lab_7
import lab_8
src_path = '/home/san/Documents/university/babakov/'


def solve_lab_6(graph):
    path = src_path + 'lab6/'
    lab_6.solve(graph, path)


def solve_lab_7(graph):
    path = src_path + 'lab7/'
    lab_7.solve(graph, path)


def solve_lab_8(graph):
    path = src_path + 'lab8/'
    print(lab_8.solve(graph, path))


graph = get_graph_for_topic_1()
# graph = get_graph_from_txt()

solve_lab_6(graph.copy())
solve_lab_7(graph.copy())
solve_lab_8(graph.copy())
