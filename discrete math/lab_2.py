import random
import igraph
from igraph import *
print(igraph.__version__)

DEBUG1 = False
DEBUG2 = False
DEBUG3 = False

u_to_ind = {}

def print_graph(names, connections, folder = '/home/san/Documents/university/babakov/lab2/testing/', filename = 'test0'):
    g = Graph().as_directed()
    g.add_vertices(len(names))
    # g.vs['label'] = names
    for i in range(len(connections)):
        for j in range(len(connections[0])):
            if connections[i][j]:
                g.add_edges([(i, j)])
    arrow_size = [1 for e in g. get_edgelist()]
    # print(arrow_size)
    plot(g, folder+filename+'.pdf', layout=g.layout('fr'), vertex_label=[str(u_to_ind[e]) for e in names], edge_arrow_size=arrow_size, arrow_size=arrow_size, edge_arrow_width=arrow_size)
def print_graph2(names1, names2, connections, folder = '/home/san/Documents/university/babakov/lab2/testing/', filename = 'test0'):
    g = Graph().as_directed()
    g.add_vertices(len(names1) + len(names2))
    # g.vs['label'] = names
    for i in range(len(connections)):
        for j in range(len(connections[0])):
            if connections[i][j]:
                g.add_edges([(i, j + len(names1))])
    arrow_size = [1 for e in g. get_edgelist()]
    # print(arrow_size)
    plot(g, folder+filename+'.pdf', layout=g.layout('fr'), vertex_label=[str(u_to_ind[e]) for e in names1+names2], edge_arrow_size=arrow_size, arrow_size=arrow_size, edge_arrow_width=arrow_size)

if DEBUG1:
    print_graph(['a', 'b', 'c'], [[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    t1 = ['1.' + str(e) for e in range(5)]
    t2 = ['2.' + str(e) for e in range(6)]
    connections = []
    for e in range(5):
        connections.append([])
        for k in range(6):
            if(e+k < 8):
                connections[e].append(True)
            else:
                connections[e].append(False)
    print_graph2(t1, t2, connections)

def get_table(names1, names2, connections):
    tab = max([len(e) for e in names1]) + 3
    shift = 3
    starts = []
    ends = []
    sm = tab+shift
    for e in names2:
        starts.append(sm)
        sm += len(e)
        ends.append(sm)
        sm += shift
    positions = []
    for start, end in zip(starts, ends):
        positions.append(int((start + end)/2))
    sm -= shift
    result = ' ' * tab
    for e in names2:
        result += ' ' * shift
        result += e
    for e, i in zip(names1, range(len(names1))):
        result += '\n'
        result += e + ' ' * (tab - len(e))
        for e2, j in zip(names2, range(len(names2))):
            result += ' ' * shift
            pos = int((len(e2)+1) / 2)
            result += ' ' * (pos - 1)
            result += '1' if connections[i][j] else '0'
            result += ' ' * (len(e2) - pos) if pos!=0 else ''
    # for i in range(len(names1)):
    #     for j in range(len(names2)):
    #         result[(sm+1) * (j+1) + positions[i]] = '1' if connections[i][j] else '0'
    return result

def get_pairs(names1, names2, connections):
    pairs = []
    for i in range(len(names1)):
        for j in range(len(names2)):
            if connections[i][j]:
                pairs.append((names1[i], names2[j]))
    return pairs

def save_to_file2(names1, names2, connections, description, folder_name = 'testing', pref='', singular=False):
    path = '/home/san/Documents/university/babakov/lab2/' + folder_name + '/'
    if singular:
        print_graph(names1, connections, path, pref+'graph')
    else:
        print_graph2(names1, names2, connections, path, pref + 'graph')
    pairs = get_pairs(names1, names2, connections)
    with open(path + pref + 'pairs.txt', 'w+') as f:
        f.write(str(pairs))
    table = get_table(names1, names2, connections)
    with open(path + pref + 'table.txt', 'w+') as f:
        f.write(table)
    with open(path + pref + 'description.txt', 'w+') as f:
        f.write(description)


if DEBUG2:
    print_graph(['a', 'b', 'c'], [[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    t1 = ['1.' + str(e) for e in range(5)]
    t2 = ['2.' + str(e) for e in range(6)]
    connections = []
    for e in range(5):
        connections.append([])
        for k in range(6):
            if(e+k < 8):
                connections[e].append(True)
            else:
                connections[e].append(False)
    save_to_file2(t1, t2, connections)

vowels = set()
a = ord('а')
# z1 = ord('я')+1
z1 = ord('а')+11
hui = 0
while a<z1:
    vowels.add(chr(a))
    vowels.add(chr(ord('я') - (a - ord('а'))))
    a += 1
print(vowels)

def str_to_int(name):
    name = name.replace(' ', '').replace('-', '').lower()
    # vowels = {'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н'}
    val = 0
    for e in name:
        val *= 2
        if e in vowels:
            val += 1
    return val

a = ['Велосипед', 'Самокат', 'Роликовые коньки', 'Уницикл', 'Скейтборд', 'Галера', 'Каяка', 'Катамаран']
b = ['Трамвай', 'Троллейбус', 'Поезд', 'Электричка', 'Самолёт', 'Баржа', 'Маршутное такси', 'Автобус']
c = ['Галера', 'Каяка', 'Катамаран', 'Баржа', 'Яхта', 'Гидроцикл', 'Каравелла', 'Подводная лодка']
d = ['Галера', 'Самолёт', 'Подводная лодка', 'БТР', 'Танк', 'Командно-штабная машина', 'Боевая машина огневой поддержки']
u = list(set(a+b+c+d))
u_int = [str_to_int(e) for e in u]
e_to_int = {}
for e in u:
    e_to_int[e] = str_to_int(e)
int_to_e = {}
for k, v in e_to_int.items():
    int_to_e[v] = k
int_to_ind = {}
for i, val in enumerate(sorted(int_to_e.keys())):
    int_to_ind[val] = i
ind_to_int = {}
for k, v in int_to_ind.items():
    ind_to_int[v] = k
for i in range(len(u)):
    u[i] = int_to_e[ind_to_int[i]]
u_int = sorted(u_int)
for i, e in enumerate(u):
    u_to_ind[e] = i
for i in range(len(u)):
    if u_int[i] != str_to_int(u[i]):
        print('hui')
a_int = [str_to_int(e) for e in a]
b_int = [str_to_int(e) for e in b]
c_int = [str_to_int(e) for e in c]
d_int = [str_to_int(e) for e in d]

if DEBUG3:
    cnt = {}
    for e in u:
        val = str_to_int(e)
        if val not in cnt:
            cnt[val] = 0
        cnt[val] += 1
    print('bad:')
    print(sum([1 for e in cnt.values() if e > 1]))
    bad_keys = []
    for k, v in cnt.items():
        if v>1:
            bad_keys.append(k)
    print(bad_keys)
    bad_names = []
    for e in u:
        if(str_to_int(e) in bad_keys):
            bad_names.append(e)
    # bad_names = [e for e in u if (str_to_int(e) in bad_keys)]
    print(bad_names)


def create_connections(ar1, ar2, my_fn):
    res = []
    for e1 in ar1:
        res.append([])
        for e2 in ar2:
            if my_fn(e1, e2):
                res[-1].append(True)
            else:
                res[-1].append(False)
    return res

def create_connections_arr(ar1, ar2, my_fn):
    res = []
    for e1 in ar1:
        res.append(my_fn(e1, ar2))
    return res

description1 = "конгруентный элемент по модулю 7"
fn = lambda x, y: x % 7 == y % 7
connections = create_connections(a_int, b_int, fn)
save_to_file2(a, b, connections, description1, '1')

description2 = "сумма конгруэнтна 5 по модулю 8"
fn = lambda x, y: (x+y) %8 == 5
connections = create_connections(a_int, c_int, fn)
save_to_file2(a, c, connections, description2, '2')

description3 = "разность конгруентна 2 по модулю 3"
fn = lambda x, y: ((x%3) - (y%3) + 3) % 3 == 2
connections = create_connections(b_int, d_int, fn)
save_to_file2(b, d, connections, description3, '3')

description4 = "квадрат первого без значения второго кратен 6"
fn = lambda x, y: abs(x*x - y) % 6 == 0
connections = create_connections(c_int, b_int, fn)
save_to_file2(c, b, connections, description4, '4')

description5 = "ближайший элемент"
fn = lambda x, ar: [True if (abs(x-e) == min([abs(x-k) for k in ar])) else False for e in ar]
connections = create_connections_arr(a_int, b_int, fn)
save_to_file2(a, b, connections, description5, '5', pref='ab.')
connections = create_connections_arr(b_int, c_int, fn)
save_to_file2(b, c, connections, description5, '5', pref='bc.')
connections = create_connections_arr(c_int, d_int, fn)
save_to_file2(c, d, connections, description5, '5', pref='cd.')

description6 = "минимальный ближайший элемент"
# fn = lambda x, ar: [True if (abs(x-e) == min([abs(x-k) for k in ar])) else False for e in ar]
fn = lambda x, ar: [True if (l == min([k for k in ar if (abs(x-k) == min([abs(x-e) for e in ar]))])) else False for l in ar]
# def create_6_connections(ar1, ar2):
#     name_to_index1 = {}
#     name_to_index2 = {}
#     for i in range(len(ar1)):

connections = create_connections_arr(a_int, b_int, fn)
save_to_file2(a, b, connections, description6, '6', pref='ab.')
connections = create_connections_arr(b_int, c_int, fn)
save_to_file2(b, c, connections, description6, '6', pref='bc.')
connections = create_connections_arr(c_int, d_int, fn)
save_to_file2(c, d, connections, description6, '6', pref='cd.')

def get_sorted_connections_to_next(my_ar):
    good = {}
    sorted_ar = sorted(my_ar)
    for i in range(len(my_ar)):
        good[sorted_ar[i]] = sorted_ar[(i+1)%len(my_ar)]
    res = []
    for e in my_ar:
        res.append([])
        for e2 in my_ar:
            if e2 == good[e]:
                res[-1].append(True)
            else:
                res[-1].append(False)
    return res

description71 = "xQx для любого x из заданного множества"
description72 = "следующий элемент в отсортированном списке"
all_true_fn = lambda x, y:True
connections = create_connections(a_int, a_int, all_true_fn)
save_to_file2(a, a, connections, description71, '7', pref='all.', singular=True)
connections = get_sorted_connections_to_next(a_int)
save_to_file2(a, a, connections, description72, '7', pref='next.', singular=True)

connections = create_connections(b_int, b_int, all_true_fn)
save_to_file2(b, b, connections, description71, '8', pref='all.', singular=True)
connections = get_sorted_connections_to_next(b_int)
save_to_file2(b, b, connections, description72, '8', pref='next.', singular=True)

connections = create_connections(c_int, c_int, all_true_fn)
save_to_file2(c, c, connections, description71, '9', pref='all.', singular=True)
connections = get_sorted_connections_to_next(c_int)
save_to_file2(c, c, connections, description72, '9', pref='next.', singular=True)

connections = create_connections(d_int, d_int, all_true_fn)
save_to_file2(d, d, connections, description71, '10', pref='all.', singular=True)
connections = get_sorted_connections_to_next(d_int)
save_to_file2(d, d, connections, description72, '10', pref='next.', singular=True)

connections = create_connections(u_int, u_int, all_true_fn)
save_to_file2(u, u, connections, description71, '11', pref='all.', singular=True)
connections = get_sorted_connections_to_next(u_int)
save_to_file2(u, u, connections, description72, '11', pref='next.', singular=True)
