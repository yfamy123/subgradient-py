if __name__ == "__main__":
    from expr import *
    from expr_sum import *
    from expr_max import *
    from exp import *
    x = expr_tree(expr_max, [expr_tree(expr_sum, [expr(1), expr(3)]),
                             expr_tree(expr_sum, [expr(-2), expr(4)])])
    print x.get_value()
