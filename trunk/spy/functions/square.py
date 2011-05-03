import math
from spy.scalar import *

class expr_square(object):
    def __init__(self):
        self.name = 'square'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        assert len(args) == 1
        
        x = args[0]
        if(isinstance(x, expr)):
            return expr(expr_square, [x])
        else:
            return x*x
    def subgrad(self, values):
        x = values[0]
        return [2.0*x]

# Function instance
expr_square = expr_square()
