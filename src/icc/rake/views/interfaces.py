#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1504: * @file interfaces.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1505: ** interfaces declarations
#!/usr/bin/python

import zope.interface as ZI

#@+node:eugeneai.20110116171118.1516: ** Interfaces
#@+node:eugeneai.20110116171118.1506: *3* IView
class IView(ZI.Interface):
    model = ZI.Attribute("Project under exploration. The MVC Model.")
    ui = ZI.Attribute("User interface component holder.")

#@+node:eugeneai.20110116171118.1507: *3* IPanelView
class IPanelView(IView):
    """A View viewn as a panel (not a window)"""

#@+node:eugeneai.20110116171118.1508: *3* IWindowView
class IWindowView(IView):
    """A View viewn as a window"""

#@+node:eugeneai.20110116171118.1509: *3* IProjectView
class IProjectView(IPanelView):
    """View the a project. To make "New" action working applications
    shoud adapt this interface to their models.
    """

#@+node:eugeneai.20110116171118.1510: *3* ICanvasView
class ICanvasView(IProjectView):
    """We use drawing canvas as main project view
    """

#@+node:eugeneai.20110116171118.1511: *3* IApplication
class IApplication(IWindowView):
    #@+others
    #@+node:eugeneai.20110116171118.1512: *4* remove_active_widget
    def remove_active_widget():
        """Remove active widget froom the active area."""

    #@-others
#@+node:eugeneai.20110116171118.1513: *3* IModuleCanvasView
class IModuleCanvasView(IView):
    """Module view, through which the canvas can render module,
    usually as an icon.
    """

#@+node:eugeneai.20110116171118.1514: *3* IAdjustenmentView
class IAdjustenmentView(IWindowView):
    """Generic view to adjust modules' parameters and connection names"""

#@+node:eugeneai.20110116171118.1515: *3* IModulePanel
class IModulePanel(IPanelView):
    """View, that allows to adjust parameters of modules"""

#@-others
#@-leo
