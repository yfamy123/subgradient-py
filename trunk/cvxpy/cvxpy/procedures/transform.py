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
from cvxpy.constraints import cvxpy_list
from cvxpy.interface import less,greater

# Function
def transform(constr_list):
    """
    Description 
    -----------
    Transforms nonlinear equality constraints
    to equivalent form involving two inequalities.

    Arguments
    ---------
    constr_list: cvxpy_list of constraints in 
    expanded form so that all nonlinear constraints
    are equalities.
    """

    # New list
    new_list = cvxpy_list([])

    # Transform
    for constr in constr_list:

        # Function
        if(constr.left.type == TREE and
           constr.left.item.type == FUNCTION):

            # Get function
            fn = constr.left.item

            # Get equivalent transformation
            new_constr = cvxpy_list([less(constr.left,constr.right),
                                     greater(constr.left,constr.right)])
        
            # Append
            new_list += cvxpy_list(new_constr)
        
        # Not a function
        else:
            
            # Append
            new_list += cvxpy_list([constr])
            
    # Return transformed list
    return new_list
            
                                          
