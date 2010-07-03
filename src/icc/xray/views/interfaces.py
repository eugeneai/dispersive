#!/usr/bin/python
# encoding: utf-8

import zope.interface as ZI

class IView(ZI.Interface):
    model = ZI.Attribute("Project under exploration. The MVC Model.")
    ui = ZI.Attribute("User interface component holder.")

class IApplication(IView):
    def remove_active_widget():
        """Remove active widget froom the active area."""

class IFrame(IView):
    pass

class IPlottingFrame(IFrame):
    pass

