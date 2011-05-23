#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    A = matrix(3, 4)
    x = vector(4)
    aa = [[1, 2, 3, 5], [0, 2, -3, 1], [-1.5, 3.14, 2.718, 0.0]]
    xx = [5, -3, 1.0, 2.222]
    for i in range(3):
        for j in range(4):
            A.set(i, j, aa[i][j])
    for i in range(4): x.set(i, xx[i])
    print A
    print x
    t = A*x
    print t
