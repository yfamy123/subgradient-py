import math
from spy.scalar import *

class expr_quad_over_lin(object):
    def __init__(self):
        self.name = 'prod'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        assert len(args) == 2
        
        x = args[0]
        y = args[1]
        if(isinstance(x, expr)):
            return expr(expr_quad_over_lin, [x, y])
        else:
            return x*x/y
    def subgrad(self, values):
        x = values[0]
        y = values[1]
        return [2*x/y, -(x*x)/(y*y)]

# Function instance
expr_quad_over_lin = expr_quad_over_lin()
