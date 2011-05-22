from spy.scalar import *
from spy.constants import *
from spy.functions import *
from spy.constraint import *
from spy.problem import *
from spy.utils import *
from interface import *

__all__  = interface.__all__
__all__ += functions.__all__
#__all__ += ["scalar", "scalar_var", "constraint", "problem"]


# from interface import *
# from cvxpy.utils import *
# from cvxpy.atoms import *
# from cvxpy.sets import *

# __all__ = interface.__all__
# __all__ += utils.__all__ 
# __all__ += atoms.__all__ 
# __all__ += sets.__all__
