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

# Groups
SCALAR_OBJS = ['cvxpy_scalar_var','cvxpy_scalar_param','cvxpy_tree']
ARRAY_OBJS = ['cvxpy_var','cvxpy_param','cvxpy_expression']

# Object types
OPERATOR = 'operator'
CONSTANT = 'constant'
FUNCTION = 'function'
VARIABLE = 'variable'
PARAMETER = 'parameter'
TREE = 'tree'
SET = 'set'
EXPRESSION = 'expression'

# Function and set expansion types
SDC = 'sdc'
SOC = 'soc'
DIF = 'dif'
PM = 'pm'

# Curvature
CONVEX = 'convex'
CONCAVE = 'concave'

# Monotonicity
INCREASING = 'increasing'
DECREASING = 'decreasing'
NEITHER = 'neither'

# Action
MINIMIZE = 'minimize'
MAXIMIZE = 'maximize'
 
# SCP Algorithm
SCP_ALG_OPT = {'top residual':1e1,
               'tight tol':1e-4,
               'lambda multiplier':5.0,
               'max lambda':1e5,
               'starting lambda':1e0,
               'max scp iter':100}

# SCP Solver
SCP_SOLVER_OPT ={'check redundancy':False,
                 'solver progress':False,
                 'show steps':False,
                 'maxiters':150,
                 'abstol':1e-6,
                 'reltol':1e-5,
                 'feastol':1e-6}

# Solve Convex
RELAX_SOLVER_OPT ={'check redundancy':False,
                   'solver progress':True,
                   'show steps':False,
                   'maxiters':150,
                   'abstol':1e-6,
                   'reltol':1e-5,
                   'feastol':1e-6}
