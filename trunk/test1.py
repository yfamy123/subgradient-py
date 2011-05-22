#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    ex = sum(3, 4)
    print ex
    
    ex = sum(scalar(3), scalar(4))
    print ex
    
    ex = exp(sum(scalar_var('x'), scalar_var('y')))
    print ex.get_vars()
    print ex.get_value()
    print ex.get_value({'x': 2, 'y': -1})
    print ex.get_value({'x': 2})
    
    ex = exp(scalar_var('x'))
    print ex
    print 'computing subgrad at x=2, y=-1'
    print ex.subgrad({'x': 2, 'y': -1})
    
    x = scalar_var('x')
    y = scalar_var('y')
    
    ex = exp(exp(x))
    print ex
    print ex.get_value({'x': 1})
    print ex.get_value({'x': 0})
    print ex.subgrad({'x': 0})
    
    ex = max(x, y)
    print ex
    print ex.get_value({'x': 1124, 'y': 233})
    print ex.subgrad({'x': 1124, 'y': 233})
    
    ex = sum(prod(scalar(3), x), prod(scalar(4), y))
    print ex
    print ex.get_value({'x': 1124, 'y': 233})
    print ex.subgrad({'x': 1124, 'y': 233})
    
    ex = sqrt(sum(x, y))
    print ex
    print ex.get_value({'x': 3, 'y': 4})
    print ex.subgrad({'x': 3, 'y': 4})

    ex = max(scalar(0), prod(scalar(3), x))
    print ex
    print ex.subgrad({'x': 123})
    
    ex = prod(scalar(3), x)
    print ex
    print ex.subgrad({'x': 123})
	
    ex = sum(abs(sum(x, scalar(-3))), exp(x))
    print ex
    print ex.subgrad({'y': -2})
    
    #ex = x+3
    #print ex
    #print ex.get_value({'x': 12345})
    #print ex.subgrad({'x': 12345})
