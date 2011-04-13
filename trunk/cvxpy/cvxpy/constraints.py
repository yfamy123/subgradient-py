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

#***********************************************************
# Class definition: cvxpy_constr                           *
#***********************************************************
class cvxpy_constr(object):

    # Method: __init__
    def __init__(self,left,op,right):
        self.left = left
        self.op = op
        self.right = right

    # Method: get_vars
    def get_vars(self):
        if(self.op == 'in'):
            return self.left.get_vars()
        else:
            return self.left.get_vars() + self.right.get_vars()

    # Method: get_params
    def get_params(self):
        if(self.op == 'in'):
            return self.left.get_params()
        else:
            return self.left.get_params() + self.right.get_params()

    # Method: __str__
    def __str__(self):
        l_text = str(self.left)
        op_text = self.op
        r_text = str(self.right)
        return l_text+' '+op_text+' '+r_text

    # Method: is_dcp
    def is_dcp(self):
        if(self.op == '==' and
           self.left.is_affine() and
           self.right.is_affine()):
            return True
        elif(self.op == '<=' and
             self.left.is_convex() and
             self.right.is_concave()):
            return True
        elif(self.op == '>=' and
             self.left.is_concave() and
             self.right.is_convex()):
            return True
        elif(self.op == 'in' and
             self.left.is_affine()):
            return True
        else:
            return False
        
    # Method: is_affine
    def is_affine(self):
        if(self.op == 'in'):
            return False
        else:
            return self.left.is_affine() and self.right.is_affine()
        

#***********************************************************
# Class definition: cvxpy_list                             *
#***********************************************************
class cvxpy_list(list):

    # Method: get_vars
    def get_vars(self):

        # Check if empty
        if(len(self) == 0):
            return cvxpy_list([])

        # Not empty
        else:

            # Get all vars
            all_vars = map(lambda x: x.get_vars(),self)
            if (len(all_vars) != 0):
                all_vars = reduce(lambda x,y: x+y,all_vars)
            else:
                all_vars = cvxpy_list([])

            # Construct set
            new_list = cvxpy_list([])
            for v in all_vars:
                l1 = map(lambda x: x is v,new_list)
                if(len(l1) != 0):
                    if not reduce(lambda x,y: x or y,l1):
                        new_list += cvxpy_list([v])
                else:
                    new_list += cvxpy_list([v])

            # Return set of variables
            return new_list
        
    # Method: get_params
    def get_params(self):

        # Check if empty
        if(len(self) == 0):
            return cvxpy_list([])

        # Not empty
        else:

            # Get all params
            all_params = map(lambda x: x.get_params(),self)
            if (len(all_params) != 0):
                all_params = reduce(lambda x,y: x+y,all_params)
            else:
                all_params = cvxpy_list([])

            # Construct set
            new_list = cvxpy_list([])
            for v in all_params:
                l1 = map(lambda x: x is v,new_list)
                if(len(l1) != 0):
                    if not reduce(lambda x,y: x or y,l1):
                        new_list += cvxpy_list([v])
                else:
                    new_list += cvxpy_list([v])

            # Return set of parameters
            return new_list

    # Method: _get_eq
    def _get_eq(self):

        # New list
        nl = [c for c in self if c.op == '==']

        # Return equality constraints
        return cvxpy_list(nl)

    # Method: _get_ineq_in
    def _get_ineq_in(self):

        # New list
        nl = [c for c in self if c.op != '==']

        # Return inequality and membership constraints
        return cvxpy_list(nl)

    # Method: _get_convex
    def _get_convex(self):
        """
        Description
        -----------
        Return convex constraints.
        Note: It assumes the constraints have been
        expanded and transformed.
        """

        # Empty list
        constr_list = cvxpy_list([])
        for c in self:

            # Function (Always on the left side)
            if(c.left.type == TREE and
               c.left.item.type == FUNCTION):
                
                # Get function
                fn = c.left.item
                
                # Add only if convex constraint
                if((fn.curvature == CONVEX and
                    c.op == '<=') or
                   (fn.curvature == CONCAVE and
                    c.op == '>=')):
                    constr_list += cvxpy_list([c])
            
            # Not a function
            else:
                constr_list += cvxpy_list([c])
            
        # Return
        return constr_list
    
    # Method: _get_nonconvex
    def _get_nonconvex(self):
        """
        Description
        -----------
        Return non convex constraints.
        Note: It assumes the constraints have been
        expanded and transformed.
        """

        # Empty list
        constr_list = cvxpy_list([])
        for c in self:

            # Function (Always on the left side)
            if(c.left.type == TREE and
               c.left.item.type == FUNCTION):
                
                # Get function
                fn = c.left.item
                
                # Add only if non convex constraint
                if((fn.curvature == CONVEX and
                    c.op == '>=') or
                   (fn.curvature == CONCAVE and
                    c.op == '<=')):
                    constr_list += cvxpy_list([c])

        # Return
        return constr_list

    # Method: is_dcp
    def is_dcp(self):
        l = map(lambda x:x.is_dcp(),self)
        if(len(l) == 0):
            return True
        else:
            return reduce(lambda x,y:x and y,l)

    # Method: is_affine
    def is_affine(self):
        l = map(lambda x:x.is_affine(),self)
        if(len(l) == 0):
            return True
        else:
            return reduce(lambda x,y: x and y,l)
    
    # Method: __add__
    def __add__(self,other):        
        return cvxpy_list(list(self) + other)

    # Method: __radd__
    def __radd__(self,other):
        return cvxpy_list(other + list(self))

    # Method: __str__
    def __str__(self):
        output = ''
        for i in range(0,len(self),1):
            output = output + str(self[i])
            if(i != len(self)-1):
                output = output + '\n'
        return output
