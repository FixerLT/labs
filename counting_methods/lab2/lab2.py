import matplotlib
from matplotlib import pyplot as plt
import math
import numpy as np
from pypoly import Polynomial

def plot_lagranz(x, y, secret_point):
     def lagranz(x,y,t):
         z=0
         for j in range(len(y)):
             p1=1; p2=1
             for i in range(len(x)):
                 if i==j:
                     p1=p1*1; p2=p2*1
                 else:
                     p1=p1*(t-x[i])
                     p2=p2*(x[j]-x[i])
             z=z+y[j]*p1/p2
         return z
     xnew=np.linspace(np.min(x),np.max(x),100)
     ynew=[lagranz(x,y,i) for i in xnew]
     plt.plot(x,y,'o',xnew,ynew)
     plt.grid(True)
     plt.title('Интерполяция Полиномом Лагранжа')
     plt.show()
     return lagranz(x, y, secret_point)

def solve_lagranz(x, y):
    x, X = len(x), list(zip(x, y))
    equations = np.array([[point[0] ** i for i in range(len(X))] for point in X])
    values = np.array([point[1] for point in X])
    coefficients = np.linalg.solve(equations, values)
    return coefficients


def coef(x, y):
    '''x : array of data points
       y : array of f(x)  '''
    # x.astype(float)
    # y.astype(float)
    n = len(x)
    a = []
    for i in range(n):
        a.append(y[i])

    for j in range(1, n):

        for i in range(n-1, j-1, -1):
            a[i] = float(a[i]-a[i-1])/float(x[i]-x[i-j])

    return np.array(a) # return an array of coefficient


def Eval(a, x, r):

    # x.astype(float)
    n = len(a) - 1
    temp = a[n] + (r - x[n])
    for i in range(n - 1, -1, -1):
        temp = temp * (r - x[i]) + a[i]
    return temp  # return the y_value interpolation
    #    a : array returned by function coef()
    #    x : array of data points
    #    r : the node to interpolate at


#enter your values here
a = 0.1
b = 0.25

step = 0.01

functions = [lambda x: math.log(math.sin(x)),
             lambda x: ((x**3) + 1)**0.5,
             lambda x: x, #TODO nuhia ne vidno, gde norm screen shot
             lambda x: ((3*(x**2)) + 1)**0.5,
             lambda x: 1/((x+1)**0.5),
             lambda x: math.e ** x + math.cos(x)**3] # tut ne ponyatno cos(x^3) ili cox(x)^3
fn = functions[5]

secret_point = a + 3.5 * step

x = []
y = []
tmp = a
while tmp - b - 0.005 < 0.0001:
    x.append(tmp)
    y.append(fn(tmp))
    tmp += step
plt.plot(x, y, 'o')
plt.grid(True)
plt.title('Значения Функции')
plt.show()

# plot_lagranz(x, y)
# l_cf = solve_lagranz(x, y)
# p = Polynomial(*l_cf)
# print("Lagrande polynomial: {}".format(p))
lagrande_secret_point_value = plot_lagranz(x, y, secret_point)


newton_cf = coef(x, y)
# p = Polynomial(*newton_cf)
# print("Newton's polynomial: {}".format(p))
xnew=np.linspace(np.min(x), np.max(x), 100)
ynew=[Eval(newton_cf, x, i) for i in xnew]
plt.plot(x, y, 'o', xnew, ynew)
plt.grid(True)
plt.title('Интерполяция Полиномом Ньютона')
plt.show()
newton_secret_point_value = Eval(newton_cf, x, secret_point)

fn_secret_point_value = fn(secret_point)
lagrande_abs = abs(lagrande_secret_point_value - fn_secret_point_value)
lagrande_rel = lagrande_abs / abs(fn_secret_point_value)
newton_abs = abs(newton_secret_point_value - fn_secret_point_value)
newton_rel = newton_abs / abs(fn_secret_point_value)
print("Абсолютная погрешность в точке {} для полинома Лагранжа составляет {}".format(secret_point, lagrande_abs))
print("Относительная погрешность в точке {} для полинома Лагранжа составляет {}".format(secret_point, lagrande_rel))
print("Абсолютная погрешность в точке {} для полинома Ньютона составляет {}".format(secret_point, newton_abs))
print("Относительная погрешность в точке {} для полинома Ньютона составляет {}".format(secret_point, newton_rel))