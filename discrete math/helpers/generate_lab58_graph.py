from my_graph import LabGraph


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


if __name__ == "__main__":
    get_graph_for_topic_1(('/home/san/Documents/university/babakov/lab5/test/', 'topic1_source'))


