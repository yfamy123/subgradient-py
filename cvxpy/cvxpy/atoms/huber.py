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
from cvxpy.atoms.abs import abs
from cvxpy.atoms.square import square
from cvxpy.interface import *

# Huber 
def huber(x,M):
    """
    Huber penalty function with parameter M.
    Convex.

    :param x: Number or scalar object.
    :param M: Positive constant.
    :rtype: Number or :class:`cvxpy_tree`.
    """

    # x must be scalar
    if((not np.isscalar(x)) and
       type(x).__name__ not in SCALAR_OBJS):
        raise ValueError('Invalid first argument')

    # M must be a positive constant
    if((not np.isscalar(M)) or M <= 0):
        raise ValueError('Invalid second argument')

    # Construct and return program
    v = var('v')
    w = var('w')
    a = param('a')
    p = prog(minimize(2*v+square(w)),
             [less(abs(a),w+v),
              greater(v,0),
              greater(w,0),
              less(w,1)],
             [a],None,'huber') 
    return square(M)*p((1.0/M)*x)

