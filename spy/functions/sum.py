import math
from spy.scalar import *

class expr_sum(object):
    def __init__(self):
        self.name = 'sum'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        
        x = args
        if(isinstance(x[0], expr)):
            return expr(expr_sum, x)
        else:
            return sum(x)
    def subgrad(self, values):
        return [1.0 for i in range(len(values))]
    def is_increasing(self, argindex): return True
    def is_decreasing(self, argindex): return False
    def is_convex(self): return True
    def is_concave(self): return True

# Function instance
expr_sum = expr_sum()
