#!/usr/bin/env python

from spy import *
if __name__ == "__main__":
    ex = sum(3, 4)
    print ex
    
    ex = exp(sum(var('x'), var('y')))
    print ex.get_vars()
    print ex.get_value()
    print ex.get_value({'x': 2, 'y': -1})
    print ex.get_value({'x': 2})
    
    ex = exp(var('x'))
    print ex
    print 'computing subgrad at x=2, y=-1'
    print ex.subgrad({'x': 2, 'y': -1})
    
    x = var('x')
    y = var('y')
    
    ex = exp(exp(x))
    print ex
    print ex.get_value({'x': 1})
    print ex.get_value({'x': 0})
    print ex.subgrad({'x': 0})
    
    ex = max(x, y)
    print ex
    print ex.get_value({'x': 1124, 'y': 233})
    print ex.subgrad({'x': 1124, 'y': 233})
    
    ex = sum(prod(3, x), prod(4, y))
    print ex
    print ex.get_value({'x': 1124, 'y': 233})
    print ex.subgrad({'x': 1124, 'y': 233})
    
    ex = sqrt(sum(x, y))
    print ex
    print ex.get_value({'x': 3, 'y': 4})
    print ex.subgrad({'x': 3, 'y': 4})

    ex = max(0, prod(3, x))
    print ex
    print ex.subgrad({'x': 123})
    
    ex = prod(3, x)
    print ex
    print ex.subgrad({'x': 123})
	
    ex = sum(abs(sum(x, -3)), exp(x))
    print ex
    print ex.subgrad({'y': -2})
    
    #ex = x+3
    #print ex
    #print ex.get_value({'x': 12345})
    #print ex.subgrad({'x': 12345})
