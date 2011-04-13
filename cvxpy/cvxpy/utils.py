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
from defs import *
from cvxpy.scalars import cvxpy_obj
from cvxpy.interface import matrix
from cvxpy.arrays import cvxpy_expression,cvxpy_matrix
from scipy.linalg import sqrtm as sci_sqrtm

# Names
__all__ = ["hstack", "vstack", "sum", "randn", "rand",
           "seed", "eye", "zeros", "ones", "diag", "diagflat",
           "sqrtm"]

# Utility function: Horizontal Stack
def hstack(t):
    """
    Horizontal stack.
    """
    
    # Verify input type
    new_list = []
    numeric = True
    for x in t:
        if(np.isscalar(x)):
            new_list += [matrix(x)]
        elif(type(x) is cvxpy_obj):
            new_list += [matrix(x.data)]
        elif(type(x).__name__ in SCALAR_OBJS):
            numeric = False
            new_x = cvxpy_expression(1,1)
            new_x[0,0] = x
            new_list += [new_x]
        elif(type(x).__name__ in ARRAY_OBJS):
            numeric = False
            new_list += [x]
        elif(type(x) is cvxpy_matrix):
            new_list += [x]
        else:
            raise ValueError('Invalid Input')
        
    # Input is numeric
    if(numeric):
        return np.hstack(new_list)

    # Verify dimensions
    m = new_list[0].shape[0]
    for x in new_list:
        if(x.shape[0] != m):
            raise ValueError('Invalid Dimensions')
    
    # Allocate new expression
    n = 0
    for x in new_list:
        n += x.shape[1]
    new_exp = cvxpy_expression(m,n)

    # Fill new expression
    k = 0
    for x in new_list:
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                new_exp[i,k+j] = x[i,j]
        k = k + x.shape[1]
        
    # Return new expression
    return new_exp

# Utility function: Vertical Stack
def vstack(t):
    """
    Vertical stack.
    """

    # Verify input type
    new_list = []
    numeric = True
    for x in t:
        if(np.isscalar(x)):
            new_list += [matrix(x)]
        elif(type(x) is cvxpy_obj):
            new_list += [matrix(x.data)]
        elif(type(x).__name__ in SCALAR_OBJS):
            numeric = False
            new_x = cvxpy_expression(1,1)
            new_x[0,0] = x
            new_list += [new_x]
        elif(type(x).__name__ in ARRAY_OBJS):
            numeric = False
            new_list += [x]
        elif(type(x) is cvxpy_matrix):
            new_list += [x]
        else:
            raise ValueError('Invalid Input')
        
    # Input is numeric
    if(numeric):
        return np.vstack(new_list)

    # Verify dimensions
    n = new_list[0].shape[1]
    for x in new_list:
        if(x.shape[1] != n):
            raise ValueError('Invalid Dimensions')
    
    # Allocate new expression
    m = 0
    for x in new_list:
        m += x.shape[0]
    new_exp = cvxpy_expression(m,n)

    # Fill new expression
    k = 0
    for x in new_list:
        for i in range(0,x.shape[0],1):
            for j in range(0,x.shape[1],1):
                new_exp[i+k,j] = x[i,j]
        k = k + x.shape[0]
        
    # Return new expression
    return new_exp

# Utility function: Sum
def sum(arg):
    """
    Sum of elements.
    """
    if(np.isscalar(arg) or type(arg).__name__ in SCALAR_OBJS):
        return arg
    elif(type(arg) is cvxpy_matrix or type(arg).__name__ in ARRAY_OBJS):
        m = arg.shape[0]
        n = arg.shape[1]
        temp = 0
        for i in range(0,m,1):
            for j in range(0,n,1):
                temp += arg[i,j]
        return temp
    else:
        return np.sum(arg)

# Utility function: Randn
def randn(m,n):
    return matrix(np.random.randn(m,n))

# Utility function: Rand
def rand(m,n):
    return matrix(np.random.rand(m,n))

# Utility function: Seed
def seed(arg=None):
    np.random.seed(arg)

# Utility function: Eye
def eye(n):
    return matrix(np.eye(n))

# Utility function: Zeros
def zeros(shape):
    """
    Matrix of zeros.
    """
    return matrix(np.zeros(shape))

# Utility function: Ones
def ones(shape):
    """
    Matrix of ones.
    """
    return matrix(np.ones(shape))

# Utility function: Diag
def diag(arg):
    """
    Extract the diagonal from square array-like object.
    """

    # Check size
    (m,n) = arg.shape
    if(m!=n):
        raise ValueError('Invalid dimensions')

    # cvxpy matrix
    if(type(arg) is cvxpy_matrix):
        return matrix(np.diag(arg)).T

    # Object array
    elif(type(arg).__name__ in ARRAY_OBJS):
        new_exp = cvxpy_expression(m,1)
        for i in range(0,m,1):
            new_exp[i,0] = arg[i,i]
        return new_exp

    # Error
    else:
        raise ValueError('Invalid argument type')    

# Utility function: Diagflat
def diagflat(arg):
    """
    List, row or column vector to diagonal matrix.
    """

    # Argument is a list
    if(type(arg) is list):
        arg = hstack(arg)

    # Argument is a matrix or object array
    elif(type(arg) is cvxpy_matrix or
         type(arg).__name__ in ARRAY_OBJS):
        (m,n) = arg.shape
        if(m!=1 and n!=1):
            raise ValueError('Argument must be one dimensional')
        elif(n == 1):
            arg = arg.T
    
    # Invalid argument
    else:
        raise ValueError('Invalid argument')

    # Argument is numeric
    numeric = True
    for i in range(0,arg.shape[1],1):
        if(not np.isscalar(arg[0,i])):
            numeric = False
    if(numeric):
        return matrix(np.diagflat(arg))
    
    # Not numeric
    (m,n) = arg.shape
    new_exp = cvxpy_expression(n,n)
    for i in range(0,n,1):
        new_exp[i,i] = arg[0,i]
    return new_exp

# Utility function: Sqrtm
def sqrtm(A):
    """
    Matrix square root.
    """
    return matrix(sci_sqrtm(A))
