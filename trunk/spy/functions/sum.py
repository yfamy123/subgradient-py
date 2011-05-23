import __builtin__
from spy.scalar import *

class expr_sum(object):
    def __init__(self):
        self.name = 'sum'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        
        x = args
        flag = False
        for xi in x:
            if isinstance(xi, expr):
                flag = True
                break
        if not flag: return __builtin__.sum(x)
        y = []
        for i in range(len(x)):
            if isNumber(x[i]): y.append(scalar(x[i]))
            else: y.append(x[i])
        return expr(self, y)
        
    def subgrad(self, values):
        return [1.0 for i in range(len(values))]
    def is_increasing(self, argindex): return True
    def is_decreasing(self, argindex): return False
    def is_convex(self): return True
    def is_concave(self): return True

# Function instance
sum = expr_sum()
