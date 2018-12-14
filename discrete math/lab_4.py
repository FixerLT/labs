from newqm import QM
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
            result += str(connections[i][j])
            result += ' ' * (len(e2) - pos) if pos!=0 else ''
    return result


def my_not(a):
    # return chr(ord('z') - ord(a) + ord('a'))
    return '(not ' + a + ')'


def to_bin_arr(num):
    res = []
    for i in range(5):
        res.append(num % 2)
        num = int(num/2)
    res = list(reversed(res))
    return res


def to_bin_str(num):
    res = ''
    for i in range(5):
        res += (str(num%2))
        num = int(num/2)
    res2 = ''
    for i in range(4, -1, -1):
        res2 += res[4 - i]
    return res2


def small_kyr(let):
    return ord(let) >= ord('а') and ord(let) <= ord('я')


vowels = {'а', 'у', 'е', 'ы', 'о', 'э', 'я', 'и', 'ю'}


def is_vowel(let):
    return let in vowels


def get_sym(let):
    if not small_kyr(let):
        return '*'
    elif is_vowel(let):
        return '1'
    else:
        return '0'


def solve(names1):
    sz = len(names1)
    for i in range(sz, 32):
        names1 += names1[i % sz]
    names1 = list(names1)

    names2 = ['a', 'b', 'c', 'd', 'e', 'y1']

    col4 = [get_sym(e) for e in names1]
    connections = []
    for i in range(32):
        row = to_bin_arr(i)
        row.append(col4[i])
        connections.append(row)
    print(get_table(names1, names2, connections))
    print()
    print(get_table(names1, names2, [['0' if e == '*' else e for e in row] for row in connections]))

    ddnf = ''
    for i in range(32):
        if col4[i] == '1':
            if len(ddnf) != 0:
                ddnf += ' or '
            ddnf += '('
            ddnf += 'a' if connections[i][0] == 1 else my_not('a')
            ddnf += ' and '
            ddnf += 'b' if connections[i][1] == 1 else my_not('b')
            ddnf += ' and '
            ddnf += 'c' if connections[i][2] == 1 else my_not('c')
            ddnf += ' and '
            ddnf += 'd' if connections[i][3] == 1 else my_not('d')
            ddnf += ' and '
            ddnf += 'e' if connections[i][4] == 1 else my_not('e')
            ddnf += ')'
    print(ddnf)
    qm = QM(['e', 'd', 'c', 'b', 'a'])
    ones = []
    dm = []
    dknf = ''
    for i, e in enumerate(col4):
        if e == '1':
            ones.append(i)
        # if e == '*':
        #     dm.append(i)
    fn = str(qm.get_function(qm.solve(ones, dm)[1]))
    fn = fn.replace('NOT', 'not')
    fn = fn.replace('OR', 'or')
    fn = fn.replace('AND', 'and')
    print(fn + '\n')
    print()
    print(get_table(names1, names2, [['1' if e == '*' else e for e in row] for row in connections]))
    for i in range(32):
        if col4[i] == '0':
            if len(dknf) != 0:
                dknf += ' and '
            dknf += '('
            dknf += my_not('a') if connections[i][0] == 1 else 'a'
            dknf += ' or '
            dknf += my_not('b') if connections[i][1] == 1 else 'b'
            dknf += ' or '
            dknf += my_not('c') if connections[i][2] == 1 else 'c'
            dknf += ' or '
            dknf += my_not('d') if connections[i][3] == 1 else 'd'
            dknf += ' or '
            dknf += my_not('e') if connections[i][4] == 1 else 'e'
            dknf += ')'
    print(dknf)
    print()
    ones = []
    dm = []
    for i, e in enumerate(col4):
        if e == '1':
            ones.append(i)
        if e == '*':
            ones.append(i)
    fn = str(qm.get_function(qm.solve(ones, dm)[1]))
    fn = fn.replace('NOT', 'not')
    fn = fn.replace('OR', 'or')
    fn = fn.replace('AND', 'and')
    print(fn + '\n')
    print()
    ones = []
    dm = []
    for i, e in enumerate(col4):
        if e == '1':
            ones.append(i)
        if e == '*':
            dm.append(i)
    fn = str(qm.get_function(qm.solve(ones, dm)[1]))
    fn = fn.replace('NOT', 'not')
    fn = fn.replace('OR', 'or')
    fn = fn.replace('AND', 'and')
    print(fn + '\n')


solve('БаргоМаркИгоревич')
solve('МаркИгоревичБарго')
solve('ИгоревичБаргоМарк')