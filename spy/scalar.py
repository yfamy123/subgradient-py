from constants import *

# Base class
class expr(object):
    def __init__(self, func = None, children = []):
        self.func     = func
        self.children = children
    def __str__(self):
        strs = map(lambda x: x.__str__(), self.children)
        if(self.func.name == 'sum'):
            ret = '(' + '+'.join(strs) + ')'
        else:
            ret = self.func.name + '(' + ', '.join(strs) + ')'
        return ret
    def get_value(self, varmap = {}):
    	values = map(lambda x: x.get_value(varmap), self.children)
        return self.func(values)
    def get_vars(self):
        ret = set()
        for child in self.children:
            ret = ret.union(child.get_vars())
        return ret
    def subgrad(self, varmap = {}):
        # composition rule
        # f(x) = h(f1(x), f2(x), ..., fk(x))
        # find q in subgrad h(f1(x), ..., fk(x))
        # find gi in subgrad fi(x)
        # return q1g1 + q2g2 + ... + qkgk
        
        values = map(lambda x: x.get_value(varmap), self.children)
        q = self.func.subgrad(values)
        # q is a list of numbers
        subgrads = map(lambda x: x.subgrad(varmap), self.children)
        # subgrads is a list of maps
        # now return the "weighted sum" of the maps
        ret = {}
        for var in varmap:
            ret[var] = sum(q[i]*subgrads[i][var] for i in range(len(q)))
        return ret

# Scalar constant
class scalar(expr):
    def __init__(self, value = None):
        self.value = value
    def __str__(self):
        return str(self.value)
    def get_value(self, varmap = {}):
        return self.value
    def get_vars(self):
        return set()
    def subgrad(self, varmap = {}):
        # subgradient of a constant is constant
        ret = {}
        for var in varmap:
            ret[var] = 0
        return ret

# Scalar variable
class scalar_var(expr):
    def __init__(self, name = None, value = NAN):
        self.name  = name
        self.value = value
    def __str__(self):
        return self.name
    def get_value(self, varmap = {}):
        if self.name in varmap:
            return varmap[self.name]
        return NAN
    def get_vars(self):
        return set(self.name)
    def set_value(self, value):
        self.value = value
    def subgrad(self, varmap = {}):
        if(self.name in varmap):
            ret = {}
            for var in varmap:
                ret[var] = 0
            ret[self.name] = 1
            return ret
        else:
            return {}
