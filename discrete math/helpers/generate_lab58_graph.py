from my_graph import LabGraph
from my_graph import add_edges_to_table
import random


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


def make_graph_manually():
    nodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    table = []
    for i in range(len(nodes)):
        table.append([])
        for j in range(len(nodes)):
            table[-1].append(None)
    add_edges_to_table(table, [(0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 4, 4), (4, 0, 5), (2, 5, 6), (2, 5, 7),
                               (5, 2, 8), (5, 6, 9), (6, 8, 10), (6, 7, 11), (7, 8, 12), (5, 7, 13), (8, 11, 14),
                               (10, 11, 15), (7, 10, 16), (7, 10, 17), (9, 10, 18), (5, 9, 19), (6, 5, 20)])
    # рёбра графа имеют тип tuple, а не list. Разница в том, что tuple immutable, а list - mutable
    return LabGraph(nodes, table)


# TODO planar if possible
# TODO 25 вершин, 100+ рёбер
def get_graph_for_topic_1(test_save=None):
    nodes = ['Signal Bar', 'The Drinkery', 'Barrel Pub', 'BarDuck', 'Varvar Bar',
             'Beer.Live', 'Mugnum94', 'Pravda Beer Theatre', 'OLD BAR', 'Pilsner Bar',
             'Black Bull Bar', 'MumuBar', 'CRAFT vs PUB', 'Steam Pub', 'Porter Pub']
    distances = []
    for i in range(len(nodes)):
        distances.append([])
        for j in range(len(nodes)):
            if random.random() < 0.15:
                distances[-1].append(get_distance_between_pubs(nodes[i], nodes[j]))
            else:
                distances[-1].append(None)
    graph = LabGraph(nodes, distances)
    if test_save is not None:
        graph.save_plot(test_save[0], test_save[1])
    return graph


# одна функция возвращает 1 граф. можно сделать, чтобы функция возвращала граф относительно входящих аргументов
# смысл функции get_graph_for_topic_1 в том, что она возвращает мой исходный граф для первого варианта
# в рамках ветки lab_5 не вижу смысла менять смысл этой функции
def get_graph_for_topic_not_1(test_save=None):
    graph = make_graph_manually()
    if test_save is not None:
        graph.save_plot(test_save[0], test_save[1])
    return graph


if __name__ == "__main__":
    get_graph_for_topic_1(('/home/san/Documents/university/babakov/lab5/test/', 'topic1_source'))
    # get_graph_for_topic_1(('D:/Education/DonNU/Discrete math/', 'topic1_source'))



