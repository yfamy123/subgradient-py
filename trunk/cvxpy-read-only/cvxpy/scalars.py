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

#***********************************************************
# Class definition: cvxpy_obj                              *
#***********************************************************
class cvxpy_obj(object):

    # Method: __init__
    def __init__(self,t=None,d=None,n=None):
        """
        Description
        -----------
        Class constructor.
        
        Arguments
        ---------
        t: Object type (See cvxpy.def).
        d: Data or value.
        n: Name string.
        """
        self.type = t
        self.data = d
        self.name = n
        self.shape = (1,1)

    # Method: get_shape
    def get_shape(self):
        return self.shape

    # Method: is_convex
    def is_convex(self):
        return True

    # Method: is_concave
    def is_concave(self):
        return True

    # Method: is_dcp
    def is_dcp(self):
        return True

    # Method: is_affine
    def is_affine(self):
        return True

    # Method: get_value
    def get_value(self):
        return self.data

    # Method: set_value
    def set_value(self,new_value):
        self.data = new_value 

    # Method: get_vars
    def get_vars(self):
        return cvxpy_list([])

    # Method: get_params
    def get_params(self):
        return cvxpy_list([])

    # Method: __add__
    def __add__(self,other):
        return self.__addsub__(other,'+')

    # Method: __sub__
    def __sub__(self,other):
        return self.__addsub__(other,'-')

    # Method: __radd__
    def __radd__(self,other):
        return self.__raddsub__(other,'+')

    # Method: __rsub__
    def __rsub__(self,other):
        return self.__raddsub__(other,'-')

    # Method: __addsub__
    def __addsub__(self,other,op):
        """
        Description
        -----------
        Handles left add or left subtract.
        
        Arguments
        ---------
        other: right hand object.
        op: Character (+ or -)
        """

        # Create operator (I should create another class for this)
        operator = cvxpy_obj(OPERATOR,None,'+')

        # Create args to combine
        if(type(self) is cvxpy_tree and
           self.item.name == '+'):
            args = self.children
        else:
            args = [self]

        # Number
        if(np.isscalar(other)):
            if(other == 0.0):
                return self
            if(op == '+'):
                constant = cvxpy_obj(CONSTANT,other,str(other))
            else:
                constant = cvxpy_obj(CONSTANT,-other,str(-other))
            return cvxpy_tree(operator,args+[constant])

        # Scalar variable or scalar param
        elif(type(other) is cvxpy_scalar_var or
             type(other) is cvxpy_scalar_param):
            if(op == '+'):
                return cvxpy_tree(operator,args+[other])
            else:
                return cvxpy_tree(operator,args+[-other])
        
        # Tree
        elif(type(other) is cvxpy_tree):
            if(other.item.name == '+'):
                if(op == '+'):
                    return cvxpy_tree(operator,
                                      args+other.children)
                else:
                    return cvxpy_tree(operator,
                                      args+[-x for x in other.children])
            else:
                if(op == '+'):
                    return cvxpy_tree(operator,args+[other])
                else:
                    return cvxpy_tree(operator,args+[-other])

        # Matrix
        elif(type(other) is cvxpy_matrix):
            m = other.shape[0]
            n = other.shape[1]
            new_exp = cvxpy_expression(m,n)
            for i in range(0,m,1):
                for j in range(0,n,1):
                    if(op == '+'):
                        new_exp[i,j] = self+other[i,j]
                    else:
                        new_exp[i,j] = self-other[i,j]
            return new_exp

        # Not implemented
        else:
            return NotImplemented

    # Method: __raddsub__
    def __raddsub__(self,other,op):
        """
        Description
        -----------
        Handles right add or right subtract.
        
        Arguments
        ---------
        other: left hand object.
        op: Character (+ or -)
        """

        # Create operator
        operator = cvxpy_obj(OPERATOR,None,'+')

        # Create args to combine
        if(type(self) is cvxpy_tree and
           self.item.name == '+'):
            if(op == '+'):
                args = self.children
            else:
                args = [-x for x in self.children]
        else:
            if(op == '+'):
                args = [self]
            else:
                args = [-self]

        # Number
        if(np.isscalar(other)):
            if(other == 0.0):
                if(op == '+'):
                    return self
                else:
                    return -self
            constant = cvxpy_obj(CONSTANT,other,str(other))
            return cvxpy_tree(operator,[constant]+args)

        # Scalar variable or scalar param
        elif(type(other) is cvxpy_scalar_var or
             type(other) is cvxpy_scalar_param):
            return cvxpy_tree(operator,[other]+args)

        # Tree
        elif(type(other) is cvxpy_tree):
            if(other.item.name == '+'):
                return cvxpy_tree(operator,other.children+args)
            else:
                return cvxpy_tree(operator,[other]+args)
                
        # Matrix
        elif(type(other) is cvxpy_matrix):
            m = other.shape[0]
            n = other.shape[1]
            new_exp = cvxpy_expression(m,n)
            for i in range(0,m,1):
                for j in range(0,n,1):
                    if(op == '+'):
                        new_exp[i,j] = other[i,j]+self
                    else:
                        new_exp[i,j] = other[i,j]-self
            return new_exp

        # Not implemented
        else:
            return NotImplemented

    # Method: __mul__
    def __mul__(self,other):
        return self.__mulhandle__(other)

    # Method: __rmul__
    def __rmul__(self,other):
        return self.__mulhandle__(other)

    # Method: __mulhandle__
    def __mulhandle__(self,other):
        """
        Description
        -----------
        Handles multiply.
        Note: If other is numeric, the multiplication
        tree formed has the constant object as first child.

        Argument
        --------
        other: Other object.
        """

        # Create operator
        operator = cvxpy_obj(OPERATOR,None,'*')

        # Number
        if(np.isscalar(other)):

            # Multiplication by 0
            if(other == 0.0):
                return 0.0

            # Multiplication by 1
            elif(other == 1.0):
                return self

            # Distribution over addition
            elif(type(self) is cvxpy_tree and
                 self.item.name == '+'):
                new_children = []
                for child in self.children:
                    new_children += [other*child]
                return cvxpy_tree(self.item,new_children)

            # Associativity
            elif(type(self) is cvxpy_tree and
                 self.item.name == '*' and
                 self.children[0].type == CONSTANT):
                new_object = other*self.children[0]
                if(new_object.data == 1.0):
                    return self.children[1]
                else:
                    return cvxpy_tree(self.item,[new_object,
                                                 self.children[1]])

            # Constant times constant
            elif(type(self) is cvxpy_obj):
                new_const = cvxpy_obj(CONSTANT,self.data*other,
                                      str(self.data*other))
                return new_const

            # Else
            else:            
                constant = cvxpy_obj(CONSTANT,other,str(other))
                return cvxpy_tree(operator,[constant,self])

        # Matrix
        elif(type(other) is cvxpy_matrix):
            m = other.shape[0]
            n = other.shape[1]
            new_exp = cvxpy_expression(m,n)
            for i in range(0,m,1):
                for j in range(0,n,1):
                    new_exp[i,j] = other[i,j]*self
            return new_exp

        # Scalar param
        elif(type(other) is cvxpy_scalar_param):
            return cvxpy_tree(operator,[other,self])

        # Tree
        elif(type(other) is cvxpy_tree):
            if(len(self.get_vars()) == 0 ):
                return cvxpy_tree(operator,[self,other])
            elif(len(other.get_vars()) == 0):
                return cvxpy_tree(operator,[other,self])
            else:
                return NotImplemented

        # Not implemented
        else:
            return NotImplemented

    # Method: __neg__
    def __neg__(self):
        return (-1.0)*self        

    # Method: __str__
    def __str__(self):
        return self.name

#***********************************************************
# Class definition: cvxpy_scalar_var                       *
#***********************************************************
class cvxpy_scalar_var(cvxpy_obj):

    # Variable counter
    i = 0

    # Method: __init__
    def __init__(self,name=None):

        # Assign a name
        if(name is None):
            name = 'v'+str(cvxpy_scalar_var.i)
	    cvxpy_scalar_var.i += 1
            
        # Call parent constructor
        cvxpy_obj.__init__(self,VARIABLE,np.NaN,name)

    # Method: get_vars
    def get_vars(self):
        return cvxpy_list([self])

#***********************************************************
# Class definition: cvxpy_scalar_param                     *
#***********************************************************
class cvxpy_scalar_param(cvxpy_obj):

    # Method: __init__
    def __init__(self,name=None):
            
        # Call parent constructor
        cvxpy_obj.__init__(self,PARAMETER,np.NaN,name)

    # Method: is_convex
    def is_convex(self):
        return False

    # Method: is_concave
    def is_concave(self):
        return False

    # Method: is_dcp
    def is_dcp(self):
        return False

    # Method: is_affine
    def is_affine(self):
        return False

    # Method: get_params
    def get_params(self):
        return cvxpy_list([self])

#***********************************************************
# Class definition: cvxpy_tree                             *
#***********************************************************
class cvxpy_tree(cvxpy_obj):

    # Method: __init__
    def __init__(self,item,children):
        """
        Description
        -----------
        Class constructor.
        
        Arguments
        ---------
        item: cvxpy_obj (+ or -), atom function or
        cvxpy_program.
        children: List of scalar objects.
        """
        self.item = item
        self.children = children
        cvxpy_obj.__init__(self,TREE,None,None)

    # Method: get_vars
    def get_vars(self):
        l = map(lambda x: x.get_vars(),self.children)
        if(len(l) != 0):
            return reduce(lambda x,y:x+y,l)
        else:
            return cvxpy_list([])

    # Method: get_params
    def get_params(self):
        l = map(lambda x: x.get_params(),self.children)
        if(len(l) != 0):
            return reduce(lambda x,y:x+y,l)
        else:
            return cvxpy_list([])

    # Method: get_value
    def get_value(self):
        """
        Description
        -----------
        Compute the value of the tree with the 
        current values of the variables present.
        """

        # Summation
        if(self.item.name == '+'):
            values = map(lambda x:x.get_value(),
                         self.children)
            return sum(values)

        # Multiplication
        elif(self.item.name == '*'):
            l = self.children[0].get_value()
            r = self.children[1].get_value()
            return l*r

        # Function
        else:
            values = map(lambda x: x.get_value(),self.children)
            return self.item(values)
            
    # Method: __str__
    def __str__(self):
        
        # Multiplication
        if(self.item.name == '*'):
            left_text = str(self.children[0])
            if(self.children[0].type == TREE and
               self.children[0].item.type == OPERATOR):
                left_text = '('+left_text+')'
            right_text = str(self.children[1])
            if(self.children[1].type == TREE and
               self.children[1].item.type == OPERATOR):
                    right_text = '('+right_text+')'
            return left_text+'*'+right_text

        # Summation
        elif(self.item.name == '+'):
            text = str(self.children[0])
            for i in range(1,len(self.children),1):
                x = self.children[i]
                text += ' + '+str(x)
            return text
                   
        # Function
        else:
            children_text = map(str,self.children)
            args = ''
            for i in range(0,len(children_text),1):
                args += children_text[i]
                if(i != len(children_text)-1):
                    args += ', '
            return self.item.name+'('+args+')'
    
    # Method: is_convex
    def is_convex(self):
        """
        Description
        -----------
        Returns true if convexity of the tree is
        guaranteed, false otherwise.
        """

        # Summation
        if(self.item.name == '+'):
            l = map(lambda x: x.is_convex(),self.children)
            return reduce(lambda x,y: x and y,l)

        # Multiplication
        elif(self.item.name == '*'):
            ob1 = self.children[0]
            ob2 = self.children[1]
            
            # ob1 has parameters
            if(type(ob1) is not cvxpy_obj):
                return False
            
            # Use sign of ob1 and curvature of ob2
            else:
                if(ob1.data >= 0 and ob2.is_convex()):
                    return True
                elif(ob1.data <= 0 and ob2.is_concave()):
                    return True
                else:
                    return False

        # Function
        else:
            fcn = self.item
            args = self.children

            # Check curvature of function
            if(fcn.curvature != CONVEX):
                return False

            # Function is atom: Check composition rules
            if(fcn.atom):
                for i in range(0,len(args),1):
                    if(fcn.monotonicity(i) == INCREASING and
                       not args[i].is_convex()):
                        return False
                    if(fcn.monotonicity(i) == DECREASING and
                       not args[i].is_concave()):
                        return False
                    if(fcn.monotonicity(i) == NEITHER and
                       not args[i].is_affine()):
                        return False
                return True

            # Function is program
            else:
                return fcn.is_dcp(args)
            
    # Method: is_concave
    def is_concave(self):
        """
        Description
        -----------
        Returns true if concavity of the tree is
        guaranteed, false otherwise.
        """

        # Summation
        if(self.item.name == '+'):
            l = map(lambda x: x.is_concave(),self.children)
            return reduce(lambda x,y: x and y,l)

        # Multiplication
        elif(self.item.name == '*'):
            ob1 = self.children[0]
            ob2 = self.children[1]

            # ob1 has parameters
            if(type(ob1) is not cvxpy_obj):
                return False

            # Use sign of ob1 and curvature of ob2
            else:
                if(ob1.data >= 0 and ob2.is_concave()):
                    return True
                elif(ob1.data <= 0 and ob2.is_convex()):
                    return True
                else:
                    return False

        # Function
        else:
            fcn = self.item
            args = self.children

            # Check curvature of function
            if(fcn.curvature != CONCAVE):
                return False

            # Function is atom
            if(fcn.atom):
                for i in range(0,len(args),1):
                    if(fcn.monotonicity(i) == INCREASING and
                       not args[i].is_concave()):
                        return False
                    if(fcn.monotonicity(i) == DECREASING and
                       not args[i].is_convex()):
                        return False
                    if(fcn.monotonicity(i) == NEITHER and
                       not args[i].is_affine()):
                        return False
                return True

            # Function is program
            else:
                return fcn.is_dcp(args)

    # Method: is_dcp
    def is_dcp(self):
        """
        Description
        -----------
        Returns true if the tree follows DCP rules,
        false otherwise.
        """

        # Summation
        if(self.item.name == '+'):
            l = map(lambda x: x.is_dcp(),self.children)
            return reduce(lambda x,y: x and y,l)
        
        # Multiplication
        elif(self.item.name == '*'):
            ob1 = self.children[0]
            ob2 = self.children[1]

            # ob1 has parameters
            if(type(ob1) is not cvxpy_obj):
                return False

            # Check if ob2 is dcp
            else:
                return ob2.is_dcp()

        # Function
        else:

            # Atom
            if(self.item.atom):
                return self.is_convex() or self.is_concave()

            # Program
            else:
                return self.item.is_dcp(self.children)

    # Method: is_affine
    def is_affine(self):
        """
        Description
        -----------
        Returns true if the tree contains only
        affine expressions.
        """

        # Summation
        if(self.item.name == '+'):
            l = map(lambda x: x.is_affine(),self.children)
            return reduce(lambda x,y: x and y,l)
        
        # Multiplication
        elif(self.item.name == '*'):
            ob1 = self.children[0]
            ob2 = self.children[1]

            # ob1 has parameters
            if(type(ob1) is not cvxpy_obj):
                return False

            # Check if ob2 is affine
            else:
                return ob2.is_affine()

        # Function
        else:
            return False        
        
# Load modules
from cvxpy.constraints import cvxpy_list
from cvxpy.arrays import cvxpy_expression,cvxpy_matrix
