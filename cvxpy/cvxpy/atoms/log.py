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
from cvxpy.interface import greater
from cvxpy.arrays import cvxpy_expression
from exp import *

# Class definition
class cvxpy_log(object):
    """
    Logarithmic function.
    Concave and increasing.

    :param x: Number, scalar object, :class:`cvxpy_matrix` or array object.
    :rtype: Number, :class:`cvxpy_tree`, :class:`cvxpy_matrix`
            or :class:`cvxpy_expression`.
    """

    # Method: __init__
    def __init__(self):
        self.curvature = CONCAVE
	self.expansion_type = DIF
        self.type = FUNCTION
	self.atom = True
        self.name = 'log'

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
            return np.log(x)

    # Method: monotonicity
    def monotonicity(self,index):
        return INCREASING

    # Method: _range_constr
    def _range_constr(self,v):
        return cvxpy_list([])

    # Method: _dom_constr
    def _dom_constr(self,args):
        arg = args[0]
        return cvxpy_list([greater(arg,0)])

    # Method: _construct
    def _construct(self,args,t2,mp,n):
        #t1 = args[0]
        #return exp.construct([t2],t1,mp,n)

        # Get argument
        t1 = args[0]

        # f
        def f(x):
            return x[mp[t2]] - np.log(x[mp[t1]])

        # grad f
        def grad_f(x):
            g = opt.spmatrix(0.0,[],[],(n,1))
            g[mp[t1]] = -1.0/(1.0*x[mp[t1]])
            g[mp[t2]] = 1.0
            return g

        # hess f
        def hess_f(x):
            h = opt.spmatrix(0.0,[],[],(n,n))
            h[mp[t1],mp[t1]] = 1.0/((x[mp[t1]])**2.0)
            return h
    
        # ind f (in domain of f)
        def ind_f(x):
            if(x[mp[t1]] > 0):
                return True
            else:
                return False
        
        # Return functions
        return f,grad_f,hess_f,ind_f
        
    # Method: _linearize
    def _linearize(self,args,t2):
        t1 = args[0]
        return exp._linearize([t2],t1)

# Function instance
log = cvxpy_log()
