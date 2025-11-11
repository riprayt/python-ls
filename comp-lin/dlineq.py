# LU factorization with partial pivoting + solve A x = b
# Also counts how many multiplications are done.

def dlineq(A, b):
    """
    A : n x n matrix  (list of lists)
    b : length-n vector (list)
    returns:
        x      – solution of A x = b
        L, U   – LU factors
        perm   – permutation list
        mcount – number of multiplications
    """
    n = len(A)
    mcount = 0  # multiplication counter

    # Copy A into U
    U = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(float(A[i][j]))
        U.append(row)

    # L = identity
    L = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                row.append(0.0)
        L.append(row)

    # permutation vector
    perm = []
    for i in range(n):
        perm.append(i)

    # LU factorization
    for k in range(n):
        # pivot
        pivot_row = k
        for i in range(k + 1, n):
            if abs(U[i][k]) > abs(U[pivot_row][k]):
                pivot_row = i

        if U[pivot_row][k] == 0:
            raise ValueError("Matrix is singular; cannot factorize.")

        # swap rows in U, L, perm
        if pivot_row != k:
            U[k], U[pivot_row] = U[pivot_row], U[k]
            for j in range(k):
                L[k][j], L[pivot_row][j] = L[pivot_row][j], L[k][j]
            perm[k], perm[pivot_row] = perm[pivot_row], perm[k]

        # eliminate
        for i in range(k + 1, n):
            multiplier = U[i][k] / U[k][k]
            L[i][k] = multiplier
            for j in range(k, n):
                # one multiplication: multiplier * U[k][j]
                U[i][j] = U[i][j] - multiplier * U[k][j]
                mcount += 1

    # Solve A x = b using L, U, perm

    # P b
    Pb = []
    for i in range(n):
        Pb.append(float(b[perm[i]]))

    # forward: L y = P b
    y = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(i):
            s = s + L[i][j] * y[j]
            mcount += 1
        y[i] = Pb[i] - s

    # backward: U x = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = 0.0
        for j in range(i + 1, n):
            s = s + U[i][j] * x[j]
            mcount += 1
        x[i] = (y[i] - s) / U[i][i]

    return x, L, U, perm, mcount
