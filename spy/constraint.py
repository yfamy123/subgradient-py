from scalar import *

class constraint(object):
    def __init__(self, lhs, relop, rhs):
        if relop == EQ:
            assert lhs.is_affine() and rhs.is_affine()
        if relop == LT:
            assert lhs.is_convex() and rhs.is_concave()
        if relop == GT:
            assert lhs.is_concave() and rhs.is_convex()
        self.lhs = lhs
        self.rhs = rhs
        self.relop = relop
    def cutting_plane(self, varmap = {}): pass