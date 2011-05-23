import math
from spy.scalar import *
from spy.utils import *

class expr_huber(object):
    def __init__(self):
        self.name = 'huber'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        assert len(args) == 1 or len(args) == 2
        if len(args) == 1: args.append(1.0)        
        assert isNumber(args[1]) and args[1] >= 0
        
        x = args[0]
        M = args[1]
        if isinstance(x, expr):
            return expr(self, [x, M])
        elif math.fabs(x) <= M:
            return x*x
        else:
            return M*(2.0*math.fabs(x)-M)
    def subgrad(self, values):
        x = values[0]
        if x < 0.0:
            raise ValueError('sqrt called with negative argument %f' %x)
        else:
            return [0.5/x]
    def is_increasing(self, argindex): return argindex == 1
    def is_decreasing(self, argindex): return False
    def is_convex(self): return True
    def is_concave(self): return False

# Function instance
huber = expr_huber()
