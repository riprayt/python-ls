# Compute the inverse of a matrix A using Gauss–Jordan elimination.
# A is an n x n matrix given as a list of lists (we can say matrix).
# Returns A_inv as a list of lists.

def gauss_jordan_inverse(A):
    n = len(A)

    # Build augmented matrix [A | I]
    # M will be n x (2n)
    M = []
    for i in range(n):
        row = []
        # left part = A
        for j in range(n):
            row.append(float(A[i][j]))
        # right part = identity
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        M.append(row)

    # Gauss–Jordan elimination
    for k in range(n):
        # 1) Find pivot row (partial pivoting)
        pivot_row = k
        for i in range(k + 1, n):
            if abs(M[i][k]) > abs(M[pivot_row][k]):
                pivot_row = i

        if M[pivot_row][k] == 0:
            raise ValueError("Matrix is singular; cannot invert.")

        # 2) Swap current row with pivot row if needed
        if pivot_row != k:
            M[k], M[pivot_row] = M[pivot_row], M[k]

        # 3) Make the pivot equal to 1
        pivot = M[k][k]
        for j in range(2 * n):
            M[k][j] = M[k][j] / pivot

        # 4) Eliminate this column in all other rows
        for i in range(n):
            if i != k:
                factor = M[i][k]
                for j in range(2 * n):
                    M[i][j] = M[i][j] - factor * M[k][j]

    # After this, left side is I, right side is A^{-1}
    A_inv = []
    for i in range(n):
        row = []
        for j in range(n, 2 * n):
            row.append(M[i][j])
        A_inv.append(row)

    return A_inv
