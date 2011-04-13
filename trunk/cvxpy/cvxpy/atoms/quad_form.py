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
from cvxpy.utils import *
from cvxpy.atoms.square import square
from cvxpy.interface import *

# Quadratic form
def quad_form(x,P):
    """
    Quadratic form :math:`x^TPx`.
    Convex.

    :param x: Column vector.
    :type x: :class:`cvxpy_matrix` or array object
    :param P: Positive semidefinite matrix.
    :type P: :class:`cvxpy_matrix`
    :rtype: number or :class:`cvxpy_tree`.
    """

    # P must be symmetric
    if(not np.allclose(P,P.T)):
        raise ValueError('Invalid second argument')

    # P must be positive semidefinite
    min_eig = np.min(np.linalg.eig(P)[0])
    if(min_eig < 0.0):
        raise ValueError('Invalid second argument')
    P_half = sqrtm(P)
    (m,n) = x.shape

    # x must be a column vector
    if(n!=1):
        raise ValueError('Invalid first argument')

    # Construct and return program
    a = param('a',m,1)
    t = var('t')
    p = prog(minimize(t),
             [less(sum(square(sqrtm(P)*a)),t)],
             [a],
             None,
             'quad_form')
    return p(x)
