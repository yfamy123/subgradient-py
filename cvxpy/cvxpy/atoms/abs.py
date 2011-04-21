#***********************************************************************#
# Copyright (C) 2010-2011 Tomas Tinoco De Rubira                        #
#                                                                       #
# This file is part of CVXPY                                            #     
#                                                                       #
# CVXPY is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #   
# (at your option) any later version.                                   # 
#                                                                       #
# CVXPY is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#***********************************************************************#

import numpy as np
from cvxpy.defs import *
from cvxpy.constraints import cvxpy_list
from cvxpy.scalars import cvxpy_tree
from cvxpy.interface import less,greater
from cvxpy.arrays import cvxpy_expression

# Class definition
class cvxpy_abs(object):
    """
    Absolute value function.
    Convex.

    :param x: Number, scalar object, :class:`cvxpy_matrix` or array object.
    :rtype: Number, :class:`cvxpy_tree`, :class:`cvxpy_matrix`
            or :class:`cvxpy_expression`.
    """

    # Method: __init__
    def __init__(self):
        self.curvature = CONVEX
        self.expansion_type = PM
        self.type = FUNCTION
        self.atom = True
        self.name = 'abs'

    # Method: __call__
    def __call__(self,*arg):

        # Check number of arguments
        if(len(arg) != 1):
            raise ValueError('Invalid number of arguments')
        
        # Extract argument
        if(type(arg[0]) is list):
            x = arg[0][0]
        else:
            x = arg[0]

        # Process
        if(type(x).__name__ in SCALAR_OBJS):
            return cvxpy_tree(self,[x])
        elif(type(x).__name__ in ARRAY_OBJS):
            (m,n) = x.shape
            new_exp = cvxpy_expression(m,n)
            for i in range(0,m,1):
                for j in range(0,n,1):
                    new_exp[i,j] = self(x[i,j])
            return new_exp
        else:
            return np.abs(x)

    # Method: _pm_expand
    def _pm_expand(self,constr):
        """
        Description: Return the partial minimization 
        expansion of the function. 
        Argument constr: The constraint to be
        replaced. It is assumed to be in expanded
        format so the right hand side is a variable.
        """
        arg = constr.left.children[0]
        right = constr.right
        return cvxpy_list([less(-right,arg),
                           less(arg,right)])

    # Method: monotonicity
    def monotonicity(self,index):
        return NEITHER

    # Method: _range_constr
    def _range_constr(self, v):
        return cvxpy_list([greater(v,0)])
    
    # Method: _dom_constr
    def _dom_constr(self,args):
        return cvxpy_list([])
        
    # Method: _linearize
    def _linearize(self,args,t2):

        # Argument
        t1 = args[0]
        t1_hat = t1.get_value()

        # Subgradient
        if(t1_hat >= 0):
            g = 1.0
        else:
            g = -1.0

        # Return affine approximation
        return t2 - (np.abs(t1_hat) + g*(t1 - t1_hat))
        
# Function instance
abs = cvxpy_abs()
            
