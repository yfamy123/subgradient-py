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
from expand import *
from solve_convex import *
from cvxpy.atoms import abs
from cvxpy.constraints import cvxpy_list
from cvxpy.interface import prog

# Function
def scp(p,bad_constr,sol):
    """
    Description: Sequential convex programming
    algorithm. Solve program p and try to 
    enforce equality on the bad constraints.
    Argument p: cvxpy_program is assumed to be in
    expanded and equivalent format.
    Argument bad_constr: List of nonconvex
    constraints, also in expanded and equivalent
    format.
    Argument sol: Solution of relaxation.
    """

    # Quit if program is linear
    if(len(bad_constr) == 0):
        if(not p.options['quiet']):
            print 'Tightening not needed'
        return True

    # Get parameters
    tight_tol = p.options['SCP_ALG']['tight tol']
    starting_lambda = p.options['SCP_ALG']['starting lambda'] 
    max_scp_iter = p.options['SCP_ALG']['max scp iter']
    lambda_multiplier = p.options['SCP_ALG']['lambda multiplier']
    max_lambda = p.options['SCP_ALG']['max lambda']
    top_residual = p.options['SCP_ALG']['top residual']

    # Construct slacks
    slacks = [abs(c.left-c.right) for c in bad_constr]

    # Print header
    if(not p.options['quiet']):
        print 'Iter\t:',
        print 'Max Slack\t:',
        print 'Objective\t:',
        print 'Solver Status\t:',
        print 'Pres\t\t:',
        print 'Dres\t\t:',
        print 'Lambda Max/Min'

    # SCP Loop
    lam = starting_lambda*np.ones(len(slacks))
    for i in range(0,max_scp_iter,1):

        # Calculate max slack
        max_slack = max(map(lambda x:x.get_value(), slacks))

        # Quit if status is primal infeasible
        if(sol['status'] == 'primal infeasible'):
            if(not p.options['quiet']):
                print 'Unable to tighten: Problem became infeasible'
            return False

        # Check if dual infeasible
        if(sol['status'] == 'dual infeasible'):
            sol['status'] = 'dual inf'
            sol['primal infeasibility'] = np.NaN
            sol['dual infeasibility'] = np.NaN

        # Print values
        if(not p.options['quiet']):
            print '%d\t:' %i,
            print '%.3e\t:' %max_slack,
            print '%.3e\t:' %p.obj.get_value(),
            print '   '+sol['status']+'\t:',
            if(sol['primal infeasibility'] is not np.NaN):
                print '%.3e\t:' %sol['primal infeasibility'],
            else:
                print '%.3e\t\t:' %sol['primal infeasibility'],
            if(sol['dual infeasibility'] is not np.NaN):
                print '%.3e\t:' %sol['dual infeasibility'],
            else:
                print '%.3e\t\t:' %sol['dual infeasibility'],
            print '(%.1e,%.1e)' %(np.max(lam),np.min(lam))

        # Quit if max slack is small
        if(max_slack < tight_tol and
           sol['status'] == 'optimal'):
            if(not p.options['quiet']):
                print 'Tightening successful'
            return True

        # Quit if residual is too large
        if(sol['primal infeasibility'] >= top_residual or
           sol['dual infeasibility'] >= top_residual):
            if(not p.options['quiet']):
                print 'Unable to tighten: Residuals are too large'
            return False

        # Linearize slacks
        linear_slacks = []
        for c in bad_constr:
            fn = c.left.item
            args = c.left.children
            right = c.right
            line = fn._linearize(args,right)
            linear_slacks += [line]

        # Add linearized slacks to objective
        sum_lin_slacks = 0.0
        for j in range(0,len(slacks),1):
            sum_lin_slacks += lam[j]*linear_slacks[j]
        if(p.action == MINIMIZE):
            new_obj = p.obj + sum_lin_slacks
        else:
            new_obj = p.obj - sum_lin_slacks
        new_t0, obj_constr = expand(new_obj)    
        new_p = prog((p.action,new_t0), obj_constr+p.constr,[],p.options)

        # Solve new problem
        sol = solve_convex(new_p,'scp')

        # Update lambdas
        for j in range(0,len(slacks),1):
            if(slacks[j].get_value() >= tight_tol):
                if(lam[j] < max_lambda):
                    lam[j] = lam[j]*lambda_multiplier

    # Maxiters reached
    if(not p.options['quiet']):
        print 'Unable to tighten: Maximum iterations reached'
    if(sol['status'] == 'optimal'):
        return True
    else:
        return False
