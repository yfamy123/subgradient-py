from spy.scalar import *
from spy.constraint import *
from spy.problem import *
from spy.constants import *

__all__ = ["var", "less", "equal", "greater", "minimize", "maximize"]
def var(name): return scalar_var(name)

def less(lhs, rhs):
    return constraint(lhs, LT, rhs)
def equal(lhs, rhs):
    return constraint(lhs, EQ, rhs)
def greater(lhs, rhs):
    return constraint(lhs, GT, rhs)

def minimize(obj, constraints):
    return problem(MINIMIZE, obj, constraints)
def maximize(obj, constraints):
    return problem(MAXIMIZE, obj, constraints)
