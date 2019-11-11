import numpy as np
import matplotlib.pyplot as plt
import math



def trapz(f, a, b, N_fn=lambda a, b: 50, visualize=None):
    N = N_fn(a, b)
    '''Approximate the integral of f(x) from a to b by the trapezoid rule.

    The trapezoid rule approximates the integral \int_a^b f(x) dx by the sum:
    (dx/2) \sum_{k=1}^N (f(x_k) + f(x_{k-1}))
    where x_k = a + k*dx and dx = (b - a)/N.

    Parameters
    ----------
    f : function
        Vectorized function of a single variable
    a , b : numbers
        Interval of integration [a,b]
    N : integer
        Number of subintervals of [a,b]

    Returns
    -------
    float
        Approximation of the integral of f(x) from a to b using the
        trapezoid rule with N subintervals of equal length.

    Examples
    --------
    >>> trapz(np.sin,a=0,b=np.pi/2,N=1000)
    0.99999979438323316
    '''
    x = np.linspace(a, b, N+1)
    y = [f(e) for e in x]
    y_right = y[1:]  # Right endpoints
    y_left = y[:-1]  # Left endpoints
    dx = (b - a)/N
    T = (dx/2) * np.sum(y_right + y_left)

    if visualize is not None:
        X = np.linspace(a, b, 10 * N + 1)
        Y = [f(e) for e in X]

        plt.plot(X, Y)

        for i in range(N):
            xs = [x[i], x[i], x[i + 1], x[i + 1]]
            ys = [0, f(x[i]), f(x[i + 1]), 0]
            plt.fill(xs, ys, 'b', edgecolor='b', alpha=0.2)

        plt.title('Trapezoid Rule, N = {}'.format(N))
        plt.savefig(visualize)

    return T

def riemann_sum(f,a,b,N_fn,method='midpoint', visualze=None):
    '''Compute the Riemann sum of f(x) over the interval [a,b].

    Parameters
    ----------
    f : function
        Vectorized function of one variable
    a , b : numbers
        Endpoints of the interval [a,b]
    N : integer
        Number of subintervals of equal length in the partition of [a,b]
    method : string
        Determines the kind of Riemann sum:
        right : Riemann sum using right endpoints
        left : Riemann sum using left endpoints
        midpoint (default) : Riemann sum using midpoints

    Returns
    -------
    float
        Approximation of the integral given by the Riemann sum.
    '''
    N = n_fn(a, b)
    dx = (b - a)/N
    x = np.linspace(a,b,N+1)
    if visualze is not None:
        y = [f(e) for e in x]

        X = np.linspace(a, b, 1 * N + 1)
        Y = [f(e) for e in X]

        plt.plot(X, Y, 'b')
        x_mid = (x[:-1] + x[1:]) / 2  # Midpoints
        y_mid = [f(e) for e in x_mid]
        plt.plot(x_mid, y_mid, 'b.', markersize=10)
        plt.bar(x_mid, y_mid, width=(b - a) / N, alpha=0.2, edgecolor='b')
        plt.title('Midpoint Riemann Sum, N = {}'.format(N))
        plt.savefig(visualze)

    if method == 'left':
        x_left = x[:-1]
        return np.sum(f(x_left)*dx)
    elif method == 'right':
        x_right = x[1:]
        return np.sum(f(x_right)*dx)
    elif method == 'midpoint':
        x_mid = (x[:-1] + x[1:])/2
        return np.sum(f(x_mid)*dx)
    else:
        raise ValueError("Method must be 'left', 'right' or 'midpoint'.")

def simps(f,a,b,N_fn = lambda a1, b1: 10):
    '''Approximate the integral of f(x) from a to b by Simpson's rule.

    Simpson's rule approximates the integral \int_a^b f(x) dx by the sum:
    (dx/3) \sum_{k=1}^{N/2} (f(x_{2i-2} + 4f(x_{2i-1}) + f(x_{2i}))
    where x_i = a + i*dx and dx = (b - a)/N.

    Parameters
    ----------
    f : function
        Vectorized function of a single variable
    a , b : numbers
        Interval of integration [a,b]
    N : (even) integer
        Number of subintervals of [a,b]

    Returns
    -------
    float
        Approximation of the integral of f(x) from a to b using
        Simpson's rule with N subintervals of equal length.

    Examples
    --------
    # >>> simps(lambda x : 3*x**2,0,1,10)
    # 1.0
    '''
    #TODO visualize
    N = N_fn(a, b)
    if N % 2 == 1:
        raise ValueError("N must be an even integer.")
    dx = (b-a)/N
    x = np.linspace(a,b,N+1)
    y = [f(e) for e in x]
    S = dx/3 * np.sum(y[0:-1:2] + 4*y[1::2] + y[2::2])
    return S

# enter your values here
my_fn = lambda x: math.log(x)
my_Fn = lambda x: x * math.log(x) - x
a=1
b=2
acc=1e-4
n_fn = lambda a, b: 10
trapz(my_fn, a, b, n_fn, 'trapz.png')
riemann_sum(my_fn, a, b, n_fn, visualze='riemann.png')