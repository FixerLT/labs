
def result_to_file(index, data, arr_logs=None):
    with open("/home/san/Documents/university/babakov/lab1/" + str(index), 'w') as f:
        for i, row in enumerate(data):
            f.write(str(row) + '\n')
            if arr_logs is not None and len(arr_logs) > i:
                for e in arr_logs[i]:
                    f.write(e + '\n')


a = ['Велосипед', 'Самокат', 'Роликовые коньки', 'Уницикл', 'Скейтборд', 'Галера', 'Каяка', 'Катамаран']
b = ['Трамвай', 'Троллейбус', 'Поезд', 'Электричка', 'Самолёт', 'Баржа', 'Маршутное такси', 'Автобус']
c = ['Галера', 'Каяка', 'Катамаран', 'Баржа', 'Яхта', 'Гидроцикл', 'Каравелла', 'Подводная лодка']
d = ['Галера', 'Самолёт', 'Подводная лодка', 'БТР', 'Танк', 'Командно-штабная машина', 'Боевая машина огневой поддержки']
sets = [a, b, c, d]
a_property = 'Транспорт, приводимый в движение человеческой силой'
b_property = 'Общественный транспорт'
c_property = 'Морской транспорт'
d_property = 'Транспорт, который принимает участие в военных действиях'
u = set(a+b+c+d)
u_ordered = ['БТР', 'Танк', 'Поезд', 'Яхта', 'Трамвай', 'Баржа', 'Троллейбус', 'Уницикл', 'Каяка', 'Самолёт', 'Самокат',
             'Галера', 'Автобус', 'Скейтборд', 'Велосипед', 'Катамаран', 'Каравелла', 'Гидроцикл', 'Электричка',
             'Подводная лодка', 'Роликовые коньки', 'Маршутное такси', 'Командно-штабная машина',
             'Боевая машина огневой поддержки']
u_i = {}
for i, e in enumerate(u_ordered):
    u_i[e] = i


def to_str(my_set):
    res = [u_i[e] for e in my_set]
    return str(sorted(res))


print(u)

op_cnt = [1]
arr_logs = []
logs = []


def nt(x):  # not
    log = str(op_cnt[0]) + ') '
    log += 'not' + to_str(x) + ' = '
    op_cnt[0] += 1
    res = []
    for e in u:
        if e not in x:
            res.append(e)
    log += to_str(set(res))
    logs.append(log)
    return set(res)


def un(*args):  # unite
    log = str(op_cnt[0]) + ') '
    op_cnt[0] += 1
    log += to_str(args[0])
    for i in range(1, len(args)):
        log += ' u ' + to_str(args[i])
    log += ' = '
    res = []
    for arr in args:
        for e in arr:
            res.append(e)
    log += to_str(set(res))
    logs.append(log)
    return set(res)


def its(*args):  # intersect
    log = str(op_cnt[0]) + ') '
    op_cnt[0] += 1
    log += to_str(args[0])
    for i in range(1, len(args)):
        log += ' n ' + to_str(args[i])
    log += ' = '
    res = set()
    res2 = set()
    if len(args) > 0:
        for e in args[0]:
            res.add(e)
            res2.add(e)
    for i in range(1, len(args)):
        for e in res:
            if e not in args[i] and e in res2:
                res2.remove(e)
    log += to_str(res2)
    logs.append(log)
    return res2


def cmp(x, *args):  # complement
    log = str(op_cnt[0]) + ') '
    op_cnt[0] += 1
    log += to_str(x)
    for i in range(len(args)):
        log += ' \ ' + to_str(args[i])
    log += ' = '
    res = set()
    for e in x:
        res.add(e)
        for y in args:
            if e in y:
                res.remove(e)
                break
    log += to_str(set(res))
    logs.append(log)
    return set(res)


def sd_src(x, y):
    return cmp(un(x, y), its(x, y))


def sd(*args):  # symmetrical difference
    log = str(op_cnt[0]) + ') '
    op_cnt[0] += 1
    log += to_str(args[0])
    for i in range(1, len(args)):
        log += ' ^ ' + to_str(args[i])
    log += ' = '
    res = set()
    for e in args:
        res = sd_src(res, e)
    return res


ab = its(a, b)
ac = its(a, c)
ad = its(a, d)
bc = its(b, c)
bd = its(b, d)
cd = its(c, d)
result_to_file(1, ['Транспорт', u])
result_to_file(2, ['A', a_property, a, '|A| = ' + str(len(a)), 'B', b_property, b, '|B| = ' + str(len(b)),
                   'C', c_property, c, '|C| = ' + str(len(c)), 'D', d_property, d, '|D| = ' + str(len(d))])
result_to_file(3, [nt(a), nt(b), nt(c), nt(d)])
res = []
for i in range(4):
    j = i+1
    while j < 4:
        res.append(un(sets[i], sets[j]))
        j += 1
res += [un(d, b), un(d, a), un(c, b), un(b, c), un(c, a)]
result_to_file(4, res)
result_to_file(5, [un(a, b, c), un(d, a, c), un(b, c, d), un(a, b, c, d)])
res = [its(d, a), its(d, b), its(d, c), its(c, b), its(c, a), its(b, a), its(b, d), its(a, c), its(a, d), its(a, b), its(b, c)]
result_to_file(6, res)
result_to_file(7, [its(c, b, c), its(d, a, b), its(a, c, d), its(a, b, c, d)])
res = []
for i in range(3):
    res.append(its(sets[i], nt(sets[i+1])))
res.append(its(nt(a), nt(b), nt(c)))
res.append(its(nt(d), nt(b), nt(c)))
res.append(its(nt(d), nt(b), nt(c), nt(a)))
result_to_file(8, res)
result_to_file(9, [cmp(a, nt(b)), cmp(c, nt(d)), cmp(d, nt(a)), cmp(b, a), cmp(nt(d), c)])
result_to_file(10, [sd(a, b), sd(b, c), sd(c, d), sd(a, b, c), sd(b, c, d), sd(a, b, c, d)])

res = []
logs = []
arr_logs = []
res.append(un(a, its(b, c), d))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(its(a, b), its(c, d)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(nt(a), its(b, nt(c)), d))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(its(a, nt(b)), its(c, nt(d))))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(11, res, arr_logs)

res = []
logs = []
arr_logs = []
res.append(un(its(a, un(d, its(b, c))), its(d, un(a, its(b, c)))))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(a, un(its(a, c), un(b, its(d, un(d, its(b, c)))))))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(un(c, its(a, b)), its(c, un(d, b, its(d, a)))))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(12, res, arr_logs)

res = []
logs = []
arr_logs = []
res.append(un(cmp(cmp(a, its(b, d)), c), cmp(cmp(its(a, c), its(b, d)), its(a, c))))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(a, cmp(un(cmp(d, a), c), its(its(a, b), d), its(b, c), d)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(13, res, arr_logs)

res = []
logs = []
arr_logs = []
tmp = cmp(a, its(b, un(cmp(d, c), its(a, c))), d)
tmp = un(tmp, its(a, cmp(b, c)))
res.append(tmp)
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
tmp = sd(a, cmp(a, its(b, d), c))
tmp = its(tmp, cmp(c, its(b, d)))
tmp = cmp(tmp, its(a, c))
res.append(tmp)
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(14, res, arr_logs)

res = []
logs = []
arr_logs = []
tmp1 = cmp(nt(cmp(a, its(b, d))), c)
tmp2 = nt(cmp(c, its(b, d)))
tmp2 = nt(cmp(its(a, tmp2), c))
tmp2 = its(tmp2, a)
res.append(un(tmp1, tmp2))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0

tmp1 = nt(cmp(d, a))
tmp2 = nt(cmp(c, sd(b ,a)))
tmp2 = nt(its(tmp2, d))
tmp3 = nt(un(a, cmp(c, d)))
tmp3 = nt(its(b, tmp3))
tmp = cmp(un(tmp1, tmp2), tmp3)
res.append(tmp)
arr_logs.append(logs)
logs = []
op_cnt[0] = 0

tmp = nt(un(a, b))
tmp = nt(un(tmp, c))
tmp = nt(un(tmp, d))
tmp = nt(its(tmp, a))
tmp = nt(its(tmp, b))
tmp = nt(its(tmp, c))
tmp = nt(its(tmp, d))
res.append(tmp)
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(15, res, arr_logs)

res = []
logs = []
arr_logs = []
tmp1 = nt(cmp(a, b))
tmp2 = un(nt(c), un(a, sd(d, b)))
tmp1 = its(tmp1, nt(tmp2))
tmp2 = cmp(d, its(b, nt(a), sd(c, b), d))
tmp2 = nt(cmp(c, tmp2))
tmp1 = its(tmp1, tmp2)
tmp1 = cmp(tmp1, its(a, c))
tmp1 = nt(tmp1)
res.append(tmp1)
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(16, res, arr_logs)

res = []
logs = []
arr_logs = []
res.append(un(a, un(b, c)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(un(a, b), c))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(a, its(b, c)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(its(a, b), c))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(a, its(b, c)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(un(a, b), un(b, c)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(a, un(b, c)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(its(a, b), its(a, c)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(17, res, arr_logs)

res = []
logs = []
arr_logs = []
res.append(un(a, its(nt(a), b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(a, b))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(a, un(nt(a), b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(a, b))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(nt(un(a, b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(nt(a), nt(b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(nt(its(a, b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(nt(a), nt(b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(un(its(a, b), its(nt(a), b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(b)
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(its(un(a, b), un(nt(a), b)))
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
res.append(b)
arr_logs.append(logs)
logs = []
op_cnt[0] = 0
result_to_file(18, res, arr_logs)

print(logs)
