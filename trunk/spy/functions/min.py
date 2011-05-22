import math
import __builtin__
from spy.scalar import *

class expr_min(object):
    def __init__(self):
        self.name = 'min'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        
        x = args
        if isinstance(x[0], expr):
            return expr(self, x)
        return __builtin__.min(x)
    def subgrad(self, values): pass
    def is_increasing(self, argindex): return True
    def is_decreasing(self, argindex): return False
    def is_convex(self): return False
    def is_concave(self): return True

# Function instance
min = expr_min()
