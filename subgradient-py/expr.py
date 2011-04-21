from defs import *

# Base class
class expr(object):
    def __init__(self, v = None):
        self.value = v
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
    def __init__(self, func, children):
        self.func     = func
        self.children = children
    def get_value(self):
        if(self.func.name == '+'):
            values = map(lambda x: x.get_value(), self.children)
            return sum(values)
        elif(self.func.name == '*'):
            l = self.children[0].get_value()
            r = self.children[1].get_value()
            return l*r
        else:
            values = map(lambda x: x.get_value(), self.children)
            return self.func(values)
