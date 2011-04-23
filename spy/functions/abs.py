import math
from spy.scalar import *

class expr_abs(object):
    def __init__(self):
        self.name = 'abs'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        assert len(args) == 1
        
        x = args[0]
        if(isinstance(x, expr)):
            return expr(expr_abs, [x])
        else:
            return math.abs(x)
    def subgrad(self, values):
        x = values[0]
        if x > 0:   return 1
        elif x < 0: return -1
        else:       return 0

# Function instance
expr_abs = expr_abs()
