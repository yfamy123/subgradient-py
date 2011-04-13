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
from cvxpy.sets import *
from cvxpy.utils import *
from cvxpy.interface import *
from cvxpy.arrays import cvxpy_matrix

# Lambda min
def lambda_min(A):
    """
    Minimum eigenvalue of a symmetric matrix.
    Concave.
    
    :param A: Symmetric :class:`cvxpy_matrix` or square array object.
              If A is an array object, the constraint :math:`A^T = A` 
              is imposed.
    :rtype: Number or :class:`cvxpy_tree`.
    """

    # Check type
    if(type(A) is not cvxpy_matrix and
       type(A).__name__ not in ARRAY_OBJS):
        raise ValueError('Invalid argument type')

    # Check shape
    (m,n) = A.shape
    if(m!=n):
        raise ValueError('Invalid argument dimensions')
    
    # Construct objective and constraints
    a = param('a',m,m)
    x = var('x')
    obj = x
    constr = [belongs(a-x*eye(n),sdc(m))]

    # Add symmetry constraint if input is not numeric
    if(type(A).__name__ in ARRAY_OBJS):
        constr += [equal(a,a.T)]

    # Check symmetry if input is numeric
    elif(not np.allclose(A,A.T)):
        return -np.inf
     
    # Construct and return problem
    p = prog(maximize(obj),constr,[a],None,'lambda_min')
    
    # Check redundancy if  symmetry constr. added
    if(type(A).__name__ in ARRAY_OBJS):
        p.options['REL_SOL']['check redundancy'] = True
    
    # Return program
    return p(A)
