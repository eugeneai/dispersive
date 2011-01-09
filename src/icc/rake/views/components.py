#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk, sys

if __name__=="__main__":
    sys.path.append("..")

from icc.rake.views.interfaces import *
from zope.interface import implements, implementsOnly
import zope.component as ZC
import zope.component.interfaces as ZCI
from zope.component.factory import Factory
from pkg_resources import resource_stream, resource_string
    
import icc.rake.models.components as mdl
import icc.rake.models.interfaces as mdli
import icc.rake.interfaces as ri
import os

import cairo, math
import rsvg

M_2PI=math.pi*2.

class Ui:
    pass

class View(object):
    template = None
    widget_names = None
    resource = __name__
    main_widget_name = 'main_frame'
    #implements(IView)
    ZC.adapts(mdli.IModel)
    
    def __init__(self, model = None):
        self.ui=Ui()
        self.model=None
        self.parent_view=None
        if self.__class__.template != None:
            self.load_ui(self.__class__.template,
                         self.__class__.widget_names)
        self.set_model(model)
        self.init_resources()
        self.signals = {}

    def init_resources(self):
        pass

    def connect(self, signal, method, user_data=None):
        l = self.signals.setdefault(signal, [])
        l.append((method, user_data))

    def emit(self, signal, arg=None):
        d = self.signals.get(signal, [])
        for method, user_data in d:
            args = []
            if arg is not None:
                args.append(arg)
            if user_data is not None:
                args.append(user_data)
            method(self, *args)

    def set_model(self, model):
        if self.model != model:
            self.model=model
            # some update needed???

    def set_parent(self, view):
        """Set parent view. Used for some reason"""
        self.parent_view=view

    def load_ui(self, template, widget_names = None):
        if template:
            builder=self.ui._builder = gtk.Builder()
            builder.add_from_string(resource_string(self.resource, template))
            builder.connect_signals(self, builder)
            if widget_names:
                for name in widget_names:
                    widget = builder.get_object(name)
                    if widget is None:
                        raise ValueError("widget '%s' not found in  template '%s'" % (name, template))
                    setattr(self.ui, name, widget)

class Application(View):
    implements(IApplication)
    template = "ui/main_win_gtk.glade"
    widget_names = ['main_window', 'statusbar', 'toolbar',
             "main_vbox"]

    def __init__(self, model = None):
        View.__init__(self, model=model)
        self.ui.window=self.ui.main_window
        self.ui.window.show_all()
        self.active_view=None

        # Shoul be the last one, it seems
        if 0:
            self.default_view()
            self.open_project(self, LOAD_FILE)

    def set_model(self, model = None):
        # There shoul be event created to force model creation
        #if model is None:
        #    model = mdl.Project()
        return View.set_model(self, model)

    # Signal connection is linked in the glade XML file
    def main_window_delete_event_cb(self, widget, data1=None, data2=None):
        gtk.main_quit()
    m_quit_activate_cb=main_window_delete_event_cb

    def default_view(self):             
        self.insert_project_view(self.ui)

    def on_file_new(self, widget, data=None):
        # print "Created"
        # check wether data has been saved. YYY
        c=ZC.getUtility(ri.IConfiguration)
        factory_name=c.add_option('factory_name', default='main_model')
        self.set_model(ZC.createObject(factory_name.get()))
        self.insert_project_view(self.ui)

    def open_project(self, filename=None):
        if filename is None:
            filename = self.get_open_filename()
        if filename:
            self.model = mdl.Project(filename)
            self.default_action()

    def on_file_open(self, widget, data=None):
        return self.open_project()
            
    def get_open_filename(self):
        
        filename = None
        chooser = gtk.FileChooserDialog("Open Project...", self.ui.window,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        ffilter = gtk.FileFilter()
        for pattern, name in FILE_PATTERNS.iteritems():
            ffilter.add_pattern(pattern)

        chooser.set_filter(ffilter)
        #print gtk.FileChooserDialog.__doc__
        
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()
        # print "File:", filename
        return filename
    
    def error_message(self, message):
    
        # log to terminal window
        # print message
        
        # create an error message dialog and display modally to the user
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        
        dialog.run()
        dialog.destroy()

    def default_action(self):
        self.model.set_scale(mdl.Scale(zero=CALIBR_ZERO, scale=CALIBR_KEV))
        self.default_view()
        #self.spectra.r_plot()
        #print "AAA:", EPS_CMD
        #sp=spp.Popen([EPS_CMD, 'plot.eps'])
        #sp.communicate()

    def remove_active_view(self):
        if self.active_view is None:
            return
        main_widget = self.active_view.ui.main_frame
        self.ui.main_vbox.remove(main_widget)
        main_widget.destroy()
        self.active_wiew=None

    def insert_active_view(self, view):
        if self.active_view:
            self.remove_active_view()
        self.active_view = view
        main_widget_name = view.__class__.main_widget_name
        self.ui.main_vbox.pack_start(getattr(view.ui, main_widget_name), True, True)
        view.ui.main_frame.show_all()

    #def insert_plotting_area(self, ui):
    #    view = IPlottingView(self.model)
    #    self.insert_active_view(view)

    def insert_project_view(self, ui):
        view = IProjectView(self.model)
        self.insert_active_view(view)

    def main(self):
        return gtk.main()
    
    run = main

class Canvas(View):
    implements(ICanvasView)
    
    template = "ui/canvas_view.glade"
    widget_names = ['canvas', 'main_frame']
    
    def __init__(self, model = None):
        View.__init__(self, model=model)
        self.icon_cache={}
        self.state=Ui()
        self.selected_module=None
        self.modify_paint=False
        self.force_paint=True

    def get_position(self, module):
        return self.model.get_position(module)

    def init_resources(self):
        View.init_resources(self)
        self.module_icon_background = rsvg.Handle(
                data=resource_string(__name__,
                      "ui/pics/background.svg"))
        self.module_icon_selected = rsvg.Handle(
                data=resource_string(__name__,
                      "ui/pics/selected.svg"))

    def _module(self, canvas, module, selected=False):
        canvas.set_line_width(1.0)
        m = canvas.get_matrix()
        x, y = self.get_position(module)
        try:
            canvas.translate(x, y)
        except ValueError:
            canvas.translate(100, 100)
            
        canvas.translate(-16,-16)

        if selected:
            self.module_icon_selected.render_cairo(canvas)
        else:
            self.module_icon_background.render_cairo(canvas)
        if module:
            view=IModuleView(module)
            view.set_parent(self)
            view.render_on_canvas(canvas)
            canvas.set_source_rgb(0,0,0)
            if module.inputs:
                canvas.arc(-2, 16, 2, 0, M_2PI)
                canvas.stroke()
            if module.outputs:
                canvas.arc(34, 16, 2, 0, M_2PI)
                canvas.stroke()
            if module.controls:
                canvas.arc(16, 34, 2, 0, M_2PI)
                canvas.stroke()
            if module.implementors:
                canvas.arc(16, -2, 2, 0, M_2PI)
                canvas.stroke()

        canvas.set_matrix(m)

    def _connection(self, canvas, x1, y1, x2, y2, selected=False):
        dx=x2-x1
        dy=y2-y1
        dx,dy=dx/2.,dy/2.
        sx=16+2

        src = canvas.get_source()
        canvas.move_to (x1+sx, y1)
        canvas.curve_to (x1+sx+dx, y1,  x2-sx-dx, y2,  x2-sx, y2)
        canvas.set_source_rgba (1, 1, 1, 0.8);
        canvas.set_line_width (6.0)
        canvas.stroke()

        canvas.move_to (x1+sx, y1)
        canvas.curve_to (x1+sx+dx, y1,  x2-sx-dx, y2,  x2-sx, y2)
        if selected:
            canvas.set_source_rgba (0.0, 0.5, 0, 0.7)
        else:
            canvas.set_source_rgba (0.5, 0, 0, 0.7)
        canvas.set_line_width (3.0)
        canvas.stroke()
        canvas.set_source(src)

    def on_canvas_button_press_event(self, canvas, ev, data=None):
        self.selected_module = self.model.find_module(ev.x, ev.y)
        #(w, h) = canvas.window.get_size()
        self.modify_paint = self.selected_module != None
        if self.modify_paint:
            (px, py) = self.model.get_position(self.selected_module)
            self.mdx, self.mdy = px - ev.x, py - ev.y
        self.force_paint = True
        canvas.queue_draw()

    def on_canvas_button_release_event(self, canvas, ev, user=None):
        if self.selected_module:
            self.model.place(self.selected_module, ev.x+self.mdx, ev.y+self.mdy)
        self.selected_module=None
        self.modify_paint=False
        self.force_paint=True
        canvas.queue_draw()

    def on_canvas_motion_notify_event(self, canvas, ev, user=None):
        if self.selected_module:
            self.model.place(self.selected_module, ev.x+self.mdx, ev.y+self.mdy)
            canvas.queue_draw()

    def on_canvas_expose_event(self, canvas, ev, data=None):
        (w, h) = canvas.window.get_size()
        if not self.modify_paint:
            if self.model.changed:
                self.force_paint = True
        if self.force_paint:
            surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
            ccanvas = cairo.Context(surface)
            # fill canvas with bacground color
            src = ccanvas.get_source()
            ccanvas.rectangle(0,0, w,h)
            c=0.9
            ccanvas.set_source_rgb(c,c,c)
            ccanvas.fill()
            ccanvas.set_source(src)
            self.draw_model_on(ccanvas, self.selected_module)
            self.model.changed = False
            self.cache_surface = surface
            self.force_paint = False
        else:
            surface = self.cache_surface
        ocanvas = canvas.window.cairo_create()
        ocanvas.set_source_surface(surface)
        ocanvas.paint()
        if self.modify_paint:
            pass
            self.draw_model_on(ocanvas, exc_mod = self.selected_module, selected=True)

    def draw_model_on(self, canvas, exc_mod=None, selected=False):
        """Draw logics on the cairo canvas.
        Specially process exc_mod and its connections.
        The procedding of the exc_mod depends on selected.
        """
        for (mf, l) in self.model.forwards.iteritems():
            (x1, y1) = self.model.get_position(mf)
            emph = False
            if mf == exc_mod:
                if not selected:
                    continue
                else:
                    emph = True
            for mt in l:
                (x2, y2) = self.model.get_position(mt)
                if mt == exc_mod:
                    if not selected:
                        continue
                    else:
                        emph = True
                self._connection(canvas, x1, y1, x2, y2, selected=emph)
        for m in self.model.modules:
            if m == exc_mod:
                if selected:
                    self._module(canvas, m, selected = True)
            else:
                self._module(canvas, m)
                
            
class ModuleView(View):
    module_resource='icc.rake.modules.views'

    def set_model(self, model):
        if self.model != model:
            View.set_model(self, model)
            self.init_resources()

    def set_parent(self, parent):
        View.set_parent(self, parent)
        self.init_resources()

    def init_resources(self):
        View.init_resources(self)
        self.icon = None
        if self.parent_view:
            if self.model != None and self.model.__class__.icon:
                self.icon = self.parent_view.icon_cache.get(self.model.__class__, None)
                if self.icon == None:
                    self.icon = rsvg.Handle(
                        data=resource_string(self.__class__.module_resource,
                             self.model.__class__.icon))
                    self.parent_view.icon_cache[self.model.__class__]=self.icon
            
    def render_on_canvas(self, canvas):
        """Render myself on a cairo canvas"""
        if self.icon:
            self.icon.render_cairo(canvas)

    
