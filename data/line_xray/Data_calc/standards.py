import _standards as _sts
from appliance import *

"""
# standards
CHANNEL_NAMES=[
# 1     2     3     4    5    6
"Na", "Mg", "Al", "Si", "P", "S", 
# 7     8     9   10
"Cl", "K", "Ca", "Ti", 
#11    12    13    14   15    16
"V", "Cr", "Mn", "Fe", "Co", "Ba"
]
"""

# get names of the standards
names=_sts.__dict__.keys()
names.sort()
n1=[]
for n in names:
	if n[0]!="_" and n!="STANDARDS":
		n1.append(n)
		
_STANDARS=_sts.STANDARDS
names=n1
del n1

# set standards as arrays for their channels
STANDARDS={}
for name in names:
	st=_sts.__dict__[name]
	l=[]
	for NAME in CHANNEL_NAMES:
		l.append(st[NAME])
	globals()[name]=l
	STANDARDS[name]=l
