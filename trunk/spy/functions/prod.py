import math
from spy.scalar import *

class expr_prod(object):
    def __init__(self):
        self.name = 'prod'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        assert len(args) == 2
        
        x = args[0]
        y = args[1]
        if(isinstance(x, expr)):
            return expr(self, [x, y])
        else:
            return x*y
    def subgrad(self, values):
        x = values[0]
        y = values[1]
        return [y, x]
    def is_increasing(self, argindex): pass
    def is_decreasing(self, argindex): pass
    def is_convex(self): pass
    def is_concave(self): pass

# Function instance
prod = expr_prod()
