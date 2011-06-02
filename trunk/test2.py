#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    x = var('x')
    y = var('y')
    ex1 = (3*x-4*y+10)+abs(x-1)+quad_over_lin(x, 1)+quad_over_lin(y, 3)
    ex2 = (-2*x+6*y-5)+abs(y-3)+quad_over_lin(x, 0.5)+quad_over_lin(y, 5)
    print ex1
    print ex2
    ex = max(ex1, ex2)
    print ex
    constraints = [geq(x+y, 0)]
    prob = minimize(ex, constraints)
    prob.solve()
