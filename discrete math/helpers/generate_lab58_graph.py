from my_graph import LabGraph
from my_graph import add_edges_to_table


def get_distance_between_pubs(name1, name2):
    if name1 == name2:
        return [len(name1)]
    distances = set()
    if ('bar' in name1.lower() and 'bar' in name2.lower()) or \
            ('pub' in name1.lower() and 'pub' in name2.lower()):
        distances.add(1)
    if len(name1) == len(name2):
        distances.add(len(name1))
    elif len(name1) < len(name2):
        distances.add((len(name2) - len(name1)) * 2)
    else:
        distances.add(len(name1) - len(name2))
    return list(distances)


def make_distance_between_nodes(nodes):
    table = []  # make empty table
    for i in range(len(nodes)):
        table.append([])
        for j in range(len(nodes)):
            table[-1].append(None)  # если между вершинами отсутствуют рёбра, соответствующее значение - None, а не пустой массив
    add_edges_to_table(table, [(0, 0, 1), (1, 0, 2), (0, 1, 3), (5, 5, 4), (0, 2, 5), (0, 3, 6), (0, 4, 7)])
    add_edges_to_table(table, [(7, 8, 8), (7, 9, 9), (7, 10, 10), (7, 10, 11)])
    add_edges_to_table(table, [(1, 7, 12), (10, 6, 13), (6, 14, 14), (14, 2, 15)])
    add_edges_to_table(table, [(2, 10, 16), (10, 2, 17), (10, 14, 18), (14, 10, 19)])
    add_edges_to_table(table, [(2, 6, 20), (6, 2, 21), (1, 9, 22), (9, 1, 23)])
    # рёбра графа имеют тип tuple, а не list. Разница в том, что tuple immutable, а list - mutable
    return table


def get_graph_for_topic_1(test_save=None):
    nodes = ['Signal Bar', 'The Drinkery', 'Barrel Pub', 'BarDuck', 'Varvar Bar',
             'Beer.Live', 'Mugnum94', 'Pravda Beer Theatre', 'OLD BAR', 'Pilsner Bar',
             'Black Bull Bar', 'MumuBar', 'CRAFT vs PUB', 'Steam Pub', 'Porter Pub']
    distances = []
    for i in range(len(nodes)):
        distances.append([])
        for j in range(len(nodes)):
            distances[-1].append(get_distance_between_pubs(nodes[i], nodes[j]))
    graph = LabGraph(nodes, distances)
    if test_save is not None:
        graph.save_plot(test_save[0], test_save[1])
    return graph


# одна функция возвращает 1 граф. можно сделать, чтобы функция возвращала граф относительно входящих аргументов
# смысл функции get_graph_for_topic_1 в том, что она возвращает мой исходный граф для первого варианта
# в рамках ветки lab_5 не вижу смысла менять смысл этой функции
def get_graph_for_topic_not_1(test_save=None):
    nodes = ['Signal Bar', 'The Drinkery', 'Barrel Pub', 'BarDuck', 'Varvar Bar',
             'Beer.Live', 'Mugnum94', 'Pravda Beer Theatre', 'OLD BAR', 'Pilsner Bar',
             'Black Bull Bar', 'MumuBar', 'CRAFT vs PUB', 'Steam Pub', 'Porter Pub']
    distances = make_distance_between_nodes(nodes)
    graph = LabGraph(nodes, distances)
    if test_save is not None:
        graph.save_plot(test_save[0], test_save[1])
    return graph


if __name__ == "__main__":
    get_graph_for_topic_1(('/home/san/Documents/university/babakov/lab5/test/', 'topic1_source'))
    get_graph_for_topic_1(('D:/Education/DonNU/Discrete math/', 'topic1_source'))



