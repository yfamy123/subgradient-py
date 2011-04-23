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
        return [1 for i in range(len(values))]

# Function instance
expr_sum = expr_sum()
