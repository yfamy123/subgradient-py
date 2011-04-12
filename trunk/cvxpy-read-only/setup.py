from distutils.core import setup

setup(  name='cvxpy',
        version='0.0.1',
        description='CVXPY Setup',
        author='Tomas Tinoco de Rubira',
        author_email='ttinoco@stanford.edu',
        url='http://www.stanford.edu/~ttinoco',
        packages=['cvxpy','cvxpy.atoms','cvxpy.procedures','cvxpy.sets'],
    )

