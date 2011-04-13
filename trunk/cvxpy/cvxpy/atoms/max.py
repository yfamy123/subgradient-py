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
from cvxpy.scalars import cvxpy_tree,cvxpy_obj
from cvxpy.interface import less
from cvxpy.arrays import cvxpy_expression
from cvxpy.utils import hstack

# Class definition
class cvxpy_max(object):
    """
    Max function.
    Convex and increasing in each argument.

    :param x: Number, scalar object, 1D :class:`cvxpy_matrix` 
              or 1D array object.
    :rtype: Number or :class:`cvxpy_tree`.
    """

    # Method: __init__
    def __init__(self):
        self.curvature = CONVEX
	self.expansion_type = PM
        self.type = FUNCTION
	self.atom = True
        self.name = 'max'

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
            return np.max(x)
        
    # Method: _pm_expand
    def _pm_expand(self,constr):
	"""
	Description
        -----------
        Return the partial minimization 
        expansion of the function. 
	
        Argument
        --------
        constr: The constraint to be replaced. 
        It is assumed the constraint was expanded
        and transformed so that the right hand side 
        is a variable.
	"""
        new_list = []
        for arg in constr.left.children:
            if(type(arg) is cvxpy_obj):
                arg = arg.get_value()
            new_list += [less(arg,constr.right)]
        return cvxpy_list(new_list)

    # Method: monotonicity
    def monotonicity(self,index):
        return INCREASING

    # Method: _range_constr
    def _range_constr(self, v):
        return cvxpy_list([])

    # Method: _dom_constr
    def _dom_constr(self,args):
        return cvxpy_list([])

    # Method: _linearize
    def _linearize(self,args,t3):

        # Find max index
        values = map(lambda x:x.get_value(),args)
        max_index = np.argmax(values)

        # Return linearization
        if(args[max_index].type == VARIABLE):
            return t3-args[max_index]
        else:
            return t3-values[max_index]

# Function instance
max = cvxpy_max()
