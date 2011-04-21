import math
from defs import *
from scalar import *

class expr_exp(object):
    def __init__(self):
        self.name = 'exp'
    def __call__(self, *args):
        if(len(args) != 1):
            raise ValueError('exp called with multiple arguments')
        
        if(type(args[0]) is list):
            x = args[0][0]
        else:
            x = args[0]
        
        if(isinstance(x, expr)):
            return expr(expr_exp, [x])
        else:
            return math.exp(x)

# Function instance
expr_exp = expr_exp()
