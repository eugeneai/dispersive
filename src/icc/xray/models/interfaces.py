
from zope.interface import Interface, Attribute

class IModel(Interface):
    """Just marker interface, to mark models
    """

class ISpectra(IModel):
    """Interface denoting Spectral data model.
    It is a list of spectral counts.
    """
    source  = Attribute("The source of the data (model).")
    scale = Attribute("Scale of X-axis of the data.")
    spectra = Attribute("List of pairs (spectral counts, plotting_attributes dictionary)")
    
class IProject(IModel):
    """Interface denoting a Project.
    Structure, based on XML.
    """
