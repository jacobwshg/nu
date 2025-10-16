# mm.py #

#
# Matrix multiplication implementation, computing C=A*B where A and B
# are NxN matrices. The resulting matrix C is therefore NxN.
#
import os

from concurrent.futures import ProcessPoolExecutor as PPE


#################### debug
def matprint(M, m_name=''):
    '''
    print(m_name)
    for row in M:
       print(' '.join([f'{n}' for n in row]))
    print()
    '''
    print('\n'.join([ ' '.join([f'{n}' for n in row]) for row in M ]))

"""
    C_start_rowno: lowest row in C that the child is responsible for
    C_end_rowno: one row _past_ the highest row in C that ...
"""
class ChildData:
    def __init__(self, N, A, B, C, child_C_start, child_C_end):
        self.N = N
        self.A = A
        self.B = B
        self.C = C
        self.C_start_rowno = child_C_start
        self.C_end_rowno = child_C_end

def child_mm(child_data):
    N = child_data.N
    A = child_data.A
    B = child_data.B
    C = child_data.C
    C_start_rowno = child_data.C_start_rowno
    C_end_rowno = child_data.C_end_rowno

    for i in range(C_start_rowno, C_end_rowno):
        for k in range(N):
            for j in range(N):
                C[i][j] += (A[i][k] * B[k][j])

    return C

#
# MatrixMultiply:
#
# Computes and returns C = A * B, where matrices are NxN. No attempt is made
# to optimize the multiplication.
#
def MatrixMultiply(A, B, N, T):
  
    #
    # Setup:
    #
    print(f"Num cores: {os.cpu_count()}")
    print(f"Num threads: {T}")
    print()

    #
    # Initialize target matrix in prep for summing:
    #
    C = [[0 for _ in range(N)] for _ in range(N)]

    child_data_list = []

    #
    # Round-up int division so that process T-1 (0-based idx)
    # does less rows instead of more than others
    #
    block_max_nrows = (N + (T - 1)) // T

    for cid in range(T):
        child_C_start = cid * block_max_nrows
        child_C_end = child_C_start + block_max_nrows
        if child_C_end > N: # possible for process T-1
            child_C_end = N

        child_data_list.append(\
            ChildData(N, A, B, C, child_C_start, child_C_end)\
        )

    with PPE() as ppe:
        # Launch children
        child_Cs = list(ppe.map(child_mm, child_data_list))

        # Copy each child's C slice into parent's C
        for cid in range(T):
            child_start = child_data_list[cid].C_start_rowno
            child_end = child_data_list[cid].C_end_rowno
            for i in range(child_start, child_end):
                for j in range(N):
                    C[i][j] = child_Cs[cid][i][j]

    ## matprint(C, 'C')

    #
    # return result matrix:
    #
    return C

