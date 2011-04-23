import math
from spy.scalar import *

class expr_log(object):
    def __init__(self):
        self.name = 'log'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        assert len(args) == 1
        
        x = args[0]
        if(isinstance(x, expr)):
            return expr(expr_log, [x])
        elif x <= 0:
            raise ValueError('log called with negative argument %f' %x)
        else:
            return math.log(x)
    def subgrad(self, values):
        x = values[0]
        if x <= 0:
            raise ValueError('log called with negative argument %f' %x)
        else:
            return [1.0/x]

# Function instance
expr_log = expr_log()
