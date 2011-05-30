import unittest
import math
from spy import *

class TestDCP(unittest.TestCase):
    def setUp(self):
        pass



    def test_affine(self):
        x = var ('x')
        a = 3;
        b = -2;
        leq(a*x+b,0)
        pass

    def test_sum(self):
        x = var ('x')
        y = var ('y')
        leq(x+y,0)
        pass

    def test_exp(self):#e^(ax)
        x = var ('x')
        a = 3
        leq(exp(3*x),0)
        pass
    
    

    def test_square(self):#square(affine argument) is convex
        x = var ('x')
        y = var ('y')
        less(square(x+y),0)
        self.assertRaises(AssertionError,less,square(square(x+y)),0)#not DCP convex
        #use square_pos instead
        less(square_pos(square(x+y)),0)

    def test_max(self):
        x = var ('x')
        y = var ('y')
        less(max(3*x+y,square(y)),0)
        less(-min(max(x,y),4*x),0)
        
    def test_quad_over_linear(self):#(x+y)^2/sqrt(y)
        x = var ('x')
        y = var ('y')
        #self.assertRaises(AssertionError,less,square(x+y)/sqrt(y)),0)
        less(quad_over_lin(square(x+y),sqrt(y)),0)

    def test_log_sum_exp(self):
        x = var('x')
        y = var('y')
        z = var('z')
        less(log_sum_exp(x,0)-x,0)
        less(max(log_sum_exp(x,y,z),log_sum_exp(x,y)),0)

    def test_non_convex(self):
        x = var('x')
        y = var('y')
        self.assertRaises(AssertionError, less, exp(log(x)),0)
        self.assertRaises(AssertionError, less, 1-exp(x),0);
        self.assertRaises(AssertionError, less, sqrt(2*x+y),0)
        self.assertRaises(AssertionError, less, quad_over_lin(sqrt(x),y),0)
        #self.assertRaises(AssertionError, less, power(x,3),0)
if __name__=='__main__':
    unittest.main()
