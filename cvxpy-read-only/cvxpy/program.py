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
from cvxpy.scalars import cvxpy_scalar_param,cvxpy_obj,cvxpy_tree
from cvxpy.arrays import cvxpy_param,cvxpy_matrix
from cvxpy.interface import prog,less,greater,equal,var
from cvxpy.utils import vstack
from cvxpy.procedures.expand import expand
from cvxpy.procedures.re_eval import re_eval
from cvxpy.procedures.solve_prog import solve_prog
from cvxpy.procedures.transform import transform

#***********************************************************
# Class definition: cvxpy_program                          *
#***********************************************************
class cvxpy_program(object):

    # Method: __init__
    def __init__(self,action,obj,constr,params,opt,name):
        
        # Function attributes
        self.name = name
        self.type = FUNCTION
        self.atom = False
        self.expansion_type = PM
        if(action == MINIMIZE):
            self.curvature = CONVEX
        else:
            self.curvature = CONCAVE
       
        # Program attributes
        self.lagrange_mul_eq = None
        self.action = action
        self.obj = obj
        self.constr = cvxpy_list(constr)
        if(opt != None):
            self.options = opt
        else:
            self.options = {'SCP_ALG':SCP_ALG_OPT.copy(),
                            'SCP_SOL':SCP_SOLVER_OPT.copy(),
                            'REL_SOL':RELAX_SOLVER_OPT.copy(),
                            'show steps':False,'quiet': True}

        # Store parameters
        param_list = []
        for param in params:
            if(type(param) is cvxpy_scalar_param):
                param_list += [param]
            elif(type(param) is cvxpy_param):
                (m,n) = param.shape
                for i in range(0,m,1):
                    for j in range(0,n,1):
                        param_list += [param[i,j]]
            else:
                raise ValueError('Invalid parameter')
        self.params = cvxpy_list(param_list)

        # Verify parameters
        exp_params = self.get_params()
        if(len(exp_params) != len(self.params)):
            raise ValueError('Parameters do not match')
        for x in exp_params:
            if(x not in self.params):
                raise ValueError('Parameters do not match')
     
    # Method: _get_expanded
    def _get_expanded(self):
        """
        Description
        -----------
        Construct a new program by applying the
        expansion algorithm to the objective
        and constraints.
        """
        new_obj,new_eq = expand(self.obj)
        more_constr = expand(self.constr)
        return prog((self.action,new_obj),
                    more_constr+new_eq,[],self.options)
    
    # Method: _get_equivalent
    def _get_equivalent(self):
        """
        Description
        -----------
        Construct a new program by applying the
        transform algorithm to the constraints.
        None: It is assumed that the program 
        has been previously expanded.
        """
        return prog((self.action,self.obj),
                    transform(self.constr),[],self.options)

    # Method: _get_cvx_relaxation
    def _get_cvx_relaxation(self):
        """
        Description
        -----------
        Construct a new program by choosing
        the convex constraints and ignoring
        the other ones.
        Note: It is assumed that the program
        has been expanded and transformed
        previously.
        """
        return prog((self.action,self.obj),
                    self.constr._get_convex(),[],self.options)

    # Method: get_vars
    def get_vars(self):
        """
        Description
        -----------
        Construct a set with the variables present
        in the program.
        """
        constr_vars = self.constr.get_vars()
        obj_vars = self.obj.get_vars()
        all_vars = constr_vars
        for v in obj_vars:
            l1 = map(lambda x: x is v,all_vars)
            if(len(l1) != 0):
                if not reduce(lambda x,y: x or y,l1):
                    all_vars += cvxpy_list([v])
            else:
                all_vars += cvxpy_list([v])
        return all_vars

    # Method: get_params
    def get_params(self):
        """
        Description
        -----------
        Construct a set with the parameters present
        in the program.
        """
        constr_params = self.constr.get_params()
        obj_params = self.obj.get_params()
        all_params = constr_params
        for v in obj_params:
            l1 = map(lambda x: x is v,all_params)
            if(len(l1) != 0):
                if not reduce(lambda x,y: x or y,l1):
                    all_params += cvxpy_list([v])
            else:
                all_params += cvxpy_list([v])
        return all_params

    # Method: solve
    def solve(self):
        """
        Description
        -----------
        Solve program.
        """
        obj,lagrange_mul_eq = solve_prog(self)
        return obj

    # Method: _solve_isolating
    def _solve_isolating(self,*args):
        """
        Description
        -----------
        Isolate parameters and then solve program.
        Used by linearize method to obtain subgradient.
        Arguments must be numbers. A very important 
        point is that solve_isolating introduces
        equality constraints and places them at the
        beginning of the constraint list. This is 
        later used to construct the subgradient.
        """

        # Process input
        if(len(args) != 0 and type(args[0]) is list):
            args = args[0]
        
        # Create argument list
        arg_list = []
        for arg in args:
            if(np.isscalar(arg)):
                arg_list += [arg]
            elif(type(arg) is cvxpy_matrix):
                (m,n) = arg.shape
                for i in range(0,m,1):
                    for j in range(0,n,1):
                        arg_list += [arg[i,j]]
            else:
                raise ValueError('Arguments must be numeric')

        # Check number of arguments
        if(len(arg_list) != len(self.params)):
            raise ValueError('Invalid number of arguments')

        # Isolate parameters
        p1_map = {}
        new_constr = cvxpy_list([])
        for p in self.params:
            v = var('v_'+p.name)
            p1_map[p] = v
            new_constr += cvxpy_list([equal(v,p)])
        new_p1 = prog((self.action,re_eval(self.obj,p1_map)),
                      new_constr+re_eval(self.constr,p1_map),
                      self.params, self.options,self.name)

        # Substitute parameters with arguments
        p2_map = {}
        for k in range(0,len(arg_list),1):
            p2_map[new_p1.params[k]] = arg_list[k]
        new_p2 = prog((new_p1.action,re_eval(new_p1.obj,p2_map)),
                      re_eval(new_p1.constr,p2_map),
                      [],new_p1.options,new_p1.name)

        # Solve program
        obj,lagrange_mul_eq = solve_prog(new_p2)
        self.lagrange_mul_eq = lagrange_mul_eq
        return obj
    
    # Method: __str__
    def __str__(self):
        """
        Description
        -----------
        Return string to be shown when printing.
        """
        return self.name

    # Method: show
    def show(self):
        """
        Description
        -----------
        Print description of optimization program.
        """
        if(self.action == MINIMIZE):
            output = '\nminimize '
        else:
            output = '\nmaximize '
        output += str(self.obj)+'\n'
        output += 'subject to\n'
        output += str(self.constr)
        print output

    # Method: __call__
    def __call__(self,*args):
        """
        Description
        -----------
        Call program with specified arguments.
        Parameters are substituted with arguments.
        If all arguments are numeric, the resulting
        optimization program is solved. If some
        arguments are object, a tree is returned.
        
        Arguments
        ---------
        args: List of arguments.
        (Can be numbers or objects)
        """

        # Process input
        if(len(args) != 0 and type(args[0]) is list):
            args = args[0]
        
        # Create argument list
        arg_list = []
        for arg in args:
            if(np.isscalar(arg) or 
               type(arg).__name__ in SCALAR_OBJS):
                arg_list += [arg]
            elif(type(arg) is cvxpy_matrix or 
                 type(arg).__name__ in ARRAY_OBJS):
                (m,n) = arg.shape
                for i in range(0,m,1):
                    for j in range(0,n,1):
                        arg_list += [arg[i,j]]
            else:
                raise ValueError('Invalid argument type')

        # Check number of arguments
        if(len(arg_list) != len(self.params)):
            raise ValueError('Invalid argument syntax')
    
        # Solve if numeric
        if(len(arg_list) == 0 or
           reduce(lambda x,y: x and y,
                  map(lambda x: np.isscalar(x),arg_list))):

            # Substitute parameters with arguments
            p1_map = {}
            for k in range(0,len(arg_list),1):
                p1_map[self.params[k]] = arg_list[k]
            new_p = prog((self.action,re_eval(self.obj,p1_map)),
                         re_eval(self.constr,p1_map),[],
                         self.options,self.name)
            
            # Solve program
            obj,lagrange_mul_eq = solve_prog(new_p)
            return obj        

        # Upgrade numbers to objects
        for i in range(0,len(arg_list),1):
            if(np.isscalar(arg_list[i])):
                arg_list[i] = cvxpy_obj(CONSTANT,
                                        arg_list[i],
                                        str(arg_list[i]))

        # Return tree
        return cvxpy_tree(self,arg_list)

    # Method: is_dcp
    def is_dcp(self,args=None):
        """
        Description
        -----------
        Checks if the program follows DCP rules.
        If args is None, the check is done on the
        body of the program. If args is a list of
        arguments, the parameters are replaced
        with the arguments and the check is done
        on the resulting program. This function
        is called with a list of arguments when 
        cvxpy_tree.is_dcp is executed.
        
        Arguments
        ---------
        args: List of arguments
        """

        # No arguments: Check body of program
        if(args == None):
            if(self.action == MINIMIZE and
               not self.obj.is_convex()):
                return False
            elif(self.action == MAXIMIZE and
                 not self.obj.is_concave()):
                return False
            else:
                return self.constr.is_dcp()

        # Arguments given: Replace parameters and then check
        else:

            # Check if some argument has parameters
            if(len(cvxpy_list(args).get_params()) != 0):
                return False

            # Create a param-arg map
            p_map = {}
            for k in range(0,len(args),1):
                p_map[self.params[k]] = args[k]

            # Re-evaluate
            new_p = prog((self.action,re_eval(self.obj,p_map)),
                         re_eval(self.constr,p_map))

            # Check dcp on resulting program
            return new_p.is_dcp()
    
    # Method: _pm_expand
    def _pm_expand(self,constr):
        """
        Description
        -----------
        Given the constraint, which must be in the form
        self(args) operator variable, the parameters
        are replaced with arguments and then the 
        partial minimization description of the program
        is merged with the constraint.

        Argument
        --------
        constr: cvxpy_constr of the form self(args) 
        operator variable.
        """

        # Get arguments
        args = constr.left.children

        # Create arg-param map by position
        p_map = {}
        for k in range(0,len(args),1):
            p_map[self.params[k]] = args[k]

        # Create new program
        new_p = prog((self.action,re_eval(self.obj,p_map)),
                     re_eval(self.constr,p_map),[],
                     self.options,self.name)

        # Expand partial minimization
        right = constr.right
        new_constr = []
        if(self.curvature == CONVEX):
            new_constr += [less(new_p.obj,right)]
        else:
            new_constr += [greater(new_p.obj,right)]
        new_constr += new_p.constr
        
        # Return constraints
        return cvxpy_list(new_constr)
    
    # Method: _range_constr
    def _range_constr(self,v):
        """
        Description
        -----------
        Dummy method to make the program 
        appear as a function.
        """
        return cvxpy_list([])
    
    # Method: _dom_constr
    def _dom_constr(self,args):
        """
        Description
        -----------
        Dummy method to make the program 
        appear as a function.
        """
        return cvxpy_list([])
    
    # Method: _linearize
    def _linearize(self,args,t2):
        """
        Description
        -----------
        Form linear underestimator or linear
        overestimator of the function depeniding
        on whether the program represents a convex
        or concave function.

        Arguments
        ---------
        args: list of arguments
        t2: variable of right hand side
        """

        x = vstack(args)
        x0 = x.get_value()
        f_x0 = self._solve_isolating(x0)
        lagrange = self.lagrange_mul_eq[0:len(args),0]
        
        if(self.curvature == CONVEX):
            return t2 - (f_x0 - lagrange.T*(x-x0))
        else:
            return (f_x0 + lagrange.T*(x-x0)) - t2
