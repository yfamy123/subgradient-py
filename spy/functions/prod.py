import math
from spy.scalar import *

class expr_prod(object):
    def __init__(self):
        self.name = 'prod'
    def __call__(self, *args):
        if(len(args) == 1):
            a = args[0]
        else:
            a = args
        # now a is a list
        x = a[0]
        y = a[1]
        if(isinstance(x, expr)):
            return expr(expr_prod, [x, y])
        else:
            return x*y
    def subgrad(self, values):
        x = values[0]
        y = values[1]
        return [y, x]

# Function instance
expr_prod = expr_prod()
