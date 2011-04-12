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
import cvxopt as opt
from expand import *
from transform import *
from cvxpy.defs import *
from cvxopt import solvers
from cvxopt import lapack
from cvxpy.constraints import cvxpy_list

# Function
def solve_convex(p,mode):
    """
    Description
    -----------
    Solves the convex program p. It assumes p is the convex part 
    of an expanded and transformed program.

    Arguments
    ---------
    p: convex cvxpy_program.    
    mode: 'rel' (relaxation) or 'scp' (sequential convex programming).
    """

    # Select options
    if(mode == 'scp'):
        options = p.options['SCP_SOL']
    else:
        options = p.options['REL_SOL']
    quiet = p.options['quiet']

    # Printing format for cvxopt sparse matrices
    opt.spmatrix_str = opt.printing.spmatrix_str_triplet 	
    
    # Partial minimization expansion
    constr_list = pm_expand(p.constr)
    
    # Get variables
    variables = constr_list.get_vars()

    # Count variables
    n = len(variables)

    # Create a map (var - pos)
    if(options['show steps'] and not quiet):
        print '\nCreating variable - index map'
    var_to_index = {}
    for i in range(0,n,1):
        if(options['show steps'] and not quiet):
            print variables[i],'<-->',i
        var_to_index[variables[i]] = i

    # Construct objective vector
    c = construct_c(p.obj,var_to_index,n,p.action)
    if(options['show steps'] and not quiet):
        print '\nConstructing c vector'
        print 'c = '
        print c

    # Construct Ax == b
    A,b = construct_Ab(constr_list._get_eq(),var_to_index,n,options)
    if(options['show steps'] and not quiet):
        print '\nConstructing Ax == b'
        print 'A ='
        print A
        print 'b ='
        print b

    # Construct  Gx <= h
    G,h,dim_l,dim_q,dim_s = construct_Gh(constr_list._get_ineq_in(),
                                         var_to_index,n)
    if(options['show steps'] and not quiet):
        print '\nConstructing Gx <= h'
        print 'G ='
        print G
        print 'h ='
        print h
    
    # Construct F
    F = construct_F(constr_list._get_ineq_in(),var_to_index,n)
    if(options['show steps'] and not quiet):
        print '\nConstructing F'

    # Call cvxopt
    solvers.options['show_progress'] = options['solver progress'] and not quiet
    solvers.options['maxiters'] = options['maxiters']
    solvers.options['abstol'] = options['abstol']
    solvers.options['reltol'] = options['reltol']
    solvers.options['feastol'] = options['feastol']
    dims = {'l':dim_l, 'q':dim_q, 's':dim_s}
    if(F is None):
        if(options['show steps'] and not quiet):
            print '\nCalling cvxopt conelp solver'
        r =  solvers.conelp(c,G,h,dims,A,b)
    else:
        if(options['show steps'] and not quiet):
            print '\nCalling cvxopt cpl solver'
        r =  solvers.cpl(c,F,G,h,dims,A,b)

    # Store numerical values
    if(r['status'] != 'primal infeasible'):
        if(options['show steps'] and not quiet):
            print '\nStoring numerical values:'
        for v in variables:
            value = r['x'][var_to_index[v]]
            v.data =  value
            if(options['show steps']and not quiet):
                print v,' <- ', v.data

    # Return result
    return r

# Function
def construct_c(objective,mapping,n,action):
    """
    Description
    -----------
    Creates the vector c for the objective function c.T*x

    Arguments
    ---------
    objective: cvxpy_scalar_var or cvxpy_obj
    mapping: Map from variable to index.
    n: Size for vector c.
    action: MINIMIZE OR MAXIMIZE
    """

    # Check obj
    if(objective.type != CONSTANT and
       objective.type != VARIABLE):
        raise ValueError('Bad objective: Cannot construct c')

    # Construct c vector
    c = opt.matrix(0.0,(n,1))
    obj_vars = objective.get_vars()
    if(len(obj_vars) == 0):
        return c
    else:
        obj_var = obj_vars[0]
        i = mapping[obj_var]
        if(action == MINIMIZE):
            c[i] = 1.0
        else:
            c[i] = -1.0
    
    # Return vector
    return c

# Function 
def construct_Ab(constr_list,mapping,n,options):
    """
    Description
    -----------
    Constructs matrix A and vector b from a list 
    of equality constraints. The program is assumed 
    to be expanded and transformed so all the
    equality constraints are affine.
    
    Arguments
    ---------
    constr_list: cvxpy_list of equality constraints.
    Mapping: Dictionary mapping variable to index.
    n: Number of variables.
    """

    # Create matrices
    A = opt.spmatrix(0.0,[],[],(0,n))
    b = opt.matrix(0.0,(0,1))
    H_top = opt.sparse([[A],[b]])
    rank = 0
    counter = 1
    for constr in constr_list:

        # Get elements
        left = constr.left
        op = constr.op
        right = constr.right

        # New rows
        A_row = opt.spmatrix(0.0,[],[],(1,n))
        b_row = opt.matrix(0.0,(1,1))

        # Deal with right element
        if(right.type == CONSTANT):
            b_row[0] += right.data*1.0
        elif(right.type == VARIABLE):
            A_row[0,mapping[right]] += -1.0
        else:
            raise ValueError('Bad equality: Cannot construct A')

        # Left is a variable
        if(left.type == VARIABLE):
            A_row[0,mapping[left]] += 1.0
   
        # Left is a constant
        elif(left.type == CONSTANT):
             b_row[0] += -left.data*1.0

        # Left is an operation tree
        elif(left.type == TREE and 
             left.item.type == OPERATOR):

            # Get operator name
            name = left.item.name
            
            # Addition
            if(name == '+'):
                for arg in left.children:
                    if(arg.type == TREE and
                       arg.item.name == '*'):
                        ch1 = arg.children[1]
                        ch0 = arg.children[0]
                        A_row[0,mapping[ch1]] += ch0.data
                    elif(arg.type == VARIABLE):
                        A_row[0,mapping[arg]] += 1.0
                    elif(arg.type == CONSTANT):
                        b_row[0] += -arg.data*1.0
                    else:
                        raise ValueError('Bad equality: Cannot construct A')

            # Multiplication
            elif(name == '*'):
                
                # Constant
                op1 = left.children[0]

                # Variable
                op2 = left.children[1]

                # Process
                A_row[0,mapping[op2]] += 1.0*op1.data
            
            # Error
            else:
                raise ValueError('Bad equality: Cannot construct A')
    
        # Error
        else:
            raise ValueError('Bad equality: Cannot construct A')
        
        # Rank check
        if(options['check redundancy']):
            H_botton = opt.sparse([[A_row],[b_row]])
            H = opt.sparse([H_top,H_botton])
            svd = opt.matrix(0.0,(1,np.min([H.size[0],H.size[1]]))) 
            lapack.gesvd(opt.matrix(H),svd)
            new_rank = len([x for x in svd if x > 1e-8])
            if(new_rank > rank):
            
                # Append
                A = opt.sparse([A,A_row])
                b = opt.matrix([b,b_row])
            
                # Update rank and H_top
                rank = new_rank
                H_top = H
            else:
                if(options['show steps'] and not quiet):
                    print 'Redundant equality eliminated [',counter,']'
                    counter += 1
        else:

            # Append
            A = opt.sparse([A,A_row])
            b = opt.matrix([b,b_row])

    # Return matrices
    return A,b

# Function
def construct_Gh(constr_list,mapping,n):
    """
    Description
    -----------
    Creates the matrix G and vector h from a list 
    of inequality and membership constraints.
    
    Arguments
    ---------
    constr_list: cvxpy_list of inequality and membership constraints.
    mapping: A map from variable to index.
    n: Number of varaibles.
    """

    # Make sure constraints are well formed
    for c in constr_list:
        if(c.left.type == EXPRESSION):
            if(c.right.type != SET):
                raise ValueError('Bad inequality: Cannot construct G')
        elif(c.left.type != TREE):
            if((c.left.type != VARIABLE and c.left.type != CONSTANT) or
               (c.right.type != VARIABLE and c.right.type != CONSTANT)):
                raise ValueError('Bad inequality: Cannot construct G')
        else:
            if((c.left.item.type != FUNCTION) or
               (c.right.type != VARIABLE)):
                raise ValueError('Bad inequality: Cannot construct G')  

    # Initialize G,h and dimensions
    dim_l = 0
    dim_q = []
    dim_s = []
    G = opt.spmatrix(0.0,[],[],(0,n))
    h = opt.matrix(0.0,(0,1))

    # Nonnegative Orthant
    for c in constr_list:
        
        # Left is constant or variable
        if(c.left.type == CONSTANT or c.left.type == VARIABLE):

            # Get constraint elements
            op_name = c.op
            ob1 = c.left
            ob2 = c.right

            # New row
            rowG = opt.spmatrix(0.0,[],[],(1,n))
            rowh = opt.matrix(0.0,(1,1))
            if(ob1.type == VARIABLE):
                rowG[0,mapping[ob1]] += 1.0 if op_name=='<=' else -1.0
            else:
                rowh[0,0] += -ob1.data*1.0 if op_name=='<=' else ob1.data*1.0
            if(ob2.type == VARIABLE):
                rowG[0,mapping[ob2]] += 1.0 if op_name=='>=' else -1.0
            else:
                rowh[0,0] += -ob2.data*1.0 if op_name=='>=' else ob2.data*1.0

            # Attach to G,h
            G = opt.sparse([G,rowG])
            h = opt.matrix([h,rowh])

            # Increment size of cone
            dim_l = dim_l + 1
        
    # Semidefinite cone
    for c in constr_list:

        # Left is a function that expands to LMI
        if(c.left.type == TREE and
           c.left.item.type == FUNCTION and
           c.left.item.expansion_type == SDC):

            # Get function
            fn = c.left.item

            # Get arguments
            args = c.left.children

            # Get right side variable
            r_var = c.right

            # Get G,h section
            newG,newh,t = fn._construct(args,r_var,mapping,n)

            # Attach to G,h
            G = opt.sparse([G,newG])
            h = opt.matrix([h,newh])

            # Attach size of cone
            dim_s = dim_s + [t]

        # Set membership that expands to LMI
        elif(c.left.type == EXPRESSION and
             c.right.expansion_type == SDC):
            
            # Get G,h, section
            el = c.left
            set_atom = c.right
            newG,newh,t = set_atom._construct(el,mapping,n)

            # Attach to G,h
            G = opt.sparse([G,newG])
            h = opt.matrix([h,newh])

            # Attach size of cone
            dim_s = dim_s + [t]
    
    # Second order cone
    for c in constr_list:

        # Set membership that expands to SOC
        if(c.left.type == EXPRESSION and
           c.right.expansion_type == SOC):
        
            # Get G,h, section
            el = c.left
            set_atom = c.right
            newG,newh,r = set_atom._construct(el,mapping,n)

            # Attach to G,h
            G = opt.sparse([G,newG])
            h = opt.matrix([h,newh])

            # Attach size of cone
            dim_q = dim_q + [r]
        
    # Return 
    return G,h,dim_l,dim_q,dim_s

# Function
def construct_F(constr_list,mapping,n):
    """
    Description
    -----------
    Constructs the function F needed by cvxopt 
    to solve nonlinear programs.
    
    Arguments
    ---------
    constr_list: List of inequality constraints.
    mapping: Map from variables to indeces.
    n: Numbe of variables.
    """

    # Lists
    fs = []
    grads = []
    hess = []
    inds = []
    
    for c in constr_list:

        # Function that has a (f,gradf,hessf) implementation
        if(c.left.type == TREE and
           c.left.item.type == FUNCTION and
           c.left.item.expansion_type == DIF):

            # Get function
            fn = c.left.item

            # Get arguments
            args = c.left.children

            # Get right side variable
            r_var = c.right
            if(r_var.type != VARIABLE):
                raise ValueError('Bad inequality: Cannot construct F')

            # Get functions from atom
            n_f,n_grad,n_hess,n_ind = fn._construct(args,r_var,
                                                    mapping,n)
            
            # Append
            fs = fs + [n_f]
            grads = grads + [n_grad]
            hess = hess + [n_hess]
            inds = inds + [n_ind]

    # Check if no functions
    if(len(fs) == 0):
        return None

    # Construct F
    def F(x=None,z=None):
        
        # Case 1
        if(x is None and z is None):
            x0 = opt.matrix(np.ones((n,1)))*1.0
            return (len(fs),x0)

        # Case 2
        elif(x is not None and z is None):

            in_domain = map(lambda y: y(x),inds)
            if(reduce(lambda v,w: v and w,in_domain)):
                f = opt.matrix(0.0,(len(fs),1))
                for i in range(0,len(fs),1):
                    f[i] = fs[i](x)
                Df = opt.spmatrix(0.0,[],[],(0,n))
                for i in range(0,len(grads),1):
                    Df = opt.sparse([Df,grads[i](x).T])
                return (f,Df)
            else:
                return (None,None)

        # Case 3
        else:
            f = opt.matrix(0.0,(len(fs),1))
            for i in range(0,len(fs),1):
                f[i] = fs[i](x)
            Df = opt.spmatrix(0.0,[],[],(0,n))
            for i in range(0,len(grads),1):
                Df = opt.sparse([Df,grads[i](x).T])
            H = opt.spmatrix(0.0,[],[],(n,n))
            for i in range(0,len(hess),1):
                H = H + z[i]*hess[i](x)
            return (f,Df,H)

    # Return F
    return F

# Function: Partial minimization expand
def pm_expand(constr_list):
    """
    Description
    -----------
    Expands functions which are implemented
    using partial minimization descriptions.
    constr_list: cvxpy_list of constraints.

    Arguments
    ---------
    constr_list: cvxpy_list of constraints.
    """

    new_list = cvxpy_list([])
    for c in constr_list:
        if(c.left.type == TREE and
           c.left.item.type == FUNCTION and
           c.left.item.expansion_type == PM):
            new_constr = transform(expand(c.left.item._pm_expand(c)))
            new_constr = pm_expand(new_constr._get_convex())
            new_list += new_constr
        elif(c.left.type == EXPRESSION and
             c.right.type == SET and
             c.right.expansion_type == PM):
            new_constr = transform(expand(c.right._pm_expand(c)))
            new_constr = pm_expand(new_constr._get_convex())
            new_list += new_constr
        else:
            new_list += cvxpy_list([c])

    # Return new list
    return new_list
