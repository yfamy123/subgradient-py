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
    cons = sum(x, y)
    
    cur = {'x': 0, 'y': 0}
    for i in range(10000):
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
