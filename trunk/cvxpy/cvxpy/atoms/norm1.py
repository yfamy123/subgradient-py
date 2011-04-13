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

from cvxpy.defs import *
from cvxpy.interface import *
from cvxpy.utils import *
from cvxpy.atoms.abs import abs
from cvxpy.arrays import cvxpy_matrix

# Norm 1
def norm1(x):
    """
    :math:`l_1` norm. 
    Convex. 
    
    :param x: :class:`cvxpy_matrix` or array object.
    :rtype: Number or :class:`cvxpy_tree`.
    """
    
    # x must be matrix or array object
    if(type(x) is not cvxpy_matrix and
       type(x).__name__ not in ARRAY_OBJS):
        raise ValueError('Invalid argument')

    # Construct and return program
    (m,n) = x.shape
    t = var('t')
    a = param('a',m,n)
    p = prog(minimize(t),
             [less(sum(abs(a)),t)],
             [a],
             None,
             'norm1')
    return p(x)

