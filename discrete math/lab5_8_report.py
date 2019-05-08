from generate_lab58_graph import get_graph_for_topic_1, get_graph_from_txt, make_graph_manually
import lab_6
import lab_7
import lab_8
src_path = '/home/mark/Documents/university/babakov/'


def solve_lab_6(graph):
    path = src_path + 'lab6/'
    lab_6.solve(graph, path)


def solve_lab_7(graph):
    path = src_path + 'lab7/'
    lab_7.solve(graph, path)


def solve_lab_8(graph):
    path = src_path + 'lab8/'
    print(lab_8.solve(graph, path))


# graph = get_graph_for_topic_1()
graph = get_graph_from_txt(file_path='/home/mark/Coding/py/projects/DNOLABS/labs/discrete math/helpers/alex_graph.txt',
                           reduce_edges=False, has_distances=True)
# graph = make_graph_manually()

# solve_lab_6(graph.copy())
solve_lab_7(graph.copy())
solve_lab_8(graph.copy())
