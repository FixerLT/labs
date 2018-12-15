from generate_lab58_graph import get_graph_for_topic_1


def save_to_file(report, path, file_name):
    print(report)
    return
    with open(path + file_name + '.txt') as f:
        f.write(report)


graph = get_graph_for_topic_1()
path = '/home/san/Documents/university/babakov/lab5/'

task1 = 'Вершины: {}\nМощность: {}\n\nРёбра: {}\nМощность: {}\n\nДуги: {}\nМощность: {}\n\n'  # TODO distinguish Рёбра and Дуги
task1 = task1.format(str(graph.nodes), len(graph.nodes), graph.edges_list, len(graph.edges_list), graph.edges_list, len(graph.edges_list))
save_to_file(task1, path, '1')