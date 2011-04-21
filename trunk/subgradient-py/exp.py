import math
from defs import *

class expr_exp(object):
    def __init__(self):
        self.curvature = CONVEX
        self.name = 'exp'
    def __call__(self, *args):
        self.args = args[0]
        return self
    def monotonicity(self):
        return INCREASING
    def get_value(self):
        return math.exp(self.args)

# Function instance
exp = expr_exp()
