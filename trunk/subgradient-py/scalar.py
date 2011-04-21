from defs import *

# Base class
class expr(object):
    def __init__(self, func = None, children = []):
        self.func     = func
        self.children = children
    def get_value(self, varmap = {}):
    	values = map(lambda x: x.get_value(varmap), self.children)
        return self.func(values)
    def get_vars(self):
        varsets = map(lambda x: x.get_vars(), self.children)
        ret = set()
        for varset in varsets:
            ret = ret.union(varset)
        return ret
    def subgrad(self, varmap):
        return 0
    def __str__(self):
        strs = map(lambda x: x.__str__(), self.children)
        if(self.func.name == 'sum'):
            ret = '(' + '+'.join(strs) + ')'
        else:
            ret = self.func.name + '(' + ', '.join(strs) + ')'
        return ret

# Scalar constant
class scalar(expr):
    def __init__(self, value = None):
        self.value = value
    def get_value(self, varmap = {}):
        return self.value
    def get_vars(self):
        return set()
    def subgrad(self, varmap):
        return 0
    def __str__(self):
        return str(self.value)

# Scalar variable
class scalar_var(expr):
    def __init__(self, name = None, value = NAN):
        self.name  = name
        self.value = value
    def get_value(self, varmap = {}):
        if self.name in varmap:
            return varmap[self.name]
        return NAN
    def get_vars(self):
        return set(self.name)
    def set_value(self, value):
        self.value = value
    def __str__(self):
        return self.name
