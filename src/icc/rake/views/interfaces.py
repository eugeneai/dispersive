#!/usr/bin/python

import zope.interface as ZI

class IView(ZI.Interface):
    model = ZI.Attribute("Project under exploration. The MVC Model.")
    ui = ZI.Attribute("User interface component holder.")

class IPanelView(IView):
    """A View viewn as a panel (not a window)"""

class IWindowView(IView):
    """A View viewn as a window"""

class IProjectView(IPanelView):
    """View the a project. To make "New" action working applications
    shoud adapt this interface to their models.
    """

class ICanvasView(IProjectView):
    """We use drawing canvas as main project view
    """

class IApplication(IWindowView):
    def remove_active_widget():
        """Remove active widget froom the active area."""

class IModuleCanvasView(IView):
    """Module view, through which the canvas can render module,
    usually as an icon.
    """

class IAdjustenmentView(IWindowView):
    """Generic view to adjust modules' parameters and connection names"""

class IModulePanel(IPanelView):
    """View, that allows to adjust parameters of modules"""
    
