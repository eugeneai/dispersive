#!/usr/bin/python
import os, os.path
from zope.interface import implements
from icc.rake.models.interfaces import *
    
class Model:
    implements(IModel)
    pass

class Canvas:
    implements(ICanvas)
    pass
