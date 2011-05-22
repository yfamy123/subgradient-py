#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    x = var('x')
    y = var('y')
    ex1 = sum(sum(prod(3, x), prod(-4, y), 10), abs(sum(x, -1)), quad_over_lin(x, 1), quad_over_lin(y, 3))
    ex2 = sum(sum(prod(-2, x), prod(6, y), -5), abs(sum(y, -3)), quad_over_lin(x, 0.5), quad_over_lin(y, 5))
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
