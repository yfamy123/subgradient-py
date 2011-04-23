#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    x = expr_sum(3, 4)
    print x
    x = expr_sum(scalar(3), scalar(4))
    print x
    x = expr_exp(expr_sum(scalar_var('x'), scalar_var('y')))
    print x.get_vars()
    print x.get_value()
    print x.get_value({'x': 2, 'y': -1})
    print x.get_value({'x': 2})
    x = expr_exp(scalar_var('x'))
    print x
    print 'computing subgrad at x=2, y=-1'
    print x.subgrad({'x': 2, 'y': -1})
    
    x = scalar_var('x')
    y = scalar_var('y')
    
    # (e^(e^x))
    ex = expr_exp(expr_exp(x))
    print ex
    print ex.get_value({'x': 1})
    print ex.get_value({'x': 0})
    print ex.subgrad({'x': 0})
    
    ex = expr_max(x, y)
    print ex
    print ex.get_value({'x': 1124, 'y': 233})
    print ex.subgrad({'x': 1124, 'y': 233})
    
    ex = expr_sum(expr_prod(scalar(3), x), expr_prod(scalar(4), y))
    print ex
    print ex.get_value({'x': 1124, 'y': 233})
    print ex.subgrad({'x': 1124, 'y': 233})