#!/usr/bin/env python

from spy import *

def print_sol(arg):
    (optval, optpoint) = arg
    print 'objective value: ' + str(optval)
    print 'optimal point: '
    for key, val in optpoint.iteritems():
        print key + ': ' + str(val)

if __name__ == "__main__":
    x1 = var("x1")
    x2 = var("x2")
    
    ex1 = x1+x2
    ex2 = -x1-x2
    ex3 = x1
    ex4 = max(x1, x2)
    ex5 = square(x1)+9*square(x2)
    
    constraints = [geq(2*x1+x2, 1), geq(x1+3*x2, 1), geq(x1, 0), geq(x2, 0)]

    print_sol(minimize(ex1, constraints).solve())
    print_sol(minimize(ex2, constraints).solve())
    print_sol(minimize(ex3, constraints).solve())
    print_sol(minimize(ex4, constraints).solve())
    print_sol(minimize(ex5, constraints).solve())
    
    print_sol(maximize(-ex1, constraints).solve())
    print_sol(maximize(-ex2, constraints).solve())
    print_sol(maximize(-ex3, constraints).solve())
    print_sol(maximize(-ex4, constraints).solve())
    print_sol(maximize(-ex5, constraints).solve())
