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
#    x = expr(expr_max, [expr(expr_sum, [scalar(1), scalar(3)]),
#                             expr(expr_sum, [scalar(-2), scalar(4)])])
#    y = expr(expr_exp, [x])
#    print y.get_value()
#    print y.__str__()
    
#    x = expr(expr_max, [scalar_var('x'), scalar_var('y')])
#    print x.__str__()
    
#    x = expr_sum(scalar_var('x'), scalar_var('y'))
#    print x.__str__()
