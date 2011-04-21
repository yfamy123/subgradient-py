import math
from defs import *

class expr_max(object):
    def __init__(self):
        self.name = 'max'
    def __call__(self, *args):
    	return max(args[0])

# Function instance
expr_max = expr_max()
