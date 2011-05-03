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
    cons = expr_sum(x, y)
    
    cur = {'x': 0, 'y': 0}
    for i in range(10000):
        print ex.get_value(cur)
        if cons.get_value(cur) > 0: g = cons.subgrad(cur)
        else: g = ex.subgrad(cur)
        nxt = {}
        for key in cur.keys():
            nxt[key] = cur[key]-1.0*g[key]/(i+1.0);
        cur = nxt
    print 'is minimized with value ' + str(ex.get_value(cur))
    for key, val in cur.iteritems():
        print key + ': ' + str(val)
    #print ex
    #print ex.subgrad({'x': 123})
    
    #ex = x+3
    #print ex
    #print ex.get_value({'x': 12345})
    #print ex.subgrad({'x': 12345})
