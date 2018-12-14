from newqm import QM

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

names1 = 'БаргоМаркИгоревич'
sz = len(names1)
for i in range(sz, 32):
    names1 += names1[i%sz]
names1 = list(names1)

col4 = [get_sym(e) for e in names1]

ones = []
dm = []
for i, e in enumerate(col4):
    if e == '1':
        ones.append(i)
    if e == '*':
        dm.append(i)
qm = QM(['a', 'b', 'c', 'd', 'e'])
print(qm.solve(ones, dm))
print(qm.get_function(qm.solve(ones, dm)[1]))
# (((not a) and b and e) or (a and (not b) and (not e)) or (a and c and (not d) and e) or ((not a) and c and d and e) or ((not a) and c and (not d) and (not e)) or (a and d and (not e)))
