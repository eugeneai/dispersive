
from zope.interface import Interface, Attribute

class IModel(Interface):
    """Just marker interface, to mark models
    """

class ICanvas(IModel):
    """Canvas for data processing scheme construction.
    Basic idea taken from Orange project, but impoemented
    on the basis of ZCA.
    """
