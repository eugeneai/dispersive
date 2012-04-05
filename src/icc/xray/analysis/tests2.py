import numpy as np
import pylab as p
import scipy
print help(scipy.version)
from scipy.signal import *
xs = np.arange(0, np.pi*8, 0.05)
data = np.sin(xs)+np.sin(xs*400)*10.
peakind = find_peaks_cwt(data, np.arange(5,6))
print peakind, xs[peakind],data[peakind]
p.plot(xs, data)
for i in peakind:
    p.axvline(xs[i], color=(0,0,0))
p.show()
