from my_graph import Graph


def get_distance_between_pubs(name1, name2):
    if name1 == name2:
        return [len(name1)]
    distances = set()
    if name1.find('Bar') != -1 and name2.find('Bar') != -1:
        distances.add(1)
    if name1.find('Pub') != -1 and name2.find('Pub') != -1:
        distances.add(1)
    if len(name1) == len(name2):
        distances.add(len(name1))
    elif len(name1) < len(name2):
        distances.add((len(name2) - len(name1)) * 2)
    else:
        distances.add(len(name1) - len(name2))
    distances = [e for e in distances]
    return distances


def get_graph_for_topic_1():
    nodes = ['Signal Bar', 'The Drinkery', 'Barrel Pub', 'BarDuck', 'Varvar Bar',
             'Beer.Live', 'Mugnum94', 'Pravda Beer Theatre', 'OLD BAR', 'Pilsner Bar',
             'Black Bull Bar', 'MumuBar', 'CRAFT vs PUB', 'Steam Pub', 'Porter Pub']
    distances = []
    for i in range(len(nodes)):
        distances.append([])
        for j in range(len(nodes)):
            distances[-1].append(get_distance_between_pubs(nodes[i], nodes[j]))
    return Graph(nodes, distances)
