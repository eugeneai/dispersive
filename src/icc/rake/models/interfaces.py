#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1447: * @file interfaces.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1448: ** interfaces declarations

from zope.interface import Interface, Attribute

#@+node:eugeneai.20110116171118.1449: ** class IModel
class IModel(Interface):
    """Just marker interface, to mark models
    """

#@+node:eugeneai.20110116171118.1450: ** class ICanvas
class ICanvas(IModel):
    """Canvas for data processing scheme construction.
    Basic idea taken from Orange project, but impoemented
    on the basis of ZCA.
    """

#@+node:eugeneai.20110116171118.1451: ** class IModule
class IModule(IModel):
    """Module model """

#@-others
#@-leo
