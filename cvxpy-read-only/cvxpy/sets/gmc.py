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
from cvxpy.scalars import cvxpy_obj
from cvxpy.constraints import cvxpy_list
from cvxpy.sets import sdc
from cvxpy.interface import belongs,var,greater
from cvxpy.utils import vstack,hstack

# Class definition
class cvxpy_gmc(object):
    """
    Geometric mean cone
    :math:`\{(x,y) \in R^n \\times R \ | \ x \ge 0, \ \prod_{i=1}^{n}x_i \ge y
    \}`

    :param n: Positive integer.
    :returns: Set instance.
    """

    # Method: __init__
    def __init__(self,n):
        self.type = SET
        self.name = 'gmc'
        self.shape = (n+1,1)
        self.expansion_type = PM

    # Method: __str__
    def __str__(self):
        return self.name+'('+str(self.shape[0]-1)+')'

    # Method: _pm_expand
    def _pm_expand(self,constr):
        
        # Get shape
        v = constr.left
        n = v.shape[0]-1
        x = v[0:n,0]
        y = v[n,0]
        z = var()

        # Get power of 2 size
        m = 0
        while (np.log2(n+m) % 1 != 0):
            m = m + 1

        # Copy elements of x on a list and restrict them
        constr_list = []
        el_list = []
        for i in range(0,n,1):
            el_list+=[x[i,0]]
            if(not np.isscalar(x[i,0]) and
               type(x[i,0]) is not cvxpy_obj):
                constr_list += [greater(x[i,0],0)]

        # Construct expansion
        z = var()
        for i in range(0,m,1):
            el_list += [z]
        while(len(el_list) > 2):
            new_list = []
            for i in range(0,len(el_list)/2):
                x1 = el_list[2*i]
                x2 = el_list[2*i+1]
                w = var()
                constr_list += [belongs(vstack((hstack((x1,w)),
                                                hstack((w,x2)))),
                                        sdc(2))]
                new_list += [w]
            el_list = new_list
        x1 = el_list[0]
        x2 = el_list[1]
        constr_list += [belongs(vstack((hstack((x1,z)),
                                        hstack((z,x2)))),
                                sdc(2))]
        constr_list += [greater(z,0),greater(z,y)]
        return cvxpy_list(constr_list)

# Set interface name
gmc = cvxpy_gmc
