from generate_lab58_graph import get_graph_for_topic_not_1


def save_to_file(report, path, file_name):
    print(report)
    return # TODO remove this debug statement fo really save reports
    with open(path + file_name + '.txt') as f:
        f.write(report)


def apply_str_stub_to_array(str_stub, arr, step='\n'):
    return ''.join(str_stub.format(*e) + step for e in arr)


graph = get_graph_for_topic_not_1()
path = "D:/Education/DonNU/Discrete math"  # '/home/san/Documents/university/babakov/lab5/'

task1 = 'Вершины: {}\nМощность: {}\n\nРёбра: {}\nМощность: {}\n\nДуги: {}\nМощность: {}\n\n'  # TODO distinguish Рёбра and Дуги
task1 = task1.format(str(graph.nodes), len(graph.nodes), graph.edges_list, len(graph.edges_list), graph.edges_list, len(graph.edges_list))
save_to_file(task1, path, '1')


adjacent_nodes = [len(graph.get_neighbours(i)) for i in range(len(graph.nodes))]  # количество соседей для каждой i
max_neighbours = max(adjacent_nodes)
nodes_with_max_neighbours = list(filter((lambda e: e[1] == max_neighbours), enumerate(adjacent_nodes)))

task2 = 'Вершина №{} {} смежных вершин'
task2 = apply_str_stub_to_array(task2, nodes_with_max_neighbours)
task2 += '\n'
save_to_file(task2, path, '2')

degrees = graph.get_node_degrees(orientated=True)
max_degree, min_degree = max(degrees), min(degrees)
max_degree_nodes = [i for i, e in enumerate(degrees) if e == max_degree]
min_degree_nodes = [i for i, e in enumerate(degrees) if e == min_degree]
task3_max = 'Вершина №{} имеет максимальную степень {}'
task3_min = 'Вершина №{} имеет минимальную степень {}'
task3_max = apply_str_stub_to_array(task3_max, [(e, max_degree) for e in max_degree_nodes])
task3_min = apply_str_stub_to_array(task3_min, [(e, min_degree) for e in min_degree_nodes])
save_to_file(task3_min + '\n' + task3_max + '\n', path, '3')

isoted_nodes = [i for i, e in enumerate(degrees) if e == 0]
pendant_nodes = [i for i, e in enumerate(degrees) if e == 1]
task4 = 'Количество изолированных вершин: {}\nКоличество концевых вершин: {}\n\n'
task4 = task4.format(str(len(isoted_nodes)), str(len(pendant_nodes)))
save_to_file(task4, path, '4')

max_degree = max([max([len(e) for e in row if e is not None]) for row in graph.edges])
max_degree_edges_arrays = ([[(i, j, max_degree)
                             for i in range(len(graph.nodes)) if
                                graph.edges[i][j] is not None and len(graph.edges[i][j]) == max_degree]
                             for j in range(len(graph.nodes))])
max_degree_edges = []
for e in max_degree_edges_arrays:
    max_degree_edges.extend(e)
task5 = 'Ребро {} -> {} имеет максимальную кратность({})'
task5 = apply_str_stub_to_array(task5, max_degree_edges) + '\n'
save_to_file(task5, path, '5')

loop_count = len([i for i in range(len(graph.nodes)) if graph.edges[i][i] is not None and len(graph.edges[i][i]) > 0])
task6 = 'Количество петель: {}\n\n'
task6 = task6.format(str(loop_count))
save_to_file(task6, path, '6')

#простым граф не может быть простым по условию (см. Лаб №0 п. 3)
# давай делать скрипт lab_5 независимо от условия в 0 лабе второго семестра. Чтобы наш код определял тип для всех случаев

if max_degree > 1:
    if loop_count > 0:
        s = "псевдографом"
    else:
        s = "мультиграфом"
else:
    s = 'простым'
task7 = 'Граф является {}\n\n'
task7 = task7.format(s)
save_to_file(task7, path, '7')




