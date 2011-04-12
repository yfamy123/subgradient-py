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

# Geometric Mean
def geo_mean(x):
    """
    Gemetric mean function :math:`(x_1x_2...x_n)^{1/n}`.
    Concave and increasing in each argument. 

    :param x: Column vector.
              If x is an array object, the constraint :math:`x \ge 0` 
              is imposed. 
    :type x: Positive :class:`cvxpy_matrix` or array object
    :rtype: Number or :class:`cvxpy_tree`.
    """

    # Get shape
    (m,n) = x.shape

    # x must be a vector
    if(n!=1):
        raise ValueError('Invalid argument')

    # Construct program
    a = param('a',m,1)
    v = var('v',m,1) # Extra variable needed for detecting DCP
    t = var('t')
    p = prog(maximize(t),
             [belongs(vstack((v,t)),gmc(m)),
              greater(a,v)],
             [a], 
             None,
             'geo_mean')
    return p(x)
