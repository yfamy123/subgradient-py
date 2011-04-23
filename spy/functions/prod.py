import math
from defs import *
from scalar import *

class expr_prod(object):
    def __init__(self):
        self.name = 'prod'
    def __call__(self, *args):
        if(len(args) != 2):
            raise ValueError('prod called with multiple arguments')

        x = args[0]
        y = args[1]
        if(isinstance(x, expr)):
            return expr(expr_prod, [x, y])
        else:
            return x*y

# Function instance
expr_prod = expr_prod()
