from generate_lab58_graph import get_graph_for_topic_not_1


def save_to_file(report, path, file_name):
    print(report)
    return
    with open(path + file_name + '.txt') as f:
        f.write(report)


graph = get_graph_for_topic_not_1()
path = "D:/Education/DonNU/Discrete math"  # '/home/san/Documents/university/babakov/lab5/'

task1 = 'Вершины: {}\nМощность: {}\n\nРёбра: {}\nМощность: {}\n\nДуги: {}\nМощность: {}\n\n'  # TODO distinguish Рёбра and Дуги
task1 = task1.format(str(graph.nodes), len(graph.nodes), graph.edges_list, len(graph.edges_list), graph.edges_list, len(graph.edges_list))
save_to_file(task1, path, '1')


adjacent_nodes = []
for i in range(len(graph.nodes)):
    adjacent_nodes.append(set())
    for j in range(len(graph.nodes)):
        if len(graph.edges[i][j]) > 0:
            adjacent_nodes[-1].add(j)
        if len(graph.edges[j][i]) > 0:
            adjacent_nodes[-1].add(j)

max_ = 0
max_index = []
for i in range(len(graph.nodes)):
    if len(adjacent_nodes[i]) == max_:
        max_index.append(i)
    if len(adjacent_nodes[i]) > max_:
        max_ = len(adjacent_nodes[i])
        max_index = [i]

task2 = 'Вершина №{} {} смежных вершин\n\n' # TODO if two or more nodes have max amount of adjacented nodes
task2 = task2.format(str(max_index), str(max_))
save_to_file(task2, path, '2')


max_index = []
max_ = 0
min_index = []
min_ = 0
isolated_vertex = []
pendant_vertex = []

for i in range(len(graph.nodes)):
    curr_edges = 0
    for j in adjacent_nodes[i]:
        curr_edges += len(graph.edges[i][j])+len(graph.edges[j][i])
        if i == j:
            curr_edges -= len(graph.edges[i][j])
    if i == 0:
        min_ = curr_edges
    if curr_edges == max_:
        max_index.append([i])
    if curr_edges == min_:
        min_index.append([i])
    if curr_edges > max_:
        max_ = curr_edges
        max_index = [i]
    if curr_edges < min_:
        min_ = curr_edges
        min_index = [i]
    if curr_edges == 0:
        isolated_vertex.append(i)
    if curr_edges == 1:
        pendant_vertex.append(i)

task3 = 'Вершина №{} имеет максимальную степень {}\nВершина №{} имеет минимальную степень {}\n\n' # TODO two or more nodes have max/min degree
task3 = task3.format(str(max_index), str(max_), str(min_index), str(min_))
save_to_file(task3, path, '3')

task4 = 'Количество изолированных вершин: {}\nКоличество концевых вершин: {}\n\n'
task4 = task4.format(str(len(isolated_vertex)), str(len(pendant_vertex)))
save_to_file(task4, path, '4')

edges_list = graph.edges_list.copy()
edges_list.sort()
max_ = 0
max_index = 0
curr_edges = 0
for i in range(1, len(edges_list)):
    if edges_list[i][0] == edges_list[i-1][0] and edges_list[i][1] == edges_list[i-1][1]:
        curr_edges += 1
    else:
        if curr_edges > max_:
            max_ = curr_edges
            max_index = i-1
        curr_edges = 0
if curr_edges > max_:
    max_ = curr_edges
    max_index = i-1
max_ += 1

task5 = 'Ребро {} -> {} имеет максимальную кратность({})\n\n'# TODO two or more edges have max multiplicity
task5 = task5.format(str(edges_list[max_index][0]), str(edges_list[max_index][1]), max_)
save_to_file(task5, path, '5')
max_multiplicity = max_

loop_count = 0
for i in range(len(graph.nodes)):
    loop_count += len(graph.edges[i][i])
task6 = 'Количество петель: {}\n\n'
task6 = task6.format(str(loop_count))
save_to_file(task6, path, '6')

#простым граф не может быть простым по условию (см. Лаб №0 п. 3)
# давай делать скрипт lab_5 независимо от условия в 0 лабе второго семестра. Чтобы наш код определял тип для всех случаев
s=""
if loop_count == 0:
    s = "мультиграфом"
else:
    s = "псевдографом"
task7 = 'Граф является {}\n\n'
task7 = task7.format(s)
save_to_file(task7, path, '7')




