#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    x = scalar_var('x')
    y = scalar_var('y')
    ex1 = expr_sum(expr_sum(expr_prod(scalar(3), x), expr_prod(scalar(-4), y), scalar(10)), expr_abs(expr_sum(x, scalar(-1))), expr_quad_over_lin(x, scalar(1)), expr_quad_over_lin(y, scalar(3)))
    ex2 = expr_sum(expr_sum(expr_prod(scalar(-2), x), expr_prod(scalar(6), y), scalar(-5)), expr_abs(expr_sum(y, scalar(-3))), expr_quad_over_lin(x, scalar(0.5)), expr_quad_over_lin(y, scalar(5)))
    print ex1
    print ex2
    ex = expr_max(ex1, ex2)
    print ex
    constraints = [constraint(expr_sum(x, y), 'lt', scalar(0))]
    prob = problem('minimize', ex, constraints)
    prob.solve()
