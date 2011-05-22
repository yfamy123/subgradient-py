#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    x = scalar_var('x')
    y = scalar_var('y')
    ex1 = sum(sum(prod(scalar(3), x), prod(scalar(-4), y), scalar(10)), abs(sum(x, scalar(-1))), quad_over_lin(x, scalar(1)), quad_over_lin(y, scalar(3)))
    ex2 = sum(sum(prod(scalar(-2), x), prod(scalar(6), y), scalar(-5)), abs(sum(y, scalar(-3))), quad_over_lin(x, scalar(0.5)), quad_over_lin(y, scalar(5)))
    print ex1
    print ex2
    ex = max(ex1, ex2)
    print ex
    constraints = [constraint(sum(x, y), 'lt', scalar(0))]
    prob = problem('minimize', ex, constraints)
    prob.solve()
