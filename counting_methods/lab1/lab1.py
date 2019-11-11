import math


def my_round(num):
    src_num = num
    abs_error=[]
    rel_error=[]
    print("Округление")
    base = 7
    while base>=0:
        print('{})'.format(8-base), end='')
        num *= 10**base
        num = round(num)
        num /= 10**base
        base -= 1
        print(num)
        abs_error.append(abs(src_num - num))
        print('Абсолютная погрешность: ')
        print('|{} - {}| = {}'.format(src_num, num, abs_error[-1]))
        rel_error.append(abs(src_num - num) / abs(num))
        print('Относительная погрешность: ')
        print('|{} - {}| / |{}| = {}'.format(src_num, num, src_num, rel_error[-1]))
        true_value = 0.05 / (10**base)
        print('{} V {}'.format(abs_error[-1], true_value))
        if abs_error[-1] < true_value:
            print('Верная цифра')
        else:
            print('Сомнительная цифра')
    print()
    return abs_error, rel_error


# enter your variant here
variant_num = 6
expression = ''

n = variant_num + 22

#my_fun = lambda x: math.log(x+1)
my_fun = lambda x: math.cos(x)**3 + math.e**x  # enter your function here

my_value = my_fun(n)

print(my_value)

my_value *= 10**8
my_value = round(my_value)
my_value /= 10**8

print(my_value)

#my_value = int(my_value*1e8)
# print(my_value)

n_copy = my_value
while int(n_copy) == 0:
    n_copy*= 10
zn_cnt = len(str(n_copy)) - 1
print('Значущих цифр в числе {}'.format(zn_cnt))

abs_error, rel_error = my_round(my_value)
