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
class cvxpy_exp(object):
    """
    Exponential function.
    Convex and increasing.

    :param x: Number, scalar object, :class:`cvxpy_matrix` or array object.
    :rtype: Number, :class:`cvxpy_tree`, :class:`cvxpy_matrix`
            or :class:`cvxpy_expression`.
    """

    # Method: __init__
    def __init__(self):
        self.curvature = CONVEX
	self.expansion_type = DIF
        self.type = FUNCTION
	self.atom = True
        self.name = 'exp'

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
            return np.exp(x)

    # Method: _construct
    def _construct(self,args,t2,mp,n):
	"""
	Description: Constructs f,grad f, hessian f
	and the characteristic function of the domain of f
	needed by cvxopt to solve the optimization problem.
	Argument args: List of arguments for the function.
	Argument t2: Variable from the right hand side of the
	inequality.
	Argument mp: Map from variable to index in vector x.
	Argument n: Number of variables. This is the size of
	vector that will be the input to f, grad f and hessian f.
	"""

        # Get argument
        t1 = args[0]

        # f
        def f(x):
            return np.exp(x[mp[t1]])-x[mp[t2]]

        # grad f
        def grad_f(x):
            g = opt.spmatrix(0.0,[],[],(n,1))
            g[mp[t1]] = np.exp(x[mp[t1]])
            g[mp[t2]] = -1.0
            return g

        # hess f
        def hess_f(x):
            h = opt.spmatrix(0.0,[],[],(n,n))
            h[mp[t1],mp[t1]] = np.exp(x[mp[t1]])
            return h
    
        # ind f (in domain of f)
        def ind_f(x):
            return True
        
        # Return functions
        return f,grad_f,hess_f,ind_f

    # Method: monotonicity
    def monotonicity(self,index):
        return INCREASING

    # Method: _range_constr
    def _range_constr(self,v):
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
        return t2 - (np.exp(t1_hat)+np.exp(t1_hat)*(t1-t1_hat))

# Function instance
exp = cvxpy_exp()
