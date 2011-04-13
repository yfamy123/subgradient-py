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
from cvxpy.scalars import cvxpy_scalar_var,cvxpy_scalar_param
from cvxpy.constraints import cvxpy_constr,cvxpy_list
from cvxpy.arrays import cvxpy_var,cvxpy_param
from cvxpy.arrays import cvxpy_expression,cvxpy_matrix

# Names
__all__ = ["var", "var_reset", "param", "matrix", "equal",
           "less", "greater", "prog", "minimize", "maximize", 
           "belongs"]

# Interface function: var
def var(name=None,m=1,n=1,s=None):
    """ 
    Create an optimization variable.

    :param name: Variable name.
    :type name: String
    :param m: Rows.
    :param n: Columns.
    :param s: Structure of the variable.
    :type s: String
    :rtype: :class:`cvxpy_var` or :class:`cvxpy_scalar_var`.
    """
    if((m,n) == (1,1)):
        return cvxpy_scalar_var(name)
    else:
        return cvxpy_var(name,m,n,s)

# Interface function: var_reset
def var_reset():
    cvxpy_scalar_var.i = 0     

# Interface function: param
def param(name=None,m=1,n=1):
    """ 
    Create a parameter.

    :param name: Parameter name.
    :type name: String
    :param m: Rows.
    :param n: Columns.
    :rtype: :class:`cvxpy_param` or :class:`cvxpy_scalar_param`.
    """
    if((m,n) == (1,1)):
        return cvxpy_scalar_param(name)
    else:
        return cvxpy_param(name,m,n)

# Interface function: matrix
def matrix(data):
    """ 
    Create a matrix.
    
    :param data: Array-like object.
    :rtype: :class:`cvxpy_matrix`.
    """
    #return cvxpy_matrix(np.float64(data).tolist())
    return cvxpy_matrix(np.float64(data))

# Interface function: equal
def equal(lhs,rhs):
    """
    Form equality constraint (lhs == rhs)

    :param lhs: Left hand side.
    :param rhs: Right hand side.
    :rtype: :class:`cvxpy.constr`
    """
    return compare(lhs,'==',rhs)

# Interface function: less
def less(lhs,rhs):
    """
    Form less than or equal constraint (lhs <= rhs)

    :param lhs: Left hand side.
    :param rhs: Right hand side.
    :rtype: :class:`cvxpy.constr`
    """
    return compare(lhs,'<=',rhs)

# Interface function: greater
def greater(lhs,rhs):
    """
    Form greater than or equal constraint (lhs >= rhs)

    :param lhs: Left hand side.
    :param rhs: Right hand side.
    :rtype: :class:`cvxpy.constr`
    """
    return compare(lhs,'>=',rhs)

# Interface function: compare
def compare(obj1,op,obj2):
    
    # Both scalars 
    if((np.isscalar(obj1) or type(obj1).__name__ in SCALAR_OBJS) and
       (np.isscalar(obj2) or type(obj2).__name__ in SCALAR_OBJS)):
        
        # Upgrade scalars to cvxpy_obj
        if(np.isscalar(obj1)):
            obj1 = cvxpy_obj(CONSTANT,obj1,str(obj1))
        if(np.isscalar(obj2)):
            obj2 = cvxpy_obj(CONSTANT,obj2,str(obj2))

        # Construct and return constraint
        return cvxpy_constr(obj1,op,obj2)

    # Upgrate scalars to arrays
    if((type(obj1) is cvxpy_matrix or type(obj1).__name__ in ARRAY_OBJS) and
       (np.isscalar(obj2) or type(obj2).__name__ in SCALAR_OBJS)):
        (m,n) = obj1.shape
        new_exp = cvxpy_expression(m,n)
        for i in range(0,m,1):
            for j in range(0,n,1):
                new_exp[i,j] = obj2
        obj2 = new_exp
    if((type(obj2) is cvxpy_matrix or type(obj2).__name__ in ARRAY_OBJS) and
       (np.isscalar(obj1) or type(obj1).__name__ in SCALAR_OBJS)):
        (m,n) = obj2.shape
        new_exp = cvxpy_expression(m,n)
        for i in range(0,m,1):
            for j in range(0,n,1):
                new_exp[i,j] = obj1
        obj1 = new_exp
    
    # Both arrays
    if((type(obj1) is cvxpy_matrix or type(obj1).__name__ in ARRAY_OBJS) and
       (type(obj2) is cvxpy_matrix or type(obj2).__name__ in ARRAY_OBJS)):
        constr = []
        if(obj1.shape != obj2.shape):
            raise ValueError('Invalid dimensions')
        (m,n) = obj1.shape
        for i in range(0,m,1):
            for j in range(0,n,1):
                constr += [compare(obj1[i,j],op,obj2[i,j])]
        return cvxpy_list(constr)

    # Invalid arguments
    raise ValueError('Objects not comparable')    

# Interface function: prog
def prog(pair,constr=[],params=[],opt=None,name='prog'):
    """
    Create an optimization program.

    :param pair: (MAXIMIZE or MINIMIZE, objective)
    :param constr: List of :class:`cvxpy_constr` or :class:`cvxpy_list`.
    :param params: List of :class:`cvxpy_scalar_param` or 
                   :class:`cvxpy_param`. This list must match the number
                   of parameters present in the program.
    :param opt: Dictionary of options.
    :param name: Program name string.
    :rtype: :class:`cvxpy_program`.
    """

    # Parameters
    action = pair[0]
    obj = pair[1]

    # Verify objective
    if((not np.isscalar(obj)) and
       (not type(obj) is cvxpy_obj) and 
       type(obj).__name__ not in SCALAR_OBJS):
        raise ValueError('Invalid Objective')

    # Upgrade numeric objective to scalar object
    if(np.isscalar(obj)):
        obj = cvxpy_obj(CONSTANT,obj,str(obj))

    # Return program
    return cvxpy_program(action,obj,constr,params,opt,name)

# Interface function: minimize
def minimize(obj):
    """
    Form (action,objective) pair.
    
    :param obj: Number or scalar obejct
    :rtype: Pair (MINIMIZE,obj)
    """
    return MINIMIZE,obj

# Interface function: maximize
def maximize(obj):
    """
    Form (action,objective) pair.
    
    :param obj: Number or scalar obejct
    :rtype: Pair (MAXIMIZE,obj)
    """
    return MAXIMIZE,obj

# Method: belongs
def belongs(x,A):
    """
    Form set membership constraint (x in A)
    
    :param x: :class:`cvxpy_matrix` or array object.
    :param A: Set atom. 
    :rtype: :class:`cvxpy.constr`
    """
    
    # Element is not array-like
    if(type(x).__name__ not in ARRAY_OBJS and
       type(x) is not cvxpy_matrix):
        raise ValueError('First argument must be array-like')
    
    # Set is not valid
    if(A.type != SET):
        raise ValueError('Second argument must be a set')

    # Verify dimensions
    (m1,n1) = A.shape
    (m2,n2) = x.shape

    # Dimensions don't match
    if((m1,n1) != (m2,n2)):
        raise ValueError('Invalid dimensions')

    # Construct and return constraint
    return cvxpy_constr(x,'in',A)

# Load modules
from cvxpy.program import cvxpy_program
