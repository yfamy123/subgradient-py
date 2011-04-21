import math
from defs import *

class expr_sum(object):
    def __init__(self):
        self.name = 'sum'
    def __call__(self, *args):
    	return sum(args[0])

# Function instance
expr_sum = expr_sum()
