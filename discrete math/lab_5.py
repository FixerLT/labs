import random
from generate_lab58_graph import get_graph_for_topic_not_1


def save_to_file(report, path, file_name):
    print(report)
    return # TODO remove this debug statement fo really save reports
    with open(path + file_name + '.txt') as f:
        f.write(report)


def apply_str_stub_to_array(str_stub, arr, step='\n'):
    return ''.join(str_stub.format(*e) + step for e in arr)

path = "D:/Education/DonNU/Discrete math/"  # '/home/san/Documents/university/babakov/lab5/'
graph = get_graph_for_topic_not_1((path, 'topic_1_src'))

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

def bfs(start_node, graph):
    nodes = [-1]*len(graph.nodes)
    nodes[start_node] = -2
    queue = [start_node]
    while len(queue) > 0:
        start_node = queue[0]
        queue = queue[1:]
        for i in range(len(graph.nodes)):
            if nodes[i] == -1 and graph.edges[start_node][i] is not None and start_node != i:
                queue.append(i)
                nodes[i] = start_node
    path = []
    while nodes[start_node] != -2:
        path.append(start_node)
        start_node = nodes[start_node]
    path.append(start_node)
    return path[::-1]

def make_beautiful_path(path):
    beautiful_path = ""
    for i in path:
        beautiful_path += str(i) + " -> "
    return beautiful_path[:-3]

def tasks_8_10_12():
    paths = []
    nodes_list = [i for i in range(len(graph.nodes))]
    random.shuffle(nodes_list)
    i = 0
    while len(paths) < 3:
        path = bfs(nodes_list[i], graph)
        i += 1
        if len(path) > 1:
            paths.append(path)

    result = ""
    counter = 0
    for i in paths:
        counter += 1
        result += "Путь №" + str(counter) + ": "
        result.format()
        result += make_beautiful_path(i)
        path_len = 0
        for j in range(1, len(i)):
            path_len += graph.edges[i[j-1]][i[j]][0]
        result += "\nДлина: " + str(path_len) + "\n"
    return result

task8 = tasks_8_10_12()
save_to_file(task8, path, '8')

def dfs(start_node, graph, used_nodes = [], curr_node = -1, path = []):
    if curr_node == -1:
        curr_node = start_node
        path = [curr_node]
    used_nodes[curr_node] = True
    #path.append(curr_node)
    for i in range(len(graph.nodes)):
        if graph.edges[curr_node][i] is not None:
            if not used_nodes[i]:
                path.append(i)
                path2 = dfs(start_node, graph, used_nodes, i, path.copy())
                if path2 is not None:
                    return path2
                else:
                    path = path[:-1]
            elif i == start_node and len(path) >= 3:
                return path
    return None

 # В лекции пример контура написан через ребра. TODO Нужно уточнить что выводить вершины или ребра

def tasks_9_11_13():
    paths = []
    nodes_list = [i for i in range(len(graph.nodes))]
    random.shuffle(nodes_list)
    i = 0
    while len(paths) < 3 and i < 15:
        path = dfs(nodes_list[i], graph, used_nodes=[False] * len(graph.nodes))
        if path is not None:
            path.append(nodes_list[i])
        i += 1
        if path is not None and len(path) > 2:
            paths.append(path)

    #TODO если нет 3х контуров. (они есть, можно даже петли вывести)
    result = ""
    counter = 0
    for i in paths:
        counter += 1
        result += "Путь №" + str(counter) + ": "
        result.format()
        result += make_beautiful_path(i)
        path_len = 0
        for j in range(1, len(i)):
            path_len += graph.edges[i[j-1]][i[j]][0]
        result += "\nДлина: " + str(path_len) + "\n"
    return result

task9 = tasks_9_11_13() # если есть 3 пути, то всё ок, иначе нужно ещё какую-то функцию придумать,
                        # так как контур, при заданых условиях должен быть практически всегда
save_to_file(task9, path, '9')

task10 = tasks_8_10_12()
save_to_file(task10, path, '10')

task11 = tasks_9_11_13()  #по идее данное решение должно всегда давать правильный ответ(контрпример придумать не могу)
save_to_file(task11, path, '11')

task12 = tasks_8_10_12()
save_to_file(task12, path, '12')

task13 = tasks_9_11_13()
save_to_file(task13, path, '13')

#14-17

is_symmetric = True
for i in range(len(graph.nodes)):
    for j in range(i, len(graph.nodes)):
        if graph.edges[i][j] is not None:
            if not (graph.edges[j][i] is not None and len(graph.edges[i][j]) == len(graph.edges[j][i])):
                is_symmetric = False
                i = len(graph.edges) + 1 # что бы выйти из первого цикла тоже
                break

if is_symmetric:
    s = "симметричным"
else:
    s = "антисимметричным"
task18 = 'Граф является {}\n\n'
task18 = task18.format(s)
save_to_file(task18, path, '18')

def component_finder(start_node, visited):
    visited[start_node] = True
    for i in range(len(graph.nodes)):
        if not visited[i] and graph.edges[start_node][i] is not None:
            component_finder(i, visited)

components = 0
visited = [False] * len(graph.nodes)
for i in range(len(graph.nodes)):
    if not visited[i]:
        component_finder(i, visited)
        components += 1

if components == 1:
    task19 = "Граф связный\n\n"
else:
    task19 = "Граф не связный, количество компонент связности: " + str(components) + "\n\n"
save_to_file(task19, path, '19')

#20

edges_count = 0
for i in (range(len(graph.nodes))):
    for j in (range(len(graph.nodes))):
        if graph.edges[i][j] is not None:
            edges_count += 1

if edges_count == 0:
    task21 = "Граф пустой\n\n"
elif edges_count == len(graph.nodes)**2:
    task21 = "Граф полный\n\n"
else:
    task21 = "Граф ни пустой, ни полный\n\n"
save_to_file(task21, path, '21')

nodes_degree = graph.get_node_degrees()
#for i in graph.nodes:
 #   nodes_degree.append(graph.get_node_degrees(i))

is_regular = True
for i in (range(1, len(graph.nodes))):
    if nodes_degree[i-1] != nodes_degree[i]:
        is_regular = False
        break
if is_regular:
    task22 = "Граф однородный\n\n"
    task23 = "Граф регулярный, степень регулярности: " + str(nodes_degree[0]) + "\n\n"
else:
    task22 = "Граф не однородный\n\n"
    task23 = "Граф не регулярный\n\n"

save_to_file(task22, path, '22')
save_to_file(task23, path, '23')

#24

task25 = "\t" # писать вес или просто 1? и что делать с кратными ребрами?
for i in (range(len(graph.nodes))):
    task25 += str(i) + "\t"
for i in (range(len(graph.nodes))):
    task25 += "\n" + str(i) + "\t"
    for j in (range(len(graph.nodes))):
        if graph.edges[i][j] is not None:
            task25 += str(graph.edges[i][j][0]) + "\t"
        else:
            task25 += "0\t"
task25 += "\n\n"
save_to_file(task25, path, '25')

task26 = "\t"
for i in range(len(graph.edges_list)):
    task26 += str(i) + "\t"
for i in (range(len(graph.nodes))):
    task26 += "\n" + str(i) + "\t"
    for j in range(len(graph.edges_list)):
        if graph.edges_list[j][0] == i and graph.edges_list[j][1] != i:
            task26 += "1\t"
        elif graph.edges_list[j][1] == i and graph.edges_list[j][0] != i:
            task26 += "-1\t"
        else:
            task26 += "0\t"
task26 += "\n\n"
save_to_file(task26, path, '26')

#27
