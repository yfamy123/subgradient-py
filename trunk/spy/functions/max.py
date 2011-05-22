import math
import __builtin__
from spy.scalar import *

class expr_max(object):
    def __init__(self):
        self.name = 'max'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        
        x = args
        if isinstance(x[0], expr):
            return expr(self, x)
        return __builtin__.max(x)
    def subgrad(self, values):
        y = self(values)
        return [(float)(x == y) for x in values]
    def is_increasing(self, argindex): return True
    def is_decreasing(self, argindex): return False
    def is_convex(self): return True
    def is_concave(self): return False

# Function instance
max = expr_max()
