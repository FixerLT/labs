def get_log_for_distance(node_name, distance, unreachable_value=None):
    distance_template = 'Расстояние до вершины {} равно {}\n'
    unreachable_template = 'Вершина {} недостижима\n'
    if distance == unreachable_value:
        return unreachable_template.format(node_name)
    else:
        return distance_template.format(node_name, distance)


def get_log_for_path(path):
    if path is None:
        return 'Пути нет\n'
    path_string = str(path[0])
    for e in path[1:]:
        path_string += ' -> ' + str(e)
    return 'Путь: ' + path_string + '\n'


def get_log_for_edge(edge, include_weight=False):
    log = '{} => {}'
    log_weight = '{} => {} (вес {})'
    return log.format(edge[0], edge[1]) if not include_weight else log_weight.format(edge[0], edge[1], edge[2])

