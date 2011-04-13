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
from cvxpy.utils import *
from cvxpy.constraints import cvxpy_list
from cvxpy.scalars import cvxpy_obj,cvxpy_tree

# Class definition
class cvxpy_log_sum_exp(object):
    """
    Log sum exp function.
    Convex and increasing in each argument.

    :param x: Number, scalar object, 1D :class:`cvxpy_matrix`
              of 1D array object.
    :rtype: Number or :class:`cvxpy_tree`.
    """
    
    # Method: __init__
    def __init__(self):
        self.curvature = CONVEX
        self.expansion_type = DIF
        self.type = FUNCTION
        self.atom = True
        self.name = 'log_sum_exp'

    # Method: __call__
    def __call__(self,*arg):

        # Check number of arguments
        if(len(arg) != 1):
            raise ValueError('Invalid number of arguments')

        # Extract argument
        if(type(arg[0]) is list):
            x = hstack(arg[0])
        else:
            x = arg[0]

        # Process
        if(type(x).__name__ in SCALAR_OBJS):
            return x
        elif(type(x).__name__ in ARRAY_OBJS):
            (m,n) = x.shape
            if(m != 1 and n != 1):
                raise ValueError('Argument must be 1-Dimensional')
            children = []
            for i in range(0,m,1):
                for j in range(0,n,1):
                    if(np.isscalar(x[i,j])):
                        children += [cvxpy_obj(CONSTANT,x[i,j],str(x[i,j]))]
                    else:
                        children += [x[i,j]]
            return cvxpy_tree(self,children)
        else: 
            return np.log(np.sum(np.exp(x)))

    # Method: _construct
    def _construct(self,args,t2,mp,n):
        """
        Description: Construct f, grad f, hessian f and the 
        characteristic function of the domain of f needed by cvxopt
        to solve the optimization problem.
        Argument args: List of arguments for the function.
        Argument t2: Variable from the right hand side of the
        inequality.
        Argument mp: Map from variable to index in vecto x.
        Argument n: Number of variables. This is the size of 
        vector that will be the input of f, grad f and hessian f.
        """

        # f
        def f(x):
            s = 0
            for a in args:
                if(type(a) is cvxpy_obj):
                    s += np.exp(a.get_value())
                else:
                    s += np.exp(x[mp[a]])
            return np.log(s) - x[mp[t2]]

        # grad f
        def grad_f(x):
            g = opt.spmatrix(0.0,[],[],(n,1))
            
            # denom
            d = 0
            for a in args:
                if(type(a) is cvxpy_obj):
                    d += np.exp(a.get_value())
                else:
                    d += np.exp(x[mp[a]])
            
            # g
            for a in args:
                if(type(a) is not cvxpy_obj):
                    g[mp[a]] = (1./d)*np.exp(x[mp[a]])
            g[mp[t2]] = -1
            return g

        # hess f
        def hess_f(x):
            h = opt.spmatrix(0.0,[],[],(n,n))

            # denom
            d1 = 0
            for a in args:
                if(type(a) is cvxpy_obj):
                    d1 += np.exp(a.get_value())
                else:
                    d1 += np.exp(x[mp[a]])
            d2 = d1**2

            # h
            for a1 in [a for a in args if type(a) is not cvxpy_obj]:
                for a2 in [a for a in args if type(a) is not cvxpy_obj]:
                    if(a1 == a2):
                        t = np.exp(x[mp[a1]])
                        h[mp[a1],mp[a1]] = t*(d1-t)/d2
                    else:
                        t = (-1./d2)*np.exp(x[mp[a1]]+x[mp[a2]])
                        h[mp[a1],mp[a2]] = t
                        h[mp[a2],mp[a1]] = t
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
        return cvxpy_list([])
    
    # Method: _dom_constr
    def _dom_constr(self,args):
        return cvxpy_list([])

    # Method: _linearize
    def _linearize(self,args,t2):
        
        n = len(args)
        x_hat = zeros((0,1))
        grad = zeros((0,1))
        x = zeros((0,1))
        d = 0
        for a in args:
            x_hat = vstack((x_hat,a.get_value()))
            d += np.exp(a.get_value())
            if(type(a) is cvxpy_obj):
                grad = vstack((grad,0))
                x = vstack((x,a.get_value()))
            else:
                grad = vstack((grad,np.exp(a.get_value())))
                x = vstack((x,a))
        grad = grad/d
        return t2-(self(x_hat)+grad.T*(x-x_hat))

# Function instance
log_sum_exp = cvxpy_log_sum_exp()
    
