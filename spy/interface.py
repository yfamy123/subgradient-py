from spy.scalar import *
from spy.constraint import *
from spy.problem import *
from spy.constants import *
#from spy.matrix import *

__all__ = ["var", "leq", "eq", "geq", "minimize", "maximize"]
def var(name, m = 1, n = 1):
    if m == 1 and n == 1: return scalar_var(name)
    if n == 1: return vector_var(name, m)
    return matrix_var(name, m, n)

def leq(lhs, rhs):
    return constraint(lhs, LT, rhs)
def eq(lhs, rhs):
    return constraint(lhs, EQ, rhs)
def geq(lhs, rhs):
    return constraint(lhs, GT, rhs)

def minimize(obj, constraints):
    return problem(MINIMIZE, obj, constraints)
def maximize(obj, constraints):
    return problem(MAXIMIZE, obj, constraints)
