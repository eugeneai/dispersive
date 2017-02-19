#!/usr/bin/python -u
# encoding:utf-8

import math
import numpy as n
from pylab import *
from lxml import etree
import sys

if len(sys.argv)==1:
    filename = "Co_5_2.spx"
else:
    filename = sys.argv[1]

tt=n.dtype(float_)
x=n.arange(4096, dtype = tt)
y=n.zeros(4096, dtype = tt)
for i in x:
    y[i]=i/200*math.sin(i/200)

i=open(filename)
r = etree.parse(i)

sps = r.xpath("//Channels/text()")

sps = [n.array(list(map(int,sp.split(',')))) for sp in sps]

print("Number of spectra found:", len(sps))

for sp in sps:
    plot(x,sp)

title("Plot of the spectra from '%s'" % filename)

show()

print('The prog has been stopped successfully!!!')


