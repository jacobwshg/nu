# main.py #

#
# Naive Matrix Multiplication app
#
# Uses standard triply-nested loop, nothing special. For simplicity, the matrices 
# are always square, i.e. we multiply NxN matrices, producing an NxN matrix.
#
# Usage:
#   mm [-?] [-n MatrixSize] [-t NumThreads]
#
# Author:
#   Prof. Joe Hummel
#   Northwestern University
#
import mm   # matrix multiply function

import math
import os
import sys
import time


#
# CreateAndFillMatrices:  fills A and B with predefined values, and then set TL, TR, BL and BR
# to the expected top-left, top-right, bottom-left and bottom-right values after the multiply.
#
def CreateAndFillMatrices(N):

    # 
    # create NxN matrices filled with 0:
    #
    A = [[0 for _ in range(N)] for _ in range(N)]
    B = [[0 for _ in range(N)] for _ in range(N)]

    #
    # A looks like:  
    #   1  1  1  1  ...  1
    #   2  2  2  2  ...  2
    #   .  .  .  .  ...  .
    #   .  .  .  .  ...  .
    #   N  N  N  N  ...  N
    #
    for r in range(N):
        for c in range(N):
            A[r][c] = r + 1;

    #
    # B looks like:
    #   1  2  3  4  ...  N
    #   1  2  3  4  ...  N
    #   .  .  .  .  ...  .
    #   .  .  .  .  ...  .
    #   1  2  3  4  ...  N
    #
    for r in range(N):
        for c in range(N):
            B[r][c] = c + 1;

    #
    # expected values:
    #
    TL = N;      # C[0,0] == Sum(1..1)
    TR = N*N;    # C[0,N-1] == Sum(N..N)
    BL = N*N;    # C[N-1, 0] == Sum(N..N)
    BR = N*N*N;  # C[N-1, N-1] == SUM(N^2..N^2)

    return A, B, TL, TR, BL, BR

#
# Checks the results against some expected results:
#
def CheckResults(N, C, TL, TR, BL, BR):

    b1 = math.isclose(C[0][0], TL)
    b2 = math.isclose(C[0][N-1], TR) 
    b3 = math.isclose(C[N-1][0], BL)
    b4 = math.isclose(C[N-1][N-1], BR)

    if (not b1) or (not b2) or (not b3) or ( not b4):
        print("** ERROR: matrix multiply yielded incorrect results")
        print()
        sys.exit(0)

    # 
    # if get here, all is well
    #
    return

#
# processCmdLineArgs:
#
def ProcessCmdLineArgs(_matrixSize, _numThreads):
    
    argc = len(sys.argv)

    #
    # for each command line arg (first arg is .py file, skip that one):
    #
    i = 1
    while i < argc:
        if sys.argv[i] == "-?": 
            # help:
            print("**Usage: mm [-?] [-n MatrixSize] [-t NumThreads]")
            print()
            sys.exit(0)
        elif (sys.argv[i] == "-n") and (i+1 < argc):
            # matrix size:
            i = i + 1
            _matrixSize = int(sys.argv[i])
        elif (sys.argv[i] == "-t") and (i+1 < argc):
            # # of threads:
            i = i + 1
            _numThreads = int(sys.argv[i])
        else:
            #error: unknown arg
            print(f"**Unknown argument: '{sys.argv[i]}'")
            print("**Usage: mm [-?] [-n MatrixSize] [-t NumThreads]")
            print()
            sys.exit(0)

        i = i + 1

    return _matrixSize, _numThreads


########################################################################
#
# main:
#

#
# Set defaults, process environment & cmd-line args:
#
_matrixSize = 1000
_numThreads = 1  # sequential execution

_matrixSize, _numThreads = ProcessCmdLineArgs(_matrixSize, _numThreads)

print("** Matrix Multiply Application **")
print()
print(f"Matrix size: {_matrixSize}x{_matrixSize}")

#
# Create and fill the matrices to multiply:
#
A, B, TL, TR, BL, BR = CreateAndFillMatrices(_matrixSize)

#
# Start clock and multiply:
#
start = time.time()

C = mm.MatrixMultiply(A, B, _matrixSize, _numThreads);

stop = time.time() 
duration = round(stop - start, 2) 

#
# Done, check results and output timing:
#
CheckResults(_matrixSize, C, TL, TR, BL, BR)

print()
print(f"** Done!  Time: {duration} secs")
print("** Execution complete **")
print()

