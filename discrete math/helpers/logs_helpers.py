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
