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