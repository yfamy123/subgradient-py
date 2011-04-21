import math
from defs import *
from scalar import *

class expr_max(object):
    def __init__(self):
        self.name = 'max'
    def __call__(self, *args):
        if(len(args) == 1):
            x = args[0]
        else:
            x = args
        # now x is a list
        print x[0]
        if(isinstance(x[0], expr)):
            return expr(expr_max, x)
        else:
            return max(x)

# Function instance
expr_max = expr_max()
