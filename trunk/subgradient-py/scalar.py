from defs import *

# Base class
class expr(object):
    def __init__(self, func = None, children = []):
        self.func     = func
        self.children = children
    def get_value(self):
    	values = map(lambda x: x.get_value(), self.children)
        return self.func(values)
    def __str__(self):
        strs = map(lambda x: x.__str__(), self.children)
        if(self.func.name == 'sum'):
            ret = '(' + '+'.join(strs) + ')'
        else:
            ret = self.func.name + '(' + ', '.join(strs) + ')'
        return ret

class scalar(expr):
    def __init__(self, value = None):
        self.value = value
    def get_value(self):
        return self.value
    def __str__(self):
        return str(self.value)

class scalar_var(expr):
    def __init__(self, name = None):
        self.name = name
    def __str__(self):
        return self.name
