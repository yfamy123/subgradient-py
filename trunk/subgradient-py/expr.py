from defs import *

# Base class
class expr(object):
    def __init__(self, value = None):
        self.value = value
        self.shape = (1, 1)
    def get_shape(self):
        return self.shape
    def is_convex(self):
        return True
    def is_concave(self):
        return True
    def is_affine(self):
        return True
    def is_increasing(self):
        return True
    def is_decreasing(self):
        return True
    def get_value(self):
        return self.value
    def get_subgradient(self, x = None):
        return 0

class expr_tree(expr):
    def __init__(self, this, children):
        self.this     = this
        self.children = children
    def get_value(self):
    	values = map(lambda x: x.get_value(), self.children)
    	print values
        return self.this(values)
