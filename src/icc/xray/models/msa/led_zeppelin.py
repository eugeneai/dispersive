import numpy as np
import scipy.optimize as op
import scipy.special as fn
import pylab as p
import math

fi=np.arange(-1*math.pi, 1*math.pi, 0.01)

p.plot(fi, 1-p.cos(fi))
p.show()
