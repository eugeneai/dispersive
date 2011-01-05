#!/usr/bin/python

import zope.interface as ZI

class IView(ZI.Interface):
    model = ZI.Attribute("Project under exploration. The MVC Model.")
    ui = ZI.Attribute("User interface component holder.")

class IProjectView(IView):
    """View the a project. To make "New" action working applications
    shoud adapt this interface to their models.
    """

class ICanvas(IProjectView):
    """We use drawing canvas as main project view
    """

class IApplication(IView):
    def remove_active_widget():
        """Remove active widget froom the active area."""

