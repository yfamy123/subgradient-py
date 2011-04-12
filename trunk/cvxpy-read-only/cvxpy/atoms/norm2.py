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

from cvxpy.sets import *
from cvxpy.utils import *
from cvxpy.interface import *

# Norm 2
def norm2(x):
    """
    :math:`l_2` norm.
    Convex.
    
    :param x: Column vector.
    :type x: :class:`cvxpy_matrix` or array object
    :rtype: Number or :class:`cvxpy_tree`.
    """

    # Check that x is a column vector
    (m,n) = x.shape
    if(n!=1):
        raise ValueError('Invalid argument')
    
    # Construct and return program
    a = param('a',m,1)
    t = var('t')
    p = prog(minimize(t),
             [belongs(vstack((a,t)),soc(m))],
             [a],
             None,
             'norm2')
    return p(x)
