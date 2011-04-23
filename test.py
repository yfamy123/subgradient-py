#!/usr/bin/env python

from functions.sum import *
from functions.exp import *
if __name__ == "__main__":
    x = expr_sum([3, 4])
    print x
    x = expr_sum([scalar(3), scalar(4)])
    print x
    x = expr_exp(expr_sum(scalar_var('x'), scalar_var('y')))
    print x
    print x.get_vars()
