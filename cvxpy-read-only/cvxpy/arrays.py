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
from cvxpy.constraints import cvxpy_list

#***********************************************************
# Class definition: cvxpy_expression                       *
#***********************************************************
class cvxpy_expression(object):

    # Method: __init__
    def __init__(self,m,n):
        self.shape = (m,n)
        temp1 = {}
        for i in range(0,m,1):
            temp2 = {}
            for j in range(0,n,1):
                temp2[j] = 0.0
            temp1[i] = temp2
        self.data = temp1
        self.type = EXPRESSION
    
    # Method:__getattr__
    def __getattribute__(self,name):

        # Transpose
        if(name == 'T'):
            (m,n) = self.shape
            new_exp = cvxpy_expression(n,m)
            for i in range(0,m,1):
                for j in range(0,n,1):
                    new_exp[j,i] = self[i,j]
            return new_exp
        
        # Return attribute
        else:
            return object.__getattribute__(self, name)

    # Method: get_shape
    def get_shape(self):
        return self.shape
    
    # Method: __setitem__
    def __setitem__(self,key,value):
        if(type(key) == tuple):
            self.data[key[0]][key[1]] = value
        else:
            raise ValueError('Invalid Key')

    # Method: __getitem__
    def __getitem__(self,key):
        if(type(key) != tuple):
            raise TypeError('Invalid Key')
        else:

            # Prepare left slice
            sl = [None,None,None]
            if(np.isscalar(key[0])):
                sl = [key[0],key[0]+1,1]
            elif(type(key[0]) is slice):
                if(key[0].start == None):
                    sl[0] = 0
                else:
                    sl[0] = key[0].start
                if(key[0].stop == None):
                    sl[1] = self.shape[0]
                else:
                    sl[1] = key[0].stop
                if(key[0].step == None):
                    sl[2] = 1
                else:
                    sl[2] = key[0].step
            else:
                raise TypeError('Invalid key')

            # Prepare right slices
            sr = [None,None,None]
            if(np.isscalar(key[1])):
                sr = [key[1],key[1]+1,1]
            elif(type(key[1]) is slice):
                if(key[1].start == None):
                    sr[0] = 0
                else:
                    sr[0] = key[1].start
                if(key[1].stop == None):
                    sr[1] = self.shape[1]
                else:
                    sr[1] = key[1].stop
                if(key[1].step == None):
                    sr[2] = 1
                else:
                    sr[2] = key[1].step
            else:
                raise TypeError('Invalid key')

            # Calculate new size            
            ll = range(sl[0],sl[1],sl[2])
            lr = range(sr[0],sr[1],sr[2])
            new_m = len(ll)
            new_n = len(lr)

            # Scalar
            if(new_m == 1 and new_n == 1):
                return self.data[sl[0]][sr[0]]

            # Array
            new_ex = cvxpy_expression(new_m,new_n)
            for i in range(0,new_m,1):
                for j in range(0,new_n,1):
                    if(ll[i] < 0 or ll[i] >= self.shape[0]):
                        raise TypeError('Index out of range')
                    if(lr[j] < 0 or lr[j] >= self.shape[1]):
                        raise TypeError('Index out of range')                   
                    new_ex[i,j] = self.data[ll[i]][lr[j]]
            return new_ex

    # Method: get_value
    def get_value(self):

        # Dimensions
        m = self.shape[0]
        n = self.shape[1]
        mat = cvxpy_matrix(np.zeros((m,n)))

        # Fill matrix
        for i in range(0,m,1):
            for j in range(0,n,1):
                if(np.isscalar(self[i,j])):
                    mat[i,j] = self[i,j]
                else:
                    mat[i,j] = self[i,j].get_value()
        
        # Return matrix
        return mat

    # Method: __str__
    def __str__(self):
        """
        output = 'matrix(['
        for i in range(0,self.shape[0],1):
            for j in range(0,self.shape[1],1):
                output += str(self[i,j])
                if(i != self.shape[0]-1 or j != self.shape[1]-1):
                    output += ','
        output += '], '+str(self.shape)+')'
        return output
        """
        output = '['
        for i in range(0,self.shape[0],1):
            if(i != 0):
                output += '\n ['
            else:
                output += '['
            for j in range(0,self.shape[1],1):
                output += ' ' + str(self.data[i][j]) + ' '
            output += ']'
        output += '] '
        return output

    # Method: __add__
    def __add__(self,other):
        return self.__addsub__(other,'la')

    # Method: __sub__
    def __sub__(self,other):
        return self.__addsub__(other,'ls')

    # Method: __radd__
    def __radd__(self,other):
        return self.__addsub__(other,'ra')

    # Method: __rsub__
    def __rsub__(self,other):
        return self.__addsub__(other,'rs')

    # Method: __addsub__
    def __addsub__(self,other,action):
        
        # New expression
        m = self.shape[0]
        n = self.shape[1]
        new_exp = cvxpy_expression(m,n)

        # Scalar
        if(np.isscalar(other) or 
           type(other).__name__ in SCALAR_OBJS):
            for i in range(0,m,1):
                for j in range(0,n,1):
                    if(action == 'la'):
                        new_exp[i,j] = self[i,j] + other
                    elif(action == 'ls'):
                        new_exp[i,j] = self[i,j] - other
                    elif(action == 'ra'):
                        new_exp[i,j] = other + self[i,j]
                    else:
                        new_exp[i,j] = other - self[i,j]
            return new_exp

        # Variable, expression or matrix
        elif(type(other) is cvxpy_matrix or 
             type(other).__name__ in ARRAY_OBJS):
            if(other.shape != self.shape):
                raise ValueError('Invalid Dimensions')
            else:
                for i in range(0,m,1):
                    for j in range(0,n,1):
                        if(action == 'la'):
                            new_exp[i,j] = self[i,j] + other[i,j]
                        elif(action == 'ls'):
                            new_exp[i,j] = self[i,j] - other[i,j]
                        elif(action == 'ra'):
                            new_exp[i,j] = other[i,j] + self[i,j]
                        else:
                            new_exp[i,j] = other[i,j] - self[i,j]
                return new_exp

        # Not implemented
        else:
            return NotImplemented
    
    # Method: __mul__
    def __mul__(self,other):
        return self.__mulhandle__(other,'lm')
    
    # Method: __rmul__
    def __rmul__(self,other):
        return self.__mulhandle__(other,'rm')
   
    # Method: __mulhandle__
    def __mulhandle__(self,other,action):

        # New expression
        m = self.shape[0]
        n = self.shape[1]

        # Scalar
        if(np.isscalar(other) or 
           type(other).__name__ in SCALAR_OBJS):
            new_exp = cvxpy_expression(m,n)
            for i in range(0,m,1):
                for j in range(0,n,1):
                    if(action == 'lm'):
                        new_exp[i,j] = self[i,j] * other
                    else:
                        new_exp[i,j] = other * self[i,j]
            return new_exp

        # Variable, expression or matrix
        elif(type(other) is cvxpy_matrix or 
             type(other).__name__ in ARRAY_OBJS):
            p = other.shape[0]
            q = other.shape[1]
            if(action == 'lm'):
                if(p != n):
                    raise ValueError('Invalid Dimensions')
                else:
                    new_exp = cvxpy_expression(m,q)
                    for i in range(0,m,1):
                        for j in range(0,q,1):
                            temp = 0
                            for k in range(0,n,1):
                                temp += self[i,k]*other[k,j]
                            new_exp[i,j] = temp

                    # Convert to scalar if shape = (1,1)
                    if(new_exp.shape == (1,1)):
                        return new_exp[0,0]
                    else:
                        return new_exp
            else:
                if(q != m):
                    raise ValueError('Invalid Dimensions')
                else:
                    new_exp = cvxpy_expression(p,n)
                    for i in range(0,p,1):
                        for j in range(0,n,1):
                            temp = 0
                            for k in range(0,m,1):
                                temp += other[i,k]*self[k,j]
                            new_exp[i,j] = temp
                    if(new_exp.shape == (1,1)):
                        return new_exp[0,0]
                    else:
                        return new_exp
        else:
            return NotImplemented
    
    # Method: __neg__
    def __neg__(self):
        m = self.shape[0]
        n = self.shape[1]
        new_exp = cvxpy_expression(m,n)
        for i in range(0,m,1):
            for j in range(0,n,1):
                new_exp[i,j] = -self[i,j]
        return new_exp

    # Method: get_vars
    def get_vars(self):
        l = cvxpy_list([])
        for i in range(0,self.shape[0],1):
            for j in range(0,self.shape[1],1):
                if(not np.isscalar(self[i,j])):
                    l += self[i,j].get_vars()
        return l

    # Method: get_params
    def get_params(self):
        l = cvxpy_list([])
        for i in range(0,self.shape[0],1):
            for j in range(0,self.shape[1],1):
                if(not np.isscalar(self[i,j])):
                    l += self[i,j].get_params()
        return l
    
    # Method: is_affine
    def is_affine(self):
        for i in range(0,self.shape[0],1):
            for j in range(0,self.shape[1],1):
                if(not np.isscalar(self[i,j]) and
                   not self[i,j].is_affine()):
                    return False
        return True

#***********************************************************
# Class definition: cvxpy_var                              *
#***********************************************************
class cvxpy_var(cvxpy_expression):

    # Method: __init__
    def __init__(self,name,m,n,s):
        self.name = name
        
        # Call parent constructor
        cvxpy_expression.__init__(self,m,n)
        
        # No structure
        if(s == None):
            for i in range(0,m,1):
                for j in range(0,n,1):
                    v = cvxpy_scalar_var(name+'['+str(i)+','+str(j)+']')
                    self[i,j] = v
        
        # Lower triangular
        elif(s == 'lower triangular'):
            if(m!=n):
                raise ValueError('Invalid dimensions')
            for i in range(0,m,1):
                for j in range(0,i+1,1):
                    v = cvxpy_scalar_var(name+'['+str(i)+','+str(j)+']')
                    self[i,j] = v

        # Upper triangular
        elif(s == 'upper triangular'):
            if(m!=n):
                raise ValueError('Invalid dimensions')
            for i in range(0,m,1):
                for j in range(i,n,1):
                    v = cvxpy_scalar_var(name+'['+str(i)+','+str(j)+']')
                    self[i,j] = v
        
        # Symmetric
        elif(s == 'symmetric'):
            if(m!=n):
                raise ValueError('Invalid dimensions')
            for i in range(0,m,1):
                for j in range(0,i+1,1):
                    v = cvxpy_scalar_var(name+'['+str(i)+','+str(j)+']')
                    self[i,j] = v
                    self[j,i] = v
        
        # Error
        else:
            raise ValueError('Invalid structure')

#***********************************************************
# Class definition: cvxpy_param                            *
#***********************************************************
class cvxpy_param(cvxpy_expression):

    # Method: __init__
    def __init__(self,name,m,n):
        self.name = name
        
        # Call parent constructor
        cvxpy_expression.__init__(self,m,n)
        
        # No structure
        for i in range(0,m,1):
            for j in range(0,n,1):
                v = cvxpy_scalar_param(name+'['+str(i)+','+str(j)+']')
                self[i,j] = v

#***********************************************************
# Class definition: cvxpy_matrix                           *
#***********************************************************
class cvxpy_matrix(np.matrix):

    # Method: __init__
    def __init__(self,data,dtype=None,copy=False):
        np.matrix.__init__(data)

    # Method:__getattr__
    def __getattribute__(self,name):

        # Inverse
        if(name == 'I'):
            (m,n) = self.shape
            temp = np.array(self.copy())
            temp1 = np.array((np.matrix(temp).I))
            return cvxpy_matrix(temp1)

        # Return attribute
        else:
            return np.matrix.__getattribute__(self, name)


    # Method: __add__
    def __add__(self,other):
        if(type(other).__name__ in SCALAR_OBJS or
           type(other).__name__ in ARRAY_OBJS):
            return NotImplemented
        else:
            return np.matrix.__add__(self,other)

    # Method: __radd__
    def __radd__(self,other):
        if(type(other).__name__ in SCALAR_OBJS or
           type(other).__name__ in ARRAY_OBJS):
            return NotImplemented
        else:
            return np.matrix.__radd__(self,other)
    # Method: __sub__
    def __sub__(self,other):
        if(type(other).__name__ in SCALAR_OBJS or
            type(other).__name__ in ARRAY_OBJS):
            return NotImplemented
        else:
            return np.matrix.__sub__(self,other)

    # Method: __rsub__
    def __rsub__(self,other):
        if(type(other).__name__ in SCALAR_OBJS or
           type(other).__name__ in ARRAY_OBJS):
            return NotImplemented
        else:
            return np.matrix.__rsub__(self,other)

    # Method: __mul__
    def __mul__(self,other):
        if(type(other).__name__ in SCALAR_OBJS or
           type(other).__name__ in ARRAY_OBJS):
            return NotImplemented
        else:
            return np.matrix.__mul__(self,other)
        
    # Method: __rmul__
    def __rmul__(self,other):
        if(type(other).__name__ in SCALAR_OBJS or
           type(other).__name__ in ARRAY_OBJS):
            return NotImplemented
        else:
            return np.matrix.__rmul__(self,other)

# Load modules
from cvxpy.scalars import cvxpy_scalar_var,cvxpy_scalar_param
