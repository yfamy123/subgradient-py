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
import cvxopt as opt
from cvxpy.defs import *
from cvxpy.constraints import cvxpy_list
from cvxpy.scalars import cvxpy_tree
from cvxpy.interface import greater
from cvxpy.arrays import cvxpy_expression

# Class definition
class cvxpy_square(object):
    """
    Square function.
    Convex.

    :param x: Number, scalar object, :class:`cvxpy_matrix` or array object.
    :rtype: Number, :class:`cvxpy_tree`, :class:`cvxpy_matrix`
            or :class:`cvxpy_expression`.
    """

    # Method: __init__
    def __init__(self):
        self.curvature = CONVEX
        self.expansion_type = SDC
        self.type = FUNCTION
        self.atom = True
        self.name = 'square'

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
            return np.square(x)

    # Method: _construct
    def _construct(self,args,t2,mp,n):
        """
        Description: Constructs the epygraph of
        this functions by means of an inequality
        with respect to the semidefinite cone.
        Argument args: List of arguments.
        Argument t2: Variable from the right side
        of the inequality.
        Argument mp: Map from variables to indeces.
        Argument n: Number of variables.
        """

        # Get argument
        t1 = args[0]
        
        # Construct G,h
        G = opt.spmatrix(0.0,[],[],(4,n))
        h = opt.matrix(0.0,(4,1))
        G[0,mp[t2]] = -1.0
        G[1,mp[t1]] = -1.0
        G[2,mp[t1]] = -1.0
        h[3,0] = 1.0
        
        # Return
        return G,h,2

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

        # Return affine approximation
        return t2 - (np.square(t1_hat) + 2*t1_hat*(t1-t1_hat))

# Function instance
square = cvxpy_square()
