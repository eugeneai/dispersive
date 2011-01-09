#!/usr/bin/python
import os, os.path
from zope.interface import implements
from icc.rake.models.interfaces import *
from collections import OrderedDict

class Model:
    implements(IModel)
    pass

class Record(object):
    pass
    
class Module:
    implements(IModule)
    # class fields
    inputs=OrderedDict()
    outputs=OrderedDict()
    controls=OrderedDict()
    name="<Module>"
    icon=None # Shoul not be here

class Canvas:
    implements(ICanvas)

    def __init__(self):
        self.modules={}
        # connections of the modules
        self.forwards={}
        self.backwards={}

        # test case
        m1 = FrameLoadModule()
        m2 = FrameViewModule()
        self.place(m1, 20,20)
        self.place(m2, 50, 30)
        self.connect(m1,m2)

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
        if not mto in connl:
            connl.append(mto)
            
    def _rem_con(self, mfrom, mto, conns):
        connl=conns.get(mfrom, [])
        if mfrom in connl:
            del connl[idx]

class FrameLoadModule(Module):
    #outputs['data']=('data.frame',)
    icon='ui/pics/frame_open.svg'
    name='Load a Data Frame'
    
class FrameViewModule(Module):
    #inputs['data']=('data.frame',)
    icon='ui/pics/frame_view.svg'
    name='View a Data Frame'
    

