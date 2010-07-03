
from zope.interface import Interface, Attribute

class IModel(Interface):
    """Just marker interface, to mark models
    """

class ISpectra(IModel):
    """Interface denoting Spectral data model.
    It is a list of spectral counts.
    """
    source  = Attribute("The source of the data.")
    scale = Attribute("Scale data.")
    spectra = Attribute("List of spectral counts")
    
    
