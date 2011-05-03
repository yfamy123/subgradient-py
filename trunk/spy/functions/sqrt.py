import math
from spy.scalar import *

class expr_sqrt(object):
    def __init__(self):
        self.name = 'sqrt'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        assert len(args) == 1
        
        x = args[0]
        if(isinstance(x, expr)):
            return expr(expr_sqrt, [x])
        elif x < 0:
            raise ValueError('sqrt called with negative argument %f' %x)
        else:
            return math.sqrt(x)
    def subgrad(self, values):
        x = values[0]
        if x < 0.0:
            raise ValueError('sqrt called with negative argument %f' %x)
        else:
            return [0.5/x]
    def is_increasing(self, argindex): return True
    def is_decreasing(self, argindex): return False
    def is_convex(self): return False
    def is_concave(self): return True

# Function instance
expr_sqrt = expr_sqrt()
