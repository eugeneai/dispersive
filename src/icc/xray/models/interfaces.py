#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1361: * @file interfaces.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1362: ** interfaces declarations

from zope.interface import Interface, Attribute

#@+node:eugeneai.20110116171118.1368: ** Interfaces
#@+node:eugeneai.20110116171118.1363: *3* IModel
class IModel(Interface):
    """Just marker interface, to mark models
    """

#@+node:eugeneai.20110116171118.1364: *3* ISpectra
class ISpectra(IModel):
    """Interface denoting Spectral data model.
    It is a list of spectral counts.
    """
    source  = Attribute("The source of the data (model).")
    scale = Attribute("Scale of X-axis of the data.")
    spectra = Attribute("List of pairs (spectral counts, plotting_attributes dictionary)")

#@+node:eugeneai.20110116171118.1365: *3* IProject
class IProject(IModel):
    """Interface denoting a Project.
    Structure, based on XML.
    """

class IAnalysisTask(IModel):
    """Selection of the elements, methods,
    graduation, etc.
    """
#@-others
#@-leo
