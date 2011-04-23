import math
from spy.scalar import *

class expr_sum(object):
    def __init__(self):
        self.name = 'sum'
    def __call__(self, *args):
        if(len(args) == 1):
            x = args[0]
        else:
            x = args
        # now x is a list
        if(isinstance(x[0], expr)):
            return expr(expr_sum, x)
        else:
            return sum(x)

# Function instance
expr_sum = expr_sum()
