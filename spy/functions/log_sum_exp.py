import math
from spy.scalar import *

class expr_log_sum_exp(object):
    def __init__(self):
        self.name = 'log_sum_exp'
    def __call__(self, *args):
        while type(args[0]) is list: args = args[0]
        
        x = args
        if(isinstance(x[0], expr)):
            return expr(expr_log_sum_exp, x)
        else:
            return math.log(sum([math.exp(xi) for xi in x]))
    def subgrad(self, values):
        exps = [math.exp(x) for x in values]
        expsum = sum(exps)
        return [val/expsum for val in exps]
    def is_increasing(self, argindex): return True
    def is_decreasing(self, argindex): return False
    def is_convex(self): return True
    def is_concave(self): return False

# Function instance
expr_log_sum_exp = expr_log_sum_exp()
