# dreslv.py
# Reuse L, U, perm to solve A x = b for a new right-hand side.
# Also counts multiplications.

def dreslv(L, U, perm, b):
    """
    L, U, perm : from dlineq
    b         : new RHS vector
    returns:
        x      – solution of A x = b
        mcount – number of multiplications
    """
    n = len(L)
    mcount = 0

    # P b
    Pb = [0.0] * n
    for i in range(n):
        Pb[i] = float(b[perm[i]])

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

    return x, mcount
