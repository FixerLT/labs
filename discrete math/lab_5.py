import random
from generate_lab58_graph import get_graph_for_topic_not_1
from docx_helper import Reporter
from lab_7 import hamilton_solve
from lab_6 import bfs_solve

reporter = Reporter()

def save_to_file(report, path, file_name):
    print(report)
    return # TODO remove this debug statement fo really save reports
    with open(path + file_name + '.txt') as f:
        f.write(report)


def apply_str_stub_to_array(str_stub, arr, step='\n'):
    return ''.join(str_stub.format(*e) + step for e in arr)


#if log_folder is not None:
    #graph.save_plot(log_folder, 'source_graph')
#reporter.add_page(header='Задание №1', image_path=log_folder + 'source_graph.png', comment=)


def task1_solve(graph, log_folder=None):
    task1 = 'Вершины: {}\nМощность: {}\n\nРёбра: {}\nМощность: {}\n\nДуги: {}\nМощность: {}\n\n'  # TODO distinguish Рёбра and Дуги
    task1 = task1.format(str(graph.nodes), len(graph.nodes), graph.edges_list, len(graph.edges_list), graph.edges_list,
                         len(graph.edges_list))
    if log_folder is not None:
        save_to_file(task1, log_folder, '1')
        reporter.add_page(header='Задание №1', image_path=None, comment=task1)

def task2_solve(graph, log_folder=None):
    adjacent_nodes = [len(graph.get_neighbours(i)) for i in range(len(graph.nodes))]  # количество соседей для каждой i
    max_neighbours = max(adjacent_nodes)
    nodes_with_max_neighbours = list(filter((lambda e: e[1] == max_neighbours), enumerate(adjacent_nodes)))

    task2 = 'Вершина №{} {} смежных вершин'
    task2 = apply_str_stub_to_array(task2, nodes_with_max_neighbours)
    task2 += '\n'
    if log_folder is not None:
        save_to_file(task2, log_folder, '2')
        reporter.add_page(header='Задание №2', image_path=None, comment=task2)

def task3_solve(graph, log_folder=None):
    degrees = graph.get_node_degrees(orientated=True)
    max_degree, min_degree = max(degrees), min(degrees)
    max_degree_nodes = [i for i, e in enumerate(degrees) if e == max_degree]
    min_degree_nodes = [i for i, e in enumerate(degrees) if e == min_degree]
    task3_max = 'Вершина №{} имеет максимальную степень {}'
    task3_min = 'Вершина №{} имеет минимальную степень {}'
    task3_max = apply_str_stub_to_array(task3_max, [(e, max_degree) for e in max_degree_nodes])
    task3_min = apply_str_stub_to_array(task3_min, [(e, min_degree) for e in min_degree_nodes])
    task3 = task3_min + '\n' + task3_max + '\n'
    if log_folder is not None:
        save_to_file(task3, log_folder, '3')
        reporter.add_page(header='Задание №3', image_path=None, comment=task3)

def task4_solve(graph, log_folder=None):
    degrees = graph.get_node_degrees(orientated=True)
    isoted_nodes = [i for i, e in enumerate(degrees) if e == 0]
    pendant_nodes = [i for i, e in enumerate(degrees) if e == 1]
    task4 = 'Количество изолированных вершин: {}\nКоличество концевых вершин: {}\n\n'
    task4 = task4.format(str(len(isoted_nodes)), str(len(pendant_nodes)))
    if log_folder is not None:
        save_to_file(task4, log_folder, '4')
        reporter.add_page(header='Задание №4', image_path=None, comment=task4)

def task5_solve(graph, log_folder=None):
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
    if log_folder is not None:
        save_to_file(task5, log_folder, '5')
        reporter.add_page(header='Задание №5', image_path=None, comment=task5)

def task6_solve(graph, log_folder=None):
    loop_count = len(
        [i for i in range(len(graph.nodes)) if graph.edges[i][i] is not None and len(graph.edges[i][i]) > 0])
    task6 = 'Количество петель: {}\n\n'
    task6 = task6.format(str(loop_count))
    if log_folder is not None:
        save_to_file(task6, log_folder, '6')
        reporter.add_page(header='Задание №6', image_path=None, comment=task6)

def task7_solve(graph, log_folder=None):
    loop_count = len(
        [i for i in range(len(graph.nodes)) if graph.edges[i][i] is not None and len(graph.edges[i][i]) > 0])
    max_degree = max([max([len(e) for e in row if e is not None]) for row in graph.edges])
    if max_degree > 1:
        if loop_count > 0:
            s = "псевдографом"
        else:
            s = "мультиграфом"
    else:
        s = 'простым'
    task7 = 'Граф является {}\n\n'
    task7 = task7.format(s)
    if log_folder is not None:
        save_to_file(task7, log_folder, '7')
        reporter.add_page(header='Задание №7', image_path=None, comment=task7)


def make_beautiful_path(path):
    beautiful_path = ""
    for i in path:
        beautiful_path += str(i) + " -> "
    return beautiful_path[:-3]


def tasks_8_10_12(graph):
    paths = []
    nodes_list = [i for i in range(len(graph.nodes))]
    random.shuffle(nodes_list)
    i = 0
    while len(paths) < 3:
        d, path = bfs_solve(graph, nodes_list[i])
        max_path = []
        for p in path:
            if p is not None and len(p) > len(max_path):
                max_path = p
        path = max_path
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
            path_len += graph.edges[i[j - 1]][i[j]][0]
        result += "\nДлина: " + str(path_len) + "\n"
    return result


def task8_solve(graph, log_folder=None):
    task8 = tasks_8_10_12(graph)
    if log_folder is not None:
        save_to_file(task8, log_folder, '8')
        reporter.add_page(header='Задание №8', image_path=None, comment=task8)


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

def tasks_9_11_13(graph):
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


def task9_solve(graph, log_folder=None):
    task9 = tasks_9_11_13(graph)  # если есть 3 пути, то всё ок, иначе нужно ещё какую-то функцию придумать,
                            # так как контур, при заданых условиях должен быть практически всегда
    if log_folder is not None:
        save_to_file(task9, log_folder, '9')
        reporter.add_page(header='Задание №9', image_path=None, comment=task9)

def task10_solve(graph, log_folder=None):
    task10 = tasks_8_10_12(graph)
    if log_folder is not None:
        save_to_file(task10, log_folder, '10')
        reporter.add_page(header='Задание №10', image_path=None, comment=task10)

def task11_solve(graph, log_folder=None):
    task11 = tasks_9_11_13(graph) #по идее данное решение должно всегда давать правильный ответ(контрпример придумать не могу)
    if log_folder is not None:
        save_to_file(task11, log_folder, '11')
        reporter.add_page(header='Задание №11', image_path=None, comment=task11)

def task12_solve(graph, log_folder=None):
    task12 = tasks_8_10_12(graph)
    if log_folder is not None:
        save_to_file(task12, log_folder, '12')
        reporter.add_page(header='Задание №12', image_path=None, comment=task12)

def task13_solve(graph, log_folder=None):
    task13 = tasks_9_11_13()
    if log_folder is not None:
        save_to_file(task13, log_folder, '13')
        reporter.add_page(header='Задание №13', image_path=None, comment=task13)


#14-17


def task14_solve(graph, log_folder=None): #TODO
    type, task_path = hamilton_solve(graph.copy(), log_folder)
    if task_path is None:
        task14 = "Гамильтонова пути нет\n\n"
    else:
        task14 = "Гамильтонов путь: " + task_path + "\n\n"
    if log_folder is not None:
        save_to_file(task14, log_folder, '14')
        reporter.add_page(header='Задание №14', image_path=None, comment=task14)


def task15_solve(graph, log_folder=None):
    type, task_path = hamilton_solve(graph.copy(), log_folder)
    if task_path is None:
        task14 = "Гамильтонова пути нет\n\n"
        task15 = "Гамильтонова контура нет\n\n"
    else:
        task14 = "Гамильтонов путь: \n\n"
        if type == "hamilton":
            task15 = "Гамильтонов контур: \n\n"
        else:
            task15 = "Гамильтонова контура нет\n\n"
    if log_folder is not None:
        save_to_file(task15, log_folder, '15')
        reporter.add_page(header='Задание №15', image_path=None, comment=task15)





def task18_solve(graph, log_folder=None):
    is_symmetric = True
    for i in range(len(graph.nodes)):
        for j in range(i, len(graph.nodes)):
            if graph.edges[i][j] is not None:
                if not (graph.edges[j][i] is not None and len(graph.edges[i][j]) == len(graph.edges[j][i])):
                    is_symmetric = False
                    i = len(graph.edges) + 1  # что бы выйти из первого цикла тоже
                    break
    if is_symmetric:
        s = "симметричным"
    else:
        s = "антисимметричным"
    task18 = 'Граф является {}\n\n'
    task18 = task18.format(s)
    if log_folder is not None:
        save_to_file(task18, log_folder, '18')
        reporter.add_page(header='Задание №18', image_path=None, comment=task18)



def component_finder(start_node, visited, graph):
    visited[start_node] = True
    for i in range(len(graph.nodes)):
        if not visited[i] and graph.edges[start_node][i] is not None:
            component_finder(i, visited)

def task19_solve(graph, log_folder=None):
    components = 0
    visited = [False] * len(graph.nodes)
    for i in range(len(graph.nodes)):
        if not visited[i]:
            component_finder(i, visited, graph)
            components += 1
    if components == 1:
        task19 = "Граф связный\n\n"
    else:
        task19 = "Граф не связный, количество компонент связности: " + str(components) + "\n\n"
    if log_folder is not None:
        save_to_file(task19, log_folder, '19')
        reporter.add_page(header='Задание №19', image_path=None, comment=task19)


#20



"""
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
"""

def solve():
    path = "D:/Education/DonNU/Discrete math/"  # '/home/san/Documents/university/babakov/lab5/'
    graph = get_graph_for_topic_not_1((path, 'topic_1_src'))
    # log_folder = "D:/Education/DonNU/Discrete math/"


    task1_solve(graph, path)
    task2_solve(graph, path)
    task3_solve(graph, path)
    task4_solve(graph, path)
    #task5_solve(graph, path)
    task6_solve(graph, path)
    #task7_solve(graph, path)
    task8_solve(graph, path)
    task9_solve(graph, path)
    task10_solve(graph, path)
    task11_solve(graph, path)
    task12_solve(graph, path)
    #task13_solve(graph, path)
    task18_solve(graph, path)
    #task19_solve(graph, path)

    reporter.save_report(path=path, report_name='lab5_report', create_new_page=False)

solve()

"""
def task_8_10_12_solve(graph, log_folder=None):
    task6 = 'Количество петель: {}\n\n'
    if log_folder is not None:
        save_to_file(task6, log_folder, '6')
        reporter.add_page(header='Задание №6', image_path=None, comment=task6)
"""