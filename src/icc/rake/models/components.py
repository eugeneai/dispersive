#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1427: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1428: ** components declarations
#!/usr/bin/python
import os, os.path
from zope.interface import implements
from icc.rake.models.interfaces import *
try:
    from collections import OrderedDict
except ImportError:
    # For pythons < 2.7.0
    OrderedDict=dict

#@+node:eugeneai.20110116171118.1429: ** class Model
class Model:
    implements(IModel)
    pass

#@+node:eugeneai.20110116171118.1430: ** class Record
class Record(object):
    pass

#@+node:eugeneai.20110116171118.1431: ** class Module
class Module:
    implements(IModule)
    # IDEF0 taken as a Metamodel
    inputs=OrderedDict()
    outputs=OrderedDict()
    controls=OrderedDict()
    implementors=OrderedDict()
    name="<Module>"
    icon=None # Shoul not be here
    modified=False

#@+node:eugeneai.20110116171118.1432: ** class Canvas
class Canvas:
    implements(ICanvas)

    #@+others
    #@+node:eugeneai.20110116171118.1433: *3* __init__
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
        mp = PlotModule()
        self.place(m1, 70, 150)
        self.place(m2, 200, 30)
        self.place(m3, 500, 100)
        self.place(mp, 300, 300)
        self.connect(m1,m2)
        self.connect(m1,m3)
        self.connect(m2,m3)
        self.connect(m2,mp)

    #@+node:eugeneai.20110116171118.1434: *3* find_module
    def find_module(self, x, y):
        for m, pos in self.modules.iteritems():
            (px, py) = pos
            if abs(px-x)<=16 and abs(py-y)<=16:
                return m
        return None

    #@+node:eugeneai.20110116171118.1435: *3* place
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

    #@+node:eugeneai.20110116171118.1436: *3* updated
    def updated(self):
        self.changed=True

    #@+node:eugeneai.20110116171118.1437: *3* remove
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

    #@+node:eugeneai.20110116171118.1438: *3* get_position
    def get_position(self, module):
        return self.modules[module]

    #@+node:eugeneai.20110116171118.1439: *3* connect
    def connect(self, mfrom, mto):
        self._add_con(mfrom, mto, self.forwards)
        self._add_con(mto, mfrom, self.backwards)

    #@+node:eugeneai.20110116171118.1440: *3* disconnect
    def disconnect(self, mfrom, mto):
        self._rem_con(mfrom, mto, self.forwards)
        self._rem_con(mto, mfrom, self.backwards)

    #@+node:eugeneai.20110116171118.1441: *3* _add_con
    def _add_con(self, mfrom, mto, conns):
        connl=conns.setdefault(mfrom, [])
        if not mto in connl:
            connl.append(mto)
            self.updated()

    #@+node:eugeneai.20110116171118.1442: *3* _rem_con
    def _rem_con(self, mfrom, mto, conns):
        connl=conns.get(mfrom, [])
        while mto in connl:
            connl.remove(mto)
            self.updated()

    #@-others
#@+node:eugeneai.20110116171118.1443: ** class FrameLoadModule
class FrameLoadModule(Module):
    outputs=OrderedDict(data = ('data.frame',))
    icon='ui/pics/frame_open.svg'
    name='Data Frame Loading' 

#@+node:eugeneai.20110116171118.1444: ** class FrameViewModule
class FrameViewModule(Module):
    inputs=OrderedDict(data = ('data.frame',))
    icon='ui/pics/frame_view.svg'
    name='Data Frame Viewing'

#@+node:eugeneai.20110116171118.1445: ** class LmModule
class LmModule(Module):
    inputs=OrderedDict(data = ('data.frame',))
    outputs=OrderedDict(model = ('class.lm',))
    icon='ui/pics/lm.svg'
    name='Linear Regression'

#@+node:eugeneai.20110116171118.1446: ** class PlotModule
class PlotModule(Module):
    inputs=OrderedDict(x = ('',), y=('',))
    outputs=OrderedDict()
    icon='ui/pics/plot.svg'
    name='Plot (anything)'



#@-others
#@-leo
