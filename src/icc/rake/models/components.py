#!/usr/bin/python
import os, os.path
from zope.interface import implements
from icc.rake.models.interfaces import *

class Model:
    implements(IModel)
    pass

class Record(object):
    pass
    
class Module():
    implements(IModule)
    # class fields
    inputs=[]
    outputs=[]
    controls=[]
    name="<Module>"
    icon=None # Shoul not be here

class Canvas:
    implements(ICanvas)

    def __init__(self):
        self.modules={}
        # connections of the modules
        self.forwards={}
        self.backwards={}

    def place(self, module, x, y):
        self.modules[module]=(x, y)

    def remove(self, module):
        del self.forwards[module]
        del self.backwards[module]

    def get_position(self, module):
        return self.modules[module]

    def connect(self, mfrom, mto):
        self._add_con(mfrom, mto, self.forwards)
        self._add_con(mto, mfrom, self.backwards)

    def disconnect(self, mfrom, mto):
        self._rem_con(mfrom, mto, self.forwards)
        self._rem_con(mto, mfrom, self.backwards)

    def _add_con(self, mfrom, mto, conns):
        connl=conns.setdefault(mfrom, [])
        if connl.find(mto) != -1:
            connl.append(mto)
            
    def _rem_con(self, mfrom, mto, conns):
        connl=conns.get(mfrom, None)
        if connl == None:
            return 
        idx = connl.find(mto)
        if idx != -1:
            del connl[idx]


