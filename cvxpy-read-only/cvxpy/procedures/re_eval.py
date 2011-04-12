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
from cvxpy.utils import sum
from cvxpy.constraints import cvxpy_constr,cvxpy_list
from cvxpy.scalars import cvxpy_obj,cvxpy_scalar_var
from cvxpy.scalars import cvxpy_scalar_param,cvxpy_tree
from cvxpy.interface import less,equal,greater,belongs
from cvxpy.arrays import cvxpy_expression,cvxpy_var,cvxpy_param

# Function Eval Tree
def re_eval(arg,param_map):
    """
    Description
    -----------
    Replaces parameters found in arg using the param_map
    and re-evaluates the resulting object.
    
    Arguments
    ---------
    arg: Argument to be re-evaluated.
    param_map: Dictionery that maps the parameters 
    to objects.
    """

    # Number
    if(np.isscalar(arg)):
        return arg
    
    # Constant object
    elif(type(arg) is cvxpy_obj):
        return arg.get_value()
    
    # Scalar variable
    elif(type(arg) is cvxpy_scalar_var):
        return arg
    
    # Scalar param
    elif(type(arg) is cvxpy_scalar_param):
        return re_eval(param_map[arg],param_map)

    # Summation
    elif(type(arg) is cvxpy_tree and arg.item.name == '+'):
        new_children = map(lambda x:re_eval(x,param_map),arg.children)
        return sum(new_children)

    # Multiplication
    elif(type(arg) is cvxpy_tree and arg.item.name == '*'):
        child1 = re_eval(arg.children[0],param_map)
        child2 = re_eval(arg.children[1],param_map)
        return child1*child2

    # Function
    elif(type(arg) is cvxpy_tree and arg.item.type == FUNCTION):
        new_children = map(lambda x:re_eval(x,param_map),arg.children)
        return arg.item(new_children)

    # Constraint
    elif(type(arg) is cvxpy_constr):
        
        # Not set membership
        if(arg.op != 'in'):
            left = re_eval(arg.left ,param_map)
            right= re_eval(arg.right,param_map)
            if(arg.op == '=='):
                return equal(left,right)
            elif(arg.op == '<='):
                return less(left,right)
            else:
                return greater(left,right)

        # Set membership
        else:
            left = re_eval(arg.left,param_map)
            return belongs(left,arg.right)

    # Array
    elif(type(arg) is cvxpy_expression or
         type(arg) is cvxpy_var or
         type(arg) is cvxpy_param):
        (m,n) = arg.shape
        new_exp = cvxpy_expression(m,n)
        for i in range(0,m,1):
            for j in range(0,n,1):
                new_exp[i,j] = re_eval(arg[i,j],param_map)
        return new_exp

    # List
    elif(type(arg) is cvxpy_list):
        new_list = cvxpy_list([])
        for c in arg:
            new_list += cvxpy_list([re_eval(c,param_map)])
        return new_list

    # Invalid
    else:
        raise ValueError('Invalid argument')
