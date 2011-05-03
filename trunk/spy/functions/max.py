import math
from spy.scalar import *

class expr_max(object):
    def __init__(self):
        self.name = 'max'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        
        x = args
        if isinstance(x[0], expr):
            return expr(expr_max, x)
        else:
            return max(x)
    def subgrad(self, values):
        y = expr_max(values)
        return [(float)(x == y) for x in values]
    def is_increasing(self, argindex): return True
    def is_decreasing(self, argindex): return False
    def is_convex(self): return True
    def is_concave(self): return False

# Function instance
expr_max = expr_max()
