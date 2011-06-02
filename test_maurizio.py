#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    x = var('x')
    y = var('y')
    ex = geo_mean(x,y)
    print ex
    print ex.get_value({'x':2,'y':8})
    print ex.subgrad({'x':1,'y':100})

    ex = square_pos(x)
    print ex.get_value({'x':2})
    print ex.get_value({'x':-5})
    print ex.subgrad({'x':1})
    
    ex = rel_entr(x,y)
    print ex
    print ex.get_value({'x':2.0,'y':8.0})
    print ex.subgrad({'x':1,'y':100})

    ex = pow_pos(x,5.0)
    print ex
    print ex.get_value({'x': 2.0})
    print ex.get_value({'x': -2.0})
    print ex.subgrad({'x':2.0})
