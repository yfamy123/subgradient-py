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
from cvxpy.scalars import cvxpy_obj,cvxpy_scalar_var,cvxpy_tree
from cvxpy.constraints import cvxpy_list,cvxpy_constr
from cvxpy.interface import equal,var
from cvxpy.arrays import cvxpy_expression,cvxpy_var

# Function expand
def expand(arg):
    
    # Constant
    if(type(arg) is cvxpy_obj):
        return arg,cvxpy_list([])
    
    # Scalar variable
    elif(type(arg) is cvxpy_scalar_var):
        return arg,cvxpy_list([])

    # Summation
    elif(type(arg) is cvxpy_tree and arg.item.name == '+'):

        # Get item and children
        item = arg.item
        children = arg.children

        # New var
        v = var()            
            
        # Expand children
        new_children = []
        new_constr = cvxpy_list([])
        for child in children:
            
            # Multiplication
            if(child.type == TREE and
               child.item.name == '*'):
                child_var,child_constr = expand(child.children[1])
                new_children += [child.children[0].data*child_var]
                new_constr += child_constr
                    
            # Else
            else:
                child_var,child_constr = expand(child)
                new_children += [child_var]
                new_constr += child_constr
             
        # Return (Always right side is the new variable)
        new_tree = cvxpy_tree(item,new_children)
        return v,cvxpy_list([equal(new_tree,v)])+new_constr
        
    # Multiplication
    elif(type(arg) is cvxpy_tree and arg.item.name == '*'):

        # Get item and children
        item = arg.item
        children = arg.children

        # New var
        v = var()

        # Apply expand to second operand (first is a constant)
        child_var,child_constr = expand(children[1])

        # Return result (Always right side is the new variable)
        new_tree = cvxpy_tree(item,[children[0],child_var])
        new_eq = cvxpy_list([equal(new_tree,v)])
        new_eq += child_constr
        return v,new_eq
    
    # Function
    elif(type(arg) is cvxpy_tree and arg.item.type == FUNCTION):

        # Get item and children
        item = arg.item
        children = arg.children

        # New var 
        v = var()

        # Analyze children
        new_children = []
        new_constr = cvxpy_list([])
        for child in children:
            child_var,child_constr = expand(child)
            new_children += [child_var]
            new_constr += child_constr
                
        # Return (Always right side is the new variable)
        new_tree = cvxpy_tree(item,new_children)
        new_constr += item._range_constr(v)
        new_constr += item._dom_constr(new_children)
        return v,cvxpy_list([equal(new_tree,v)])+new_constr
    
    # Constraint
    elif(type(arg) is cvxpy_constr):
        
        # Not set membership
        if(arg.op != 'in'):

            # Apply expand to left and right side
            obj1,constr_list1 = expand(arg.left)
            obj2,constr_list2 = expand(arg.right)
                                         
            # Return new constraints
            new_constr = cvxpy_constr(obj1,arg.op,obj2)
            new_list = cvxpy_list([new_constr])
            new_list += constr_list1
            new_list += constr_list2
            return new_list

        # Set membership
        else:
            obj, constr_list = expand(arg.left)
            new_constr = cvxpy_constr(obj,arg.op,arg.right)
            return cvxpy_list([new_constr])+constr_list

    # Array
    elif(type(arg) is cvxpy_expression or
         type(arg) is cvxpy_var):
        (m,n) = arg.shape
        new_list = cvxpy_list([])
        new_exp = cvxpy_expression(m,n)
        for i in range(0,m,1):
            for j in range(0,n,1):

                # Number: Upgrade
                if(np.isscalar(arg[i,j])):
                    new_exp[i,j] = cvxpy_obj(CONSTANT,arg[i,j],str(arg[i,j]))
                    
                # Not a number
                else:
                    obj,constr_list = expand(arg[i,j])
                    new_exp[i,j] = obj
                    new_list += constr_list
        return new_exp,new_list
    
    # List of constraints
    elif(type(arg) is cvxpy_list):

        # Empty list
        if(len(arg) == 0):
            return cvxpy_list([])
        else:
            new_list = map(expand,arg)
            return reduce(lambda x,y:x+y,new_list)

    # Invalid
    else:
        raise ValueError('Invalid argument')
   
