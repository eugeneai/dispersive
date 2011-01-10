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
    # IDEF0 taken as a Metamodel
    inputs=OrderedDict()
    outputs=OrderedDict()
    controls=OrderedDict()
    implementors=OrderedDict()
    name="<Module>"
    icon=None # Shoul not be here

class Canvas:
    implements(ICanvas)

    def __init__(self):
        self.modules={}
        # connections of the modules
        self.forwards={}
        self.backwards={}
        self.changed=True

        # test case
        m1 = FrameLoadModule()
        m2 = LmModule()
        m3 = FrameViewModule()
        self.place(m1, 20, 20)
        self.place(m2, 200, 30)
        self.place(m3, 500, 100)
        self.connect(m1,m2)
        self.connect(m1,m3)
        self.connect(m2,m3)
        self.exc_mod=m3

    def find_module(self, x, y):
        for m, pos in self.modules.iteritems():
            (px, py) = pos
            if abs(px-x)<=16 and abs(py-y)<=16:
                return m
        return None

    def place(self, module, x, y):
        if module in self.modules:
            (px, py) = self.modules[module]
            if px ==x and py == y:
                pass
            else:
                self.modules[module] = (x, y)
                self.updated()
        else:
                self.modules[module] = (x, y)
                self.updated()

    def updated(self):
        self.changed=True

    def remove(self, module):
        conn_ms=self.forwards.get(module, []) + self.backwards.get(module,[])
        for mto in conn_ms:
            self.disconnect(module, mto)
            self.disconnect(mto, module)
        if module in self.forwards:
            del self.forwards[module]
        if module in self.backwards:
            del self.backwards[module]
        del self.modules[module]

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
            self.updated()
            
    def _rem_con(self, mfrom, mto, conns):
        connl=conns.get(mfrom, [])
        while mto in connl:
            connl.remove(mto)
            self.updated()

class FrameLoadModule(Module):
    outputs=OrderedDict(data = ('data.frame',))
    icon='ui/pics/frame_open.svg'
    name='Load a Data Frame'
    
class FrameViewModule(Module):
    inputs=OrderedDict(data = ('data.frame',))
    icon='ui/pics/frame_view.svg'
    name='View a Data Frame'

class LmModule(Module):
    inputs=OrderedDict(data = ('data.frame',))
    outputs=OrderedDict(model = ('model.lm',))
    icon='ui/pics/lm.svg'
    name='Linear Regression'
    
    

