# where we demonstrate usage of the functions implemented in dlineq.py, dreslv.py, gj_inverse.py
# use dlineq, dreslv, gj inverse functions with demo matrices

from dlineq import dlineq
from dreslv import dreslv
from gj_inverse import gauss_jordan_inverse


def inverse_matrix_dlineq_dreslv(A):
    n = len(A)
    A_inv = [[0.0 for _ in range(n)] for _ in range(n)]
    total_mult = 0

    # first column, use DLINEQ
    e1 = [0.0] * n
    e1[0] = 1.0
    x1, L, U, perm, m1 = dlineq(A, e1)
    total_mult += m1
    for i in range(n):
        A_inv[i][0] = x1[i]

    # remaining columns, use DRESLV
    for k in range(1, n):
        ek = [0.0] * n
        ek[k] = 1.0
        xk, mk = dreslv(L, U, perm, ek)
        total_mult += mk
        for i in range(n):
            A_inv[i][k] = xk[i]

    return A_inv, total_mult


if __name__ == "__main__":
    A = [[4, 7],
         [2, 6]]

    B = [[1, 2, 3],
         [0, 1, 4],
         [5, 6, 0]]

    A_inv, mcount = inverse_matrix_dlineq_dreslv(A)

    print("\nA inverse using dlineq dreslv:")
    for row in A_inv:
        print(row)

    print("\nTotal multiplications for A:", mcount)

    B_inv, mcount_B = inverse_matrix_dlineq_dreslv(B)

    print("\nB inverse using dlineq dreslv:")
    for row in B_inv:
        print(row)

    print("\nTotal multiplications for B:", mcount_B)

    A_inv_gj = gauss_jordan_inverse(A)
    print("\nA inverse using Gauss-Jordan:")
    for row in A_inv_gj:
        print(row)

    B_inv_gj = gauss_jordan_inverse(B)
    print("\nB inverse using Gauss-Jordan:")
    for row in B_inv_gj:
        print(row)
