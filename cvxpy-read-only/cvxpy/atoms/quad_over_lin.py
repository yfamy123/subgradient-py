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
from cvxpy.utils import *
from cvxpy.sets import *
from cvxpy.interface import *
from cvxpy.arrays import cvxpy_matrix

# Quadratic overer linear
def quad_over_lin(x,y):
    """
    Quadratic over linear function :math:`x^Tx/y`.
    Convex and decreasing in y.

    :param x: Number, scalar object, column :class:`cvxpy_matrix` 
              or object array.
              If y is a scalar object, the constraint :math:`y > 0`
              is imposed.
    :param y: Positive number or scalar object.
    :rtype: Number of :class:`cvxpy_tree`
    """

    # Prepare x
    if(np.isscalar(x) or type(x).__name__ in SCALAR_OBJS):
        x = vstack([x])
    elif(type(x) is not cvxpy_matrix and 
         type(x).__name__ not in ARRAY_OBJS):
        raise ValueError('Invalid first argument')
    elif(x.shape[1] != 1):
        raise ValueError('Invalid first argument')
    
    # Check y
    if(not np.isscalar(y) and 
       type(y).__name__ not in SCALAR_OBJS):
        raise ValueError('Invalid second argument')

    # Construct objective and constraints
    n = x.shape[0]
    a = param('a',n,1)
    b = param('b')

    v = var('v') # Extra variable needed since y mey be concave
    # and set inclusion only accepts affine arguments

    t = var('t')
    TopBlock = hstack((diagflat(v*ones((1,n))),a))
    if(n == 1):
        BottomBlock = hstack((a,t))
    else:
        BottomBlock = hstack((a.T,t))
    A = vstack((TopBlock,BottomBlock))
    obj = t
    constr = [belongs(A,sdc(n+1)),greater(b,v)]
    
    # Check that y>0 if y is numeric
    if((type(y).__name__ not in SCALAR_OBJS) and y <= 0):
        raise ValueError('Invalid second argument')
    
    # Construct and return program
    p = prog(minimize(obj),
             constr,
             [a,b],
             None,
             'quad_over_lin')
    return p(x,y)
