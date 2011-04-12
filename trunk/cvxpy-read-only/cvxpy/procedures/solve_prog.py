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

from scp import *
import numpy as np
from solve_convex import *
from cvxpy.constraints import cvxpy_list
from cvxpy.interface import var_reset,matrix

# Function
def solve_prog(p):
    """
    Description
    -----------
    Solve optimization program.

    Arguments
    ---------
    p: cvxpy_program
    """

    # Reset variable counter
    var_reset()

    # Check parameters
    if(len(p.get_params()) != 0):
        if(not p.options['quiet']):
            print 'Error: Parameters present'
        return np.NaN,np.NaN

    # Original
    if(p.options['show steps'] and not p.options['quiet']):
        print '\n'
        print '****************************'
        print '*         Original         *'
        print '****************************'
        p.show()

    # Expanded
    p_expanded = p._get_expanded()
    if(p.options['show steps'] and not p.options['quiet']):
        print '\n'
        print '****************************'
        print '*         Expanded         *'
        print '****************************'
        p_expanded.show()

    # Equivalent
    p_equivalent = p_expanded._get_equivalent()
    if(p.options['show steps'] and not p.options['quiet']):
        print '\n'
        print '****************************'
        print '*       Equivalent         *'
        print '****************************'
        p_equivalent.show()

    # Nonconvex constraints
    bad_constr = p_equivalent.constr._get_nonconvex()
    if(p.options['show steps'] and not p.options['quiet']):
        print '\n'
        print '****************************'
        print '*  Nonconvex Constraints   *'
        print '****************************\n'
        print bad_constr

    # Convex Relaxation
    p_cvx_relaxation = p_equivalent._get_cvx_relaxation()
    if(p.options['show steps'] and not p.options['quiet']):
        print '\n'
        print '****************************'
        print '*    Convex Relaxation     *'
        print '****************************'
        p_cvx_relaxation.show()

    # Solve convex relaxation
    if(not p.options['quiet']):
        print '\nSolving convex relaxation ...'
    sol = solve_convex(p_cvx_relaxation,'rel')
    lagrange_mul_eq = matrix(sol['y'])
    if(not p.options['quiet']):
        print 'Relaxation status: ',sol['status']
    
    # Relaxation status: primal infeasible
    if(sol['status'] == 'primal infeasible'):
        if(not p.options['quiet']):
            print 'Original program is primal infeasible'
        if(p.action == MINIMIZE):
            return np.inf,lagrange_mul_eq
        else:
            return -np.inf,lagrange_mul_eq
        
    # Relaxation status: uknown
    elif(sol['status'] == 'unknown'):
        relaxation_obj = None

    # Relaxation status: dual infeasible
    elif(sol['status'] == 'dual infeasible'):
        if(p.action == MINIMIZE):
            relaxation_obj = -np.inf
        else:
            relaxation_obj = np.inf

    # Relaxacion status: optimal
    else:
        relaxation_obj = p_cvx_relaxation.obj.get_value()

    # Report max slack
    if(len(bad_constr) != 0 and not p.options['quiet']):
        print 'Max Slack: ',
        print max(map(lambda x:x.get_value(),
                      [abs(c.left-c.right) for c in bad_constr]))

    # Tighten
    if(p.options['show steps'] and not p.options['quiet']):
        print '\n'
        print '****************************'
        print '*    Tightening Stage      *'
        print '****************************'
    elif(not p.options['quiet']):
        print '\nAttempting tightening ...'
    valid_scp = scp(p_cvx_relaxation,bad_constr,sol)
    if(not valid_scp):
        return np.NaN,np.NaN

    # Prepare results
    if(len(bad_constr) == 0):
        obj = relaxation_obj
    else:
        obj = p.obj.get_value()
    if(p.action == MINIMIZE):
        bound_str = 'Lower Bound'
        if(relaxation_obj != None):
            bound = np.min([relaxation_obj,obj])
            gap = np.max([obj-relaxation_obj,0.0])
    else:
        bound_str = 'Upper Bound'
        if(relaxation_obj != None):
            bound = np.max([relaxation_obj,obj])
            gap = np.max([relaxation_obj-obj,0.0])

    # Show results
    if(p.options['show steps'] and not p.options['quiet']):
        print '\n'
        print '****************************'
        print '*        Results           *'
        print '****************************'
    elif(not p.options['quiet']):
        print '\nResults'
    if(not p.options['quiet']):
        print 'Objective =\t%.5e' %obj
        if(relaxation_obj != None):
            print bound_str+' =\t%.5e' %bound
            print 'Gap =\t\t%.5e' %gap
        else:
            print bound_str+' =\tUnknown'
            print 'Gap =\t\tUnknown'
        if(len(bad_constr) != 0):
            ms = max(map(lambda x:x.get_value(),
                         [abs(c.left-c.right) for c in bad_constr]))
            print 'Max Slack =\t%.5e' %ms

    # Return objective and dual var
    return obj,lagrange_mul_eq
