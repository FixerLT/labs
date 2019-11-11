import scipy
from scipy import linalg

def pprint(A):
    n = len(A)
    for i in range(0, n):
        line = ""
        for j in range(0, n+1):
            line += str(A[i][j]) + "\t"
            if j == n-1:
                line += "| "
        print(line)
    print("")


def gauss(A):
    n = len(A)

    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve equation Ax=b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x

#enter your values here
my_A = [[4, 1, 1, 2],
        [1, 3, 2, -1],
        [2, -1, 5, 3],
        [4, 5, 4, -4]]
my_B = [2, 2, -1, 8]
A = [a + [b] for a, b in zip(my_A, my_B)]

# todo pretty print input
print(A)

# solve
x_gauss = gauss(A)
x_it = linalg.solve(my_A, my_B)

# print output
# todo pretty
print('Gauss result:\t')
for i in range(0, len(my_A)):
    print(str(x_gauss[i]) + "\t")
print('iterative results: ')
print(x_it)


#
# if __name__ == "__main__":
#     from fractions import Fraction
#     n = int(input())
#
#     A = [[0 for j in range(n+1)] for i in range(n)]
#
#     # Read input data
#     for i in range(0, n):
#         line = [int(e) for e in input().split(" ")]
#         for j, el in enumerate(line):
#             A[i][j] = el
#
#     lastLine = [int(e) for e in input().split(" ")]
#     for i in range(0, n):
#         A[i][n] = lastLine[i]
#
#     # Print input
#     pprint(A)
#
#     # Calculate solution
#     x = gauss(A)
#
#     # Print result
#     line = "Result:\t"
#     for i in range(0, n):
#         line += str(x[i]) + "\t"
#     print(line)