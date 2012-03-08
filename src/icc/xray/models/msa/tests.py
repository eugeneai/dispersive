import scipy.optimize as op
import numpy as np
fmin=op.fmin
def rosen(x):
    """The Rosenbrock function"""
    return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
xopt = fmin(rosen, x0, xtol=1e-8)
print xopt
