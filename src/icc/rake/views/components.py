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
M_PI=math.pi

class Ui:
    pass

class View(object):
    template = None
    widget_names = None
    ui_resource = __name__
    main_widget_name = 'main_frame'
    #implements(IView)
    ZC.adapts(mdli.IModel)
    def __init__(self, model = None):
        self.ui=Ui()
        if self.__class__.template != None:
            self.load_ui(self.__class__.template,
                         self.__class__.widget_names)
        self.set_model(model)
        self.signals = {}

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
        self.model=model
        # some update needed???

    def load_ui(self, template, widget_names = None):
        if template:
            builder=self.ui._builder = gtk.Builder()
            builder.add_from_string(resource_string(self.ui_resource, template))
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
    implements(ICanvas)
    
    template = "ui/canvas_view.glade"
    widget_names = ['canvas', 'main_frame']
    
    def __init__(self, model = None):
        self.p=Ui()
        self.p.x=0
        self.p.y=0
        View.__init__(self, model=model)
        self._init_pics()
        self.ui.main_frame.show_all()

    def _init_pics(self):
        self.svg=rsvg.Handle(data=resource_string(__name__, "ui/pics/test.svg"))
        self.background=rsvg.Handle(data=resource_string(__name__, "ui/pics/background.svg"))
        self.lm=rsvg.Handle(data=resource_string(__name__, "ui/pics/frame_open.svg"))

    def _component(self, canvas, x, y):
        canvas.set_line_width(1.0)
        m = canvas.get_matrix()
        canvas.translate(x, y)
        canvas.translate(-16,-16)

        self.background.render_cairo(canvas)
        self.lm.render_cairo(canvas)
        canvas.arc(-2, 16, 2, 0, M_PI*2)
        canvas.stroke()
        canvas.arc(34, 16, 2, 0, M_PI*2)
        canvas.stroke()

        canvas.set_matrix(m)

    def _connect(self, canvas, x1, y1, x2, y2):
        #x=25.6;  y=128.0
        #x1=102.4; y1=230.4
        #x2=153.6; y2=25.6
        #x3=230.4; y3=128.0
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
        canvas.set_source_rgba (0.5, 0, 0, 0.7);
        canvas.set_line_width (3.0)
        canvas.stroke()
        canvas.set_source(src)

    def on_canvas_button_press_event(self, canvas, ev, data=None):
        cr = canvas.window.cairo_create()
        self._connect(cr, self.p.x, self.p.y, ev.x, ev.y)
        self._component(cr, ev.x, ev.y)
        self.p.x=ev.x
        self.p.y=ev.y

    def on_canvas_button_release_event(self, canvas, ev, user=None):
        pass

    def on_canvas_expose_event(self, canvas, ev, data=None):
        cr = canvas.window.cairo_create()
        #cr.set_line_width(0.0)
        #cr.rectangle(0,0, 200,200)
        #cr.fill()
        dx=dy=60
        for x in xrange(5):
            for y in xrange(5):
                self._connect(cr, 0,0, x*dx, y*dy)
                self._component(cr, x*dx, y*dy)
        
