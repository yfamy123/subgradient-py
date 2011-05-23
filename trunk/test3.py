#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    x1 = var("x1")
    x2 = var("x2")
    
    ex1 = x1+x2
    ex2 = -x1-x2
    ex3 = x1
    ex4 = max(x1, x2)
    ex5 = square(x1)+9*square(x2)
    
    constraints = [greater(2*x1+x2, 1), greater(x1+3*x2, 1), greater(x1, 0), greater(x2, 0)]
    minimize(ex1, constraints).solve()
    minimize(ex2, constraints).solve()
    minimize(ex3, constraints).solve()
    minimize(ex4, constraints).solve()
    minimize(ex5, constraints).solve()
