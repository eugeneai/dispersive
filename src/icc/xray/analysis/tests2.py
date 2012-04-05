import numpy as np
import pylab as p
import scipy
print help(scipy.version)
from scipy.signal import *
xs = np.arange(0, np.pi, 0.05)
data = np.sin(xs)
peakind = find_peaks_cwt(data, np.arange(1,10))
print peakind, xs[peakind],data[peakind]
