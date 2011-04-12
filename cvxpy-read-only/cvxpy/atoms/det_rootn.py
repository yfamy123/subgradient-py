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
from cvxpy.atoms.geo_mean import geo_mean

# det_rootn
def det_rootn(X):
    """
    :math:`n-th` root of the determinant of a semidefinite matrix.
    Concave.

    :param X: Symmetric :class:`cvxpy_matrix` or square array object.
              If X is an array object, the constraints :math:`A^T = A`,
              and :math:`A \succeq 0` are imposed.
    :rtype: Number of :class:`cvxpy_tree`.
    """

    # Check type
    if(type(X) is not cvxpy_matrix and
       type(X).__name__ not in ARRAY_OBJS):
        raise ValueError('Invalid argument type')

    # Check shape
    (m,n) = X.shape
    if(m!=n):
        raise ValueError('Invalid argument dimensions')

    # Construct objective and constraints
    a = param('a',m,m)
    Z = var('z',m,m,'lower triangular')
    D = diag(Z)
    obj = geo_mean(D)
    constr = [belongs(vstack((hstack((diagflat(D),Z.T)),
                              hstack((Z,a)))),
                      sdc(2*m))]
    
    # Add constraints if argument is not numeric
    if(type(X).__name__ in ARRAY_OBJS):
        constr += [equal(a,a.T),
                   belongs(a,sdc(m))]

    # Check properties if argument is nunmeric
    elif(not np.allclose(X,X.T) or
         np.min(np.linalg.eig(X)[0]) < 0):
        return -np.inf

    # Construct program
    p = prog(maximize(geo_mean(D)),constr,[a],None,'det_rootn')

    # Check redundancy if argument not numeric
    if(type(X).__name__ in ARRAY_OBJS):
        p.options['REL_SOL']['check redundancy'] = True

    # Return program
    return p(X)
         
