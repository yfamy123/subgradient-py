import math
from scalar import *
from constraint import *
from functions import *

class problem(object):
    def __init__(self, type, obj, constraints):
        assert type in [MINIMIZE, MAXIMIZE]
        #assert (type == MINIMIZE and obj.is_convex()) or (type == MAXIMIZE and obj.is_concave())
        self.type = type
        self.obj = obj
        self.constraints = []
        for cons in constraints:
            if cons.relop != GT:
                self.constraints.append(sum(cons.lhs, prod(scalar(-1), cons.rhs)))
            if cons.relop != LT:
                self.constraints.append(sum(cons.rhs, prod(scalar(-1), cons.lhs)))
        
    def solve(self):
        if self.type == MAXIMIZE:
            self.obj = prod(scalar(-1), self.obj)
        vars = self.obj.get_vars()
        cur = {}
        for var in vars: cur[var] = 0.0
        for iter in range(1, MAXITERS+1):
            g = {}
            for cons in self.constraints:
                if cons.get_value(cur) > 0:
                    g = cons.subgrad(cur)
                    break
            if g == {}: g = self.obj.subgrad(cur)
            norm = math.sqrt(sum([x**2 for x in g.itervalues()]))
            if norm < EPS: break
            nxt = {}
            for (key, val) in g.iteritems():
                nxt[key] = cur[key]-1.0*val/iter;
            cur = nxt
        if self.type == MAXIMIZE:
            self.obj = prod(scalar(-1), self.obj)
        print 'objective value: ' + str(self.obj.get_value(cur))
        print 'optimal point: '
        for key, val in cur.iteritems():
            print key + ': ' + str(val)
        