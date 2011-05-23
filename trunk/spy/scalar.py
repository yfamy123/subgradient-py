from spy.constants import *
from spy.utils import *
import __builtin__

# Base class for scalar-valued expression
class expr(object):
    def __init__(self, func = None, children = []):
        self.func     = func
        self.children = children
    def __str__(self):
        strs = map(lambda x: x.__str__(), self.children)
        if self.func == '+':
            ret = '(' + '+'.join(strs) + ')'
        elif self.func == '*':
            ret = '*'.join(strs)
        else:
            ret = self.func.name + '(' + ', '.join(strs) + ')'
        return ret
    def get_value(self, varmap = {}):
    	values = map(lambda x: x.get_value(varmap), self.children)
        if self.func == '+': return __builtin__.sum(values)
        elif self.func == '*': return values[0]*values[1]
        return self.func(values)
    def get_vars(self):
        ret = set()
        for child in self.children:
            ret = ret.union(child.get_vars())
        return ret

    # can multiply by constant only
    # warning: the first argument is an expression, the second is a scalar
    def __mul__(self, other):
        assert isNumber(other)
        if other == 1.0: return self
        if other == 0.0: return 0.0
        return expr('*', [self, scalar(other)])
    def __rmul__(self, other):
        assert isNumber(other)
        if other == 1.0: return self
        if other == 0.0: return 0.0
        return expr('*', [self, scalar(other)])
    def __neg__(self):
        return (-1.0)*self

    def __add__(self, other):
        if isNumber(other): other = scalar(other)
        return expr('+', [self, other])
    def __radd__(self, other):
        if isNumber(other): other = scalar(other)
        return expr('+', [other, self])
    def __sub__(self, other):
        if isNumber(other): return expr('+', [self, scalar(-other)])
        return expr('+', [self, -other])
    def __rsub__(self, other):
        if isNumber(other): other = scalar(other)
        return expr('+', [other, -self])
    
    def subgrad(self, varmap = {}):
        if self.func == '+':
            subgrads = map(lambda x: x.subgrad(varmap), self.children)
            ret = {}
            for var in varmap:
                ret[var] = sum(subgrad[var] for subgrad in subgrads)
            return ret
        if self.func == '*': # first arg is expression, second is scalar
            c = self.children[1].get_value()
            if c > 0: q = self.children[0].subgrad(varmap)
            else: q = self.children[0].supergrad(varmap)
            ret = {}
            for var in varmap:
                ret[var] = q[var]*c
            return ret

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

    def supergrad(self, varmap = {}):
        if self.func == '+':
            supergrads = map(lambda x: x.supergrad(varmap), self.children)
            ret = {}
            for var in varmap:
                ret[var] = sum(supergrad[var] for supergrad in supergrads)
            return ret
        if self.func == '*': # first arg is expression, second is scalar
            c = self.children[1].get_value()
            if c > 0: q = self.children[0].supergrad(varmap)
            else: q = self.children[0].subgrad(varmap)
            ret = {}
            for var in varmap:
                ret[var] = q[var]*c
            return ret

        # composition rule
        # f(x) = h(f1(x), f2(x), ..., fk(x))
        # find q in subgrad h(f1(x), ..., fk(x))
        # find gi in subgrad fi(x)
        # return q1g1 + q2g2 + ... + qkgk
        
        values = map(lambda x: x.get_value(varmap), self.children)
        q = self.func.subgrad(values)
        # q is a list of numbers
        supergrads = map(lambda x: x.supergrad(varmap), self.children)
        # subgrads is a list of maps
        # now return the "weighted sum" of the maps
        ret = {}
        for var in varmap:
            ret[var] = sum(q[i]*supergrads[i][var] for i in range(len(q)))
        return ret
    def is_convex(self):
        if self.func == '+':
            for child in self.children:
                if not child.is_convex(): return False
            return True
        if self.func == '*':
            if self.children[1].get_value() > 0: return self.children[0].is_convex()
            return self.children[0].is_concave()

        if self.func.is_convex() == False:
            return False
        convexity = map(lambda x: x.is_convex(), self.children)
        concavity = map(lambda x: x.is_concave(), self.children)
        for i in xrange(len(self.children)):
            if convexity[i] and concavity[i]:
                continue
            if convexity[i] and self.func.is_increasing(i):
                continue
            if concavity[i] and self.func.is_decreasing(i):
                continue
            return False
        return True
    def is_concave(self):
        if self.func == '+':
            for child in self.children:
                if not child.is_concave(): return False
            return True
        if self.func == '*':
            if self.children[1].get_value() > 0: return self.children[0].is_concave()
            return self.children[0].is_convex()

        if self.func.is_concave() == False:
            return False
        convexity = map(lambda x: x.is_convex(), self.children)
        concavity = map(lambda x: x.is_concave(), self.children)
        for i in xrange(len(self.children)):
            if not (convexity[i] and concavity[i]):
                continue
            if convexity[i] and self.func.is_increasing(i):
                continue
            if concavity[i] and self.func.is_decreasing(i):
                continue
            return False
        return True
    def is_affine(self):
        return self.is_convex() and self.is_concave()

# Scalar constant
class scalar(expr):
    def __init__(self, value = None):
        self.value = value
    def __str__(self):
        return str(self.value)
    def get_value(self, varmap = {}):
        return float(self.value)
    def get_vars(self):
        return set()
    def subgrad(self, varmap = {}):
        # subgradient of a constant is constant
        ret = {}
        for var in varmap:
            ret[var] = 0.0
        return ret
    def supergrad(self, varmap = {}):
        # supergradient of a constant is constant
        ret = {}
        for var in varmap:
            ret[var] = 0.0
        return ret
    def is_convex(self): return True
    def is_concave(self): return True

# Scalar variable
class scalar_var(expr):
    def __init__(self, name = None):
        self.name  = name
    def __str__(self):
        return self.name
    def get_value(self, varmap = {}):
        if self.name in varmap:
            return varmap[self.name]
        return NAN
    def get_vars(self):
        return set([self.name])
    def subgrad(self, varmap = {}):
        ret = {}
        if self.name in varmap:
            for var in varmap:
                ret[var] = 0.0
            ret[self.name] = 1.0
        else:
            for var in varmap:
                ret[var] = NAN
        return ret
    def supergrad(self, varmap = {}):
        ret = {}
        if self.name in varmap:
            for var in varmap:
                ret[var] = 0.0
            ret[self.name] = 1.0
        else:
            for var in varmap:
                ret[var] = NAN
        return ret
    def is_convex(self): return True
    def is_concave(self): return True
