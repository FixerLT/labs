def get_table(row_names, column_names, connections, crazy_flag=False):
    tab = max([len(e) for e in row_names]) + 3
    shift = 3
    starts = []
    ends = []
    sm = tab+shift
    for e in column_names:
        starts.append(sm)
        sm += len(e)
        ends.append(sm)
        sm += shift
    positions = []
    for start, end in zip(starts, ends):
        positions.append(int((start + end)/2))
    sm -= shift
    result = ' ' * tab
    for e in column_names:
        result += ' ' * shift
        result += e
    for i, row in enumerate(row_names):
        result += '\n'
        result += row + ' ' * (tab - len(row))
        if crazy_flag:
            if i == 0 or i == 3:
                result += ' '
        for j, column in enumerate(column_names):
            result += ' ' * shift
            pos = int((len(column)+1) / 2)
            result += ' ' * (pos - 1)
            result += str(connections[i][j])
            result += ' ' * (len(column) - pos) if pos != 0 else ''
    return result


def to_chr(num):
    return str(num) if num < 10 else chr(ord('A') + num - 10)


def to_str(arr):
    return ''.join(reversed([str(e) for e in arr]))


def convert(arr, base, target):
    # print('converting ' + to_str(arr) + ' from ' + str(base) + ' to ' + str(target))

    log = to_str(arr) + ' = '
    num = 0
    for i, digit in enumerate(arr):
        num += digit * (base**i)
        log += str(digit) + ' * ' + str(base) + '^' + str(i)
        if i < len(arr) - 1:
            log += ' + '
    log += ' = ' + str(num) + ' = '
    res = []
    if num == 0:
        return [0]
    i = 0
    while num > 0:
        res.append(num % target)
        log += str(num % target) + ' * ' + str(target) + '^' + str(i)
        i += 1
        num = int(num/target)
        if num > 0:
            log += ' + '
    log += ' = ' + to_str(res)
    # print(log)
    return res, log


def int10_convert(num, base):
    less = False if num > -1 else True
    num = abs(num)
    log = '-' if less else ''
    log += str(num) + ' = '
    log += '-(' if less else ''
    res = []
    if num == 0:
        return [0]
    i = 0
    while num>0:
        res.append(num % base)
        log += str(num % base) + ' * ' + str(base) + '^' + str(i)
        i += 1
        num = int(num/base)
        if num > 0:
            log += ' + '
    log += ')' if less else ''
    log += ' = '
    log += '-' if less else ''
    log += to_str(res)
    return res, log


def convert_pk(arr, base):
    log = ''
    if base != 2:
        arr, l = convert_list(arr, base, 2)
        log += l
    mult = 1 if arr[-1] == 0 else -1
    log += '\n'
    log += to_str(arr) + ' = ' + str(mult) + ' * ('
    num = 0
    for i in range(len(arr) - 1):
        num += arr[i] * (2**i)
        log += str(arr[i]) + ' * 2^' + str(i)
        if i < len(arr) - 2:
            log += ' + '
    log += ') = '  # + str(mult) + ' * '
    r, l = int10_convert(num*mult, 16)
    log += l
    # log += ' = ' + to_str(r)
    res, l = int10_convert(num*mult, 2)
    return res, log


def convert_dk(arr):
    log = to_str(arr) + ' = '
    bck = 1 - arr[-1]
    num = 0
    if bck == 0:
        log += '-('
    sign_flag = False
    for i in range(len(arr)-1):
        if arr[i] == bck:
            if sign_flag:
                log += ' + '
            else:
                sign_flag = True
            num += 2**i * (1 if arr[i] == bck else 0)
            log += '2^' + str(i)
    if bck == 0:
        log += ')'
    log += ' = '
    if bck == 0:
        log += '-'
    log += str(num)
    return log


def convert_rk(arr, base):
    log = ''
    if base != 2:
        arr, l = convert_list(arr, base, 2)
        log += l
    mult = 1 if arr[-1] == 0 else -1
    log += '\n'
    log += to_str(arr) + ' = ' + str(mult) + ' * ('
    num = 0
    for i in range(len(arr) - 1):
        num += arr[i] * (2**i)
        log += str(arr[i]) + ' * 2^' + str(i)
        if i<len(arr) - 1:
            log += ' + '
    log += ') = '  # + str(mult) + ' * '
    r, l = int10_convert(num*mult, 16)
    log += l
    # log += ' = ' + to_str(r)
    res, l = int10_convert(num*mult, 2)
    return res, log


def pk_to_16(arr2):
    log = to_str(arr2) + ' = '
    # res = list(reversed(arr2))
    res = arr2.copy()
    if res[-1] == 0:
        while len(res) % 8 != 0:
            res.append(0)
        # log += to_str(arr2)
        # return res, log
    else:
        res[-1] = 0
        # res = list(reversed(res))
        while len(res) % 8 != 0:
            res.append(0)
        res[-1] = 1
        # res = list(reversed(res))
    log += to_str(res)
    return res, log


def convert_list(arr_arr, base, target):
    res = []
    logs = []
    for e in arr_arr:
        r, l = convert(e, base, target)
        res.append(r)
        logs.append(l)
    return res, logs

def cmp(arr1, arr2): #True if arr1 is smaller
    if len(arr1) == len(arr2):
        for i in range(len(arr1) - 1, -1, -1):
            if arr1[i] != arr2[i]:
                return arr1[i] < arr2[i]
    else:
        return len(arr1) < len(arr2)
    return True


def plus(arr1, arr2, base, limited = False):
    res = []
    extra = []
    one = False
    for i in range(max(len(arr1), len(arr2))):
        extra.append(1 if one else 0)
        v1 = 0 if i>=len(arr1) else arr1[i]
        v2 = 0 if i>=len(arr2) else arr2[i]
        val = v1+v2 + (1 if one else 0)
        one = False
        if val >= base:
            one = True
            val -= base
        res.append(val)
    if one and not limited:
        extra.append(1)
        res.append(1)

    table = []
    table.append([str(e) for e in extra])
    table.append([to_chr(e) for e in arr1])
    table.append([to_chr(e) for e in arr2])
    table.append([to_chr(e) for e in res])
    max_len = max([len(e) for e in table])
    for i in range(len(table)):
        while len(table[i]) < max_len:
            table[i].append(' ')
        table[i] = list(reversed(table[i]))
    return res, table


def minus(arr1, arr2, base):
    res = []
    extra = []
    one = False
    # a1 = [e for e in arr1]
    # a2 = [e for e in arr2]
    # mx = max(len(a1), len(a2))
    # while len(a1) < mx:
    #     a1.append(0)
    # while len(a2) < mx:
    #     a2.append(0)
    # a1 = list(reversed(a1))
    # a2 = list(reversed(a2))
    #
    for i in range(max(len(arr1), len(arr2))):
        extra.append(1 if one else 0)
        v1 = 0 if i>=len(arr1) else arr1[i]
        v2 = 0 if i>=len(arr2) else arr2[i]
        val = v1 - v2 - (1 if one else 0)
        one = False
        if val < 0:
            one = True
            val += base
        res.append(val)
    # if one:
    #     extra.append(1)
    #     res.append(1)

    table = []
    table.append([str(e) for e in extra])
    table.append([to_chr(e) for e in arr1])
    table.append([to_chr(e) for e in arr2])
    table.append([to_chr(e) for e in res])
    max_len = max([len(e) for e in table])
    for i in range(len(table)):
        while len(table[i]) < max_len:
            table[i].append(' ')
        table[i] = list(reversed(table[i]))
    return res, table


def ops_to_tables(names, tables):
    res = []
    rows = ['разрядная единица', '', '', 'результат']
    # print(tables)
    for i in range(len(tables)):
        rows[1], rows[2] = names[i]
        cols = [' ' for e in tables[i][0]]
        res.append(get_table(rows, cols, tables[i], crazy_flag=False))
    return res


def report_sum(pairs, names, base, path='/home/san/Documents/university/babakov/lab3/', f_name='', parser=None, limited=False):
    tables = []
    logs = []
    for a, b in pairs:
        r, t = plus(a, b, base, limited)
        tables.append(t)
        if parser != None:
            logs.append(parser(r))
    tables = ops_to_tables(names, tables)
    if f_name != '':
        with open(path + f_name + '.txt', 'w+') as f:
            for i, e in enumerate(tables):
                f.write(e)
                f.write('\n')
                if len(logs) > i:
                    f.write(logs[i])
                    f.write('\n')
    return tables


def push_front(arr, val):
    tmp = list(reversed(arr))
    tmp.append(val)
    return list(reversed(tmp))
    # return list(reversed(list(reversed(arr)).append(val)))


def report_delt(pairs, names, base, path='/home/san/Documents/university/babakov/lab3/', f_name=''):
    tables = []
    i=0
    for a, b in pairs:
        if cmp(a, b):
            r, t = minus(b, a, base)
            # for i in range(len(t)):
            #     t[i] = push_front(t[i], ' ')
            # t[3][0] = '-'
            # t[1], t[2] = t[2], t[1]
            tables.append(t)
            names[i] = (names[i][1], names[i][0])
        else:
            r, t = minus(a, b, base)
            tables.append(t)
        i+=1
    tables = ops_to_tables(names, tables)
    if f_name != '':
        with open(path + f_name + '.txt', 'w+') as f:
            for e in tables:
                f.write(e)
                f.write('\n')
    return tables

def report(logs, path='/home/san/Documents/university/babakov/lab3/', f_name = 'report_test'):
    with open(path + f_name + '.txt', 'w+') as f:
        for e in logs:
            f.write(e + '\n')

def save_nums(arr, logs = [], f_name = '', base=2, names=['a', 'b', 'c', 'd', 'e', 'f'], path = '/home/san/Documents/university/babakov/lab3/'):
    res = ''
    for i in range(len(arr)):
        res += names[i] + str(base) + ' = ' + to_str(arr[i]) + '\n'
        if len(logs) == len(arr):
            res += logs[i]
            res += '\n'
    if f_name != '':
        with open(path + f_name + '.txt', 'w+') as f:
            f.write(res)
    else:
        return res

a2_str = '10110' # Барго
b2_str = '1011' # Марк
c2_str = '01010101' #Игоревич
d2_str = reversed(a2_str)
e2_str = reversed(b2_str)
f2_str = reversed(c2_str)
a2 = list(reversed([ord(e) - ord('0') for e in a2_str]))
b2 = list(reversed([ord(e) - ord('0') for e in b2_str]))
c2 = list(reversed([ord(e) - ord('0') for e in c2_str]))
d2 = list(reversed([ord(e) - ord('0') for e in d2_str]))
e2 = list(reversed([ord(e) - ord('0') for e in e2_str]))
f2 = list(reversed([ord(e) - ord('0') for e in f2_str]))

all_2 = [a2, b2, c2, d2, e2, f2]

for i in range(len(all_2)):
    while all_2[i][-1] == 0:
        all_2[i] = all_2[i][:-1]
all_10, logs10 = convert_list(all_2, 2, 10)
all_3, logs3 = convert_list(all_10, 10, 3)
all_7, logs7 = convert_list(all_10, 10, 7)
all_8, logs8 = convert_list(all_10, 10, 8)
all_16, logs16 = convert_list(all_10, 10, 16)

a3, b3, c3, d3, e3, f3 = all_3
a7, b7, c7, d7, e7, f7 = all_3
a8, b8, c8, d8, e8, f8 = all_3
a16, b16, c16, d16, e16, f16 = all_3

save_nums(all_10, logs=logs10, base=10, f_name='1')
save_nums(all_3, logs=logs3, base=3, f_name='2')
save_nums(all_7, logs=logs7, base=7, f_name='3')
save_nums(all_8, logs=logs8, base=8, f_name='4')
save_nums(all_16, logs=logs16, base=16, f_name='5')

print([to_str(e) for e in all_16])
pairs2 = [(a2, f2), (c2, d2), (e2, b2), (a2, e2), (d2, f2)]
names2 = [('a2', 'f2'), ('c2', 'd2'), ('e2', 'b2'), ('a2', 'e2'), ('d2', 'f2')]
report_sum(pairs2, names2, 2, f_name='6')
report_delt(pairs2, names2, 2, f_name='11')

pairs3 = [(a3, f3), (c3, d3), (e3, b3), (a3, e3), (d3, f3)]
names3 = [('a3', 'f3'), ('c3', 'd3'), ('e3', 'b3'), ('a3', 'e3'), ('d3', 'f3')]
report_sum(pairs3, names3, 3, f_name='7')
report_delt(pairs3, names3, 3, f_name='12')

pairs7 = [(a7, f7), (c7, d7), (e7, b7), (a7, e7), (d7, f7)]
names7 = [('a7', 'f7'), ('c7', 'd7'), ('e7', 'b7'), ('a7', 'e7'), ('d7', 'f7')]
report_sum(pairs7, names7, 7, f_name='8')
report_delt(pairs7, names7, 7, f_name='13')

pairs8 = [(a8, f8), (c8, d8), (e8, b8), (a8, e8), (d8, f8)]
names8 = [('a8', 'f8'), ('c8', 'd8'), ('e8', 'b8'), ('a8', 'e8'), ('d8', 'f8')]
report_sum(pairs8, names8, 8, f_name='9')
report_delt(pairs8, names8, 8, f_name='14')

pairs16 = [(a16, f16), (c16, d16), (e16, b16), (a16, e16), (d16, f16)]
names16 = [('a16', 'f16'), ('c16', 'd16'), ('e16', 'b16'), ('a16', 'e16'), ('d16', 'f16')]
report_sum(pairs16, names16, 16, f_name='10')
report_delt(pairs16, names16, 16, f_name='15')


d2_str = reversed(a2_str)
e2_str = reversed(b2_str)
f2_str = reversed(c2_str)
a2 = list(reversed([ord(e) - ord('0') for e in a2_str]))
b2 = list(reversed([ord(e) - ord('0') for e in b2_str]))
c2 = list(reversed([ord(e) - ord('0') for e in c2_str]))
d2 = list(reversed([ord(e) - ord('0') for e in d2_str]))
e2 = list(reversed([ord(e) - ord('0') for e in e2_str]))
f2 = list(reversed([ord(e) - ord('0') for e in f2_str]))

all_2 = [a2, b2, c2, d2, e2, f2]
for e in all_2:
    print(to_str(e))

all_pk_2 = []
logs = []
for e in all_2:
    res, log = convert_pk(e, 2)
    all_pk_2.append(res)
    logs.append(log)
report(logs, f_name='16')

all_pk_16 = []
logs = []
for i in range(len(all_2)):
    my_pk, l = pk_to_16(all_2[i])
    all_pk_16.append(my_pk)
    logs.append(l)
report(logs, f_name='17')

pairs = [(all_pk_16[0], all_pk_16[1]), (all_pk_16[2], all_pk_16[5]), (all_pk_16[1], all_pk_16[4]), (all_pk_16[3], all_pk_16[0]), (all_pk_16[5], all_pk_16[4])]
names = [('Aпк16', 'Bпк16'), ('Cпк16', 'Fпк16'), ('Bпк16', 'Eпк16'), ('Dпк16', 'Aпк16'), ('Fпк16', 'Eпк16')]
parser_10_16 = lambda num2: (convert(num2, 2, 10)[1]) + '\n' + convert(num2, 2, 16)[1]
report_sum(pairs, names, 2, f_name='18', parser=parser_10_16, limited=True)

logs = []
for e in all_2:
    logs.append(convert_dk(e))
report(logs, f_name='19')

all_dk_16 = []
logs = []
for i in range(len(all_2)):
    my_dk, l = pk_to_16(all_2[i])
    all_dk_16.append(my_dk)
    logs.append(l)
report(logs, f_name='20')

pairs = [(all_dk_16[0], all_dk_16[1]), (all_dk_16[2], all_dk_16[5]), (all_dk_16[1], all_dk_16[4]), (all_dk_16[3], all_dk_16[0]), (all_dk_16[5], all_dk_16[4])]
names = [('Aдк16', 'Bдк16'), ('Cдк16', 'Fдк16'), ('Bдк16', 'Eдк16'), ('Dдк16', 'Aдк16'), ('Fдк16', 'Eдк16')]
report_sum(pairs, names, 2, f_name='21', parser=parser_10_16, limited=True)

all_pk_2_minus = []
for e in all_pk_16:
    all_pk_2_minus.append([k for k in e])
    all_pk_2_minus[-1][0] = 1 - all_pk_2_minus[-1][0]
logs = []
for i, e in enumerate(['-Aпк16', '-Bпк16', '-Cпк16', '-Dпк16', '-Eпк16', '-Fпк16']):
    logs.append(e + ' = ' + ''.join([str(k) for k in all_pk_2_minus[i]]))
report(logs, f_name='22')

all_dk_2_minus = []
for e in all_pk_16:
    all_dk_2_minus.append([k for k in e])
    if all_dk_2_minus[-1][0] == 1:
        all_dk_2_minus[-1][0] = 1 - all_pk_2_minus[-1][0]
    else:
        for i in range(len(all_dk_2_minus[-1])):
            all_dk_2_minus[-1][i] = 1 - all_pk_2_minus[-1][i]
logs = []
for i, e in enumerate(['-Aдк16', '-Bдк16', '-Cдк16', '-Dдк16', '-Eдк16', '-Fдк16']):
    logs.append(e + ' = ' + ''.join([str(k) for k in all_pk_2_minus[i]]))
report(logs, f_name='23')

logs = []
string1 = 'Старший байт числа равен '
string2 = 'Младший байт числа равен '
nums = ['-Aпк16', '-Bпк16', '-Cпк16', '-Dпк16', '-Eпк16', '-Fпк16']
for i, e in enumerate(nums):
    logs.append(string1 + e + ':')
    res, log = convert(list(reversed(all_pk_2_minus[i][:8])), 2, 16)
    logs.append(log)
    logs.append(string2 + e + ':')
    res, log = convert(list(reversed(all_pk_2_minus[i][-8:])), 2, 16)
    logs.append(log)
report(logs, f_name='24')

logs = []
nums = ['-Aдк16', '-Bдк16', '-Cдк16', '-Dдк16', '-Eдк16', '-Fдк16']
for i, e in enumerate(nums):
    logs.append(string1 + e + ':')
    res, log = convert(list(reversed(all_dk_2_minus[i][:8])), 2, 16)
    logs.append(log)
    logs.append(string2 + e + ':')
    res, log = convert(list(reversed(all_dk_2_minus[i][-8:])), 2, 16)
    logs.append(log)
report(logs, f_name='25')
