#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1453: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1454: ** components declarations
#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk, sys
import goocanvas, gobject

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
import icc.rake.modules.interfaces as module_is
from icc.rake.views import *
import os, os.path

import cairo, math
import rsvg

import types

M_2PI=math.pi*2.

def sign(x):
    if x>0: return 1
    elif x<0: return -1
    return 0

#@+node:eugeneai.20110116171118.1455: ** class Ui
class Ui(object):
    pass

class RetVal(Ui):
    def __init__(self, value=None):
        self.value=None
    pass

#@+node:eugeneai.20110116171118.1456: ** InputDialog
def InputDialog(message, value='', field='Name:', secondary=''):
    "Obtained and adopted from http://ardoris.wordpress.com/2008/07/05/pygtk-text-entry-dialog/"
    def responseToDialog(entry, dialog, response):
        dialog.response(response)
    def getText(value):
        #base this on a message dialog
        dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK,
            None)
        dialog.set_markup(message)
        #create the text input field
        entry = gtk.Entry()
        #allow the user to press enter to do ok
        entry.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)
        #create a horizontal box to pack the entry and a label
        entry.set_text(value)
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label(field), False, 5, 5)
        hbox.pack_end(entry)
        #some secondary text
        dialog.format_secondary_markup(secondary)
        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        #go go go
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            value = entry.get_text()
        dialog.destroy()
        return value
    return getText(value)

#@+node:eugeneai.20110116171118.1457: ** ConfirmationDialog
def ConfirmationDialog(message, secondary=''):
    dialog = gtk.MessageDialog(
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_YES_NO,
            None)
    dialog.set_markup(message)
    dialog.format_secondary_markup(secondary)
    rc = dialog.run() == gtk.RESPONSE_YES
    dialog.destroy()
    return rc

#@+node:eugeneai.20110116171118.1458: ** class View
class View(gtk.Object):
    __gsignals__ = {
        'get-widget': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_BOOLEAN,
                       (gobject.TYPE_STRING, gobject.TYPE_PYOBJECT,)),
        'destroy-view': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                       (gobject.TYPE_PYOBJECT,)),
    }
    template = None
    widget_names = None
    resource = __name__
    main_widget_name = 'main_frame'
    #implements(IView)
    ZC.adapts(mdli.IModel, IView)

    #@+others
    #@+node:eugeneai.20110116171118.1459: *3* __init__
    def __init__(self, model = None, parent=None):
        gtk.Object.__init__(self)
        self.ui=Ui()
        self.model=None
        self.set_parent(parent)
        self.model_state=Ui()
        # model_state stores metadata about model.
        self.set_model_unmodified() # Is the model modified and to be saved on closing.
        if self.__class__.template != None:
            self.load_ui(self.__class__.template,
                         self.__class__.widget_names)
        self.set_model(model)
        self.init_resources()
        self.signals = {}
        self.connect("get-widget", self.on_get_widget)
        self.connect("destroy-view", self.do_destroy_view)

    #@+node:eugeneai.20110116171118.1460: *3* init_resources
    def init_resources(self):
        pass

    #@+node:eugeneai.20110116171118.1461: *3* connect
#    def connect(self, signal, method, user_data=None):
#        l = self.signals.setdefault(signal, [])
#        l.append((method, user_data))

    #@+node:eugeneai.20110116171118.1462: *3* emit
#    def emit(self, signal, arg=None):
#        d = self.signals.get(signal, [])
#        for method, user_data in d:
#            args = []
#            if arg is not None:
#                args.append(arg)
#            if user_data is not None:
#                args.append(user_data)
#            method(self, *args)

    #@+node:eugeneai.20110116171118.1463: *3* set_model
    def set_model(self, model):
        if self.model != model:
            self.model=model
            # some update needed???

    #@+node:eugeneai.20110116171118.1464: *3* set_parent
    def set_parent(self, view):
        """Set parent view. Used for some reason"""
        try:
            if self.parent_view:
                pass
                #disconnect
        except AttributeError:
            pass

        if IView.providedBy(view):
            self.parent_view=view
            view.connect('destroy-view', self.on_parent_destroy)

    def is_model_modified(self):
        return self.model_state.modified

    def set_model_modified(self):
        self.model_state.modified=True
        return self.is_model_modified()

    def set_model_unmodified(self):
        self.model_state.modified=False
        return self.is_model_modified()

    #@+node:eugeneai.20110116171118.1465: *3* load_ui
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
                    else:
                        widget.set_name(name)

                    setattr(self.ui, name, widget)

    def on_get_widget(self, widget, widget_name, ret_val):
        """ Responds on subwidget signal emission like
        rv=RetVal()
        self.emit('get-widget', 'main_window', rv)
        print rv.value
        """
        print "Locate:", widget, widget_name, self
        if widget_name in self.ui.__dict__:
            w = self.ui.get(widget_name)
            ret_val.value = w
            return 1 # Stop event
        else:
            return 0

    def do_destroy_view(self, self_widget, data=None):
        pass

    def locate_widget(self, widget_name):
        ui = self.ui
        try:
            return getattr(ui,widget_name)
        except AttributeError:
            pass
        if self.parent_view != None:
            return self.parent_view.locate_widget(widget_name)

        #rv=RetVal()
        #self.emit('get-widget', widget_name, rv)
        #return rv.value

    def destroy(self):
        self.emit('destroy-view', self)
        self.get_main_frame().destroy()
        self.ui=None
        gtk.Object.destroy(self)

    def remove_from(self, box):
        box.remove(self.get_main_frame())

    def insert_into(self, box):
        box.pack_start(self.get_main_frame(), True, True)

    def get_main_frame(self):
        main_widget_name = self.__class__.main_widget_name
        return getattr(self.ui, main_widget_name)

    def on_parent_destroy(self, parent, data=None):
        self.destroy()

    def add_actions_to_menu(self, a_group, label=None, before=None):
        if label == None:
            label = a_group.get_name()

        # find the position of 'before'

        mb = self.locate_widget('menubar')
        if mb == None:
            return

        mi = gtk.MenuItem(label=label)
        mi_name=a_group.get_name()+"_menu"
        mi.set_name(mi_name)

        #Create menu
        m=gtk.Menu()
        mi.set_submenu(m)
        for a in a_group.list_actions():
            m.append(a.create_menu_item())

        setattr(self.ui, mi_name, mi)

        children = mb.get_children()
        l = len(children)
        if before == None:
            mb.insert(mi, l-1)
        else:
            for ch, num in enumerate(children):
                if ch == before:
                    mb.insert(mi, num)
                    break
            else:
                mi.destroy()
                delattr(self.ui, mi_name)
                return
        mi.show()
        return mi

    def del_actions_from_menu(self, a_group):
        mb = self.locate_widget('menubar')
        mi_name=a_group.get_name()+"_menu"
        try:
            mi = getattr(self.ui, mi_name)
            delattr(self.ui, mi_name)
        except AttributeError:
            return
        mi.hide()
        mb.remove(mi)

    def add_actions_to_toolbar(self, a_group, separator=True, important=True):
        """Adds actions of the action group a_group to toolbar.
        If separator is True, a SeparatorToolItem wisget also added before the tool buttons.
        If important is True, then noimportand actions will not be added to the toolbar."""

        tb = self.locate_widget('toolbar')
        if tb == None:
            return

        acs = a_group.list_actions()
        if len(acs) == 0:
            return

        widgets = []

        if separator:
            separator = gtk.SeparatorToolItem()
            tb.insert(separator, -1)
            widgets.append(separator)
            separator.show()

        for a in a_group.list_actions():
            if not important or a.get_is_important():
                ti = a.create_tool_item()
                tb.insert(ti, -1)
                widgets.append(ti)
                ti.show()
            else:
                print a, 'did not created', a.get_is_important()

        return widgets

    def del_actions_from_toolbar(self, a_group, widgets):
        tb = self.locate_widget('toolbar')
        if tb == None:
            return

        for w in widgets:
            w.hide()
            tb.remove(w)

        return []



gobject.type_register(View)

    #@-others
#@+node:eugeneai.20110116171118.1466: ** class Application
class Application(View):
    __gsignals__ = {
        'startup-open': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    }
    implements(IApplication)
    template = "ui/main_win_gtk.glade"
    widget_names = ['main_window', 'statusbar', 'toolbar', 'menubar',
             "main_vbox", 'ac_close', 'ac_save',
                    "menu_file", "menu_edit", "menu_view", "menu_help"]

    #@+others
    #@+node:eugeneai.20110116171118.1467: *3* __init__
    def __init__(self, model = None, parent=None):
        View.__init__(self, model=model, parent=parent)
        self.ui.window=self.ui.main_window
        self.ui.window.show_all()

        self.active_view=None
        self.remove_active_view()

        self.filename=None

        _conf=get_global_configuration()
        opt=_conf.add_option('project_file_ext', default='.prj:A project file', keys='app')
        self.FILE_PATTERNS=[e.split(':') for e in opt.get().split(';')]

        self.connect("startup_open", self.on_startup_open)

                #put event to load project.
                #self.open_project(lo_f)

    #@+node:eugeneai.20110116171118.1468: *3* set_model
    def set_model(self, model = None):
        # There should be event created to force model creation
        #if model is None:
        #    model = mdl.Project()
        return View.set_model(self, model)

    #@+node:eugeneai.20110116171118.1469: *3* main_window_delete_event_cb
    # Signal connection is linked in the glade XML file
    def main_window_delete_event_cb(self, widget, data1=None, data2=None):
        gtk.main_quit()
    #@+node:eugeneai.20110116171118.1470: *3* default_view
    m_quit_activate_cb=main_window_delete_event_cb

    def default_view(self):
        self.insert_project_view(self.ui)

    #@+node:eugeneai.20110116171118.1471: *3* on_file_new
    def on_file_new(self, widget=None, data=None):
        # print "Created"
        # check wether data has been saved. YYY
        c=get_global_configuration()
        factory_name=c.add_option('factory_name', default='main_model')
        self.set_model(ZC.createObject(factory_name.get()))
        self.insert_project_view(self.ui)

    #@+node:eugeneai.20110116171118.1472: *3* open_project
    def open_project(self, filename=None):
        if filename is None:
            filename_ = self.get_filename()
        else:
            filename_=self.normalize_file_ext(filename)
        if filename_:
            self.on_file_new()
            #self.model.load_from(filename_)
            #self.active_view.update()
            if filename == None: # Loaded as result of user file dialog activity
                set_user_config_option('last_project_file_name', filename_, type='string', keys='startup')
            self.filename=filename_
        else:
            self.filename=None

    #@+node:eugeneai.20110116171118.1473: *3* on_file_open
    def on_file_open(self, widget, data=None):
        return self.open_project()

    def on_startup_open(self, widget, filename):
        return self.open_project(filename)

    def on_file_close(self, widget, data=None):
        if self.active_view:
            active_view=self.active_view
            if active_view.is_model_modified():
                # ask user to save project
                pass
        self.remove_active_view()


    def on_file_save(self, widget, data=None):
        if self.filename:
            filename_=self.filename
        else:
            filename_=None
        if not filename_:
            filename_=self.get_filename(save=True)

        if not filename_:
            return # user rejected to write data

        print "Saving the data of the project to file '%s'" % filename_
        self.filename=filename_


    #@+node:eugeneai.20110116171118.1474: *3* get_filename
    def get_filename(self, save=False):
        if save:
            msg="Save the project..."
            ac = gtk.FILE_CHOOSER_ACTION_SAVE
            icon = gtk.STOCK_SAVE
        else:
            msg="Open a project..."
            ac = gtk.FILE_CHOOSER_ACTION_OPEN
            icon = gtk.STOCK_OPEN

        filename = None
        chooser = gtk.FileChooserDialog(msg, self.ui.window,
                                        ac,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         icon, gtk.RESPONSE_OK))


        ffilter = gtk.FileFilter()
        for pattern, name in self.FILE_PATTERNS:
            ffilter.add_pattern("*"+pattern)

        chooser.set_filter(ffilter)
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()

        return self.normalize_file_ext(filename)

    def normalize_file_ext(self, filename):

        def_file_ext=self.FILE_PATTERNS[0][0]

        (_,ext) = os.path.splitext(filename)
        if not ext:
            filename+=def_file_ext
        return filename

    #@+node:eugeneai.20110116171118.1475: *3* error_message
    def error_message(self, message):

        # log to terminal window
        # print message

        # create an error message dialog and display modally to the user
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)

        dialog.run()
        dialog.destroy()

    #@+node:eugeneai.20110116171118.1476: *3* default_action
    def default_action(self):
        self.model.set_scale(mdl.Scale(zero=CALIBR_ZERO, scale=CALIBR_KEV))
        self.default_view()
        #self.spectra.r_plot()
        #print "AAA:", EPS_CMD
        #sp=spp.Popen([EPS_CMD, 'plot.eps'])
        #sp.communicate()

    #@+node:eugeneai.20110116171118.1477: *3* remove_active_view
    def remove_active_view(self):
        if self.active_view != None:
            av = self.active_view
            av.remove_from(self.ui.main_vbox)
            av.destroy()
            self.active_view=None
        for ac in [self.ui.ac_save, self.ui.ac_close]:
            ac.set_sensitive(False)

    #@+node:eugeneai.20110116171118.1478: *3* insert_active_view
    def insert_active_view(self, view):
        self.remove_active_view()

        self.active_view = view
        self.active_view.insert_into(self.ui.main_vbox)
        self.ui.ac_close.set_sensitive(True)
        view.ui.main_frame.show_all()

    #@+node:eugeneai.20110116171118.1479: *3* insert_project_view
    #def insert_plotting_area(self, ui):
    #    view = IPlottingView(self.model)
    #    self.insert_active_view(view)

    def insert_project_view(self, ui):
        view = ZC.getMultiAdapter((self.model, self), IProjectView)
        self.insert_active_view(view)

    #@+node:eugeneai.20110116171118.1480: *3* main
    def main(self):
        return gtk.main()

    #@-others
    run = main

gobject.type_register(Application)

#@+node:eugeneai.20110117171340.1635: ** Pictogramm machinery
#@+node:eugeneai.20110123122541.1648: *3* class SVGImage
class SVGImage(goocanvas.Image):
    """SVGImage, that can be rendered from SVG.
    """
    #@+others
    #@+node:eugeneai.20110123122541.1649: *4* __init__
    def __init__(self, svg, **kwargs):
        self.svg=svg
        self.kwargs=kwargs
        #pattern = self.render_pattern(**kwargs)
        d={}
        d.update(kwargs)
        #d['pattern']=pattern
        self.kwargs=d
        #print "P:", pattern

        goocanvas.Image.__init__(self, **d)
        pattern = self.render_pattern(**kwargs)
        self.set_property("pattern", pattern)

    #@+node:eugeneai.20110123122541.1650: *4* render_pattern
    def render_pattern(self, **kwargs):
        def convert_rsvg(resource):
            if type(resource) in [types.StringType, types.UnicodeType]:
                icon_registry=ZC.getUtility(IIconRegistry, 'svg')
                return icon_registry.resource(resource)
            return resource

        width, height = self.kwargs['width'], self.kwargs['height']
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        canvas = cairo.Context(surface)
        canvas.set_antialias(cairo.ANTIALIAS_NONE)
        canvas.set_source_rgb(0,1,0)
        canvas.set_line_width(4.0)
        if self.svg == None:
            canvas.rectangle(0,0, width,height)
            canvas.stroke()
        else:
            if type(self.svg) in (types.TupleType, types.ListType):
                self.svg = map(convert_rsvg, self.svg)
                for svg in self.svg:
                    svg.render_cairo(canvas)
            else:
                self.svg=convert_rsvg(self.svg)
                svg.render_cairo(canvas)

        return cairo.SurfacePattern(surface)

    #@-others
#@+node:eugeneai.20110117171340.1634: *3* class PicItem
class PicItem(goocanvas.ItemSimple, goocanvas.Item):
    #@+others
    #@+node:eugeneai.20110117171340.1637: *4* __init__
    def __init__(self, module, graph, **kwargs):
        """Icon driwer for module, using main graph canvas view `graph`
        """
        super(PicItem, self).__init__(**kwargs)
        self.graph=graph
        self.module = module
        x,y = self.graph.get_position(module)
        self.x=x-16
        self.y=y-16
        self.width=32
        self.height=32
        #self.bounds = goocanvas.Bounds()


    #@+node:eugeneai.20110117171340.1642: *4* _do_update
    def _do_update(self, entire_tree, cr):
        x, y = self.graph.get_position(self.module)
        self.bounds.x1 = x - 16.
        self.bounds.y1 = y - 16.
        self.bounds.x2 = x + 16.
        self.bounds.y2 = y + 16.
        return self.bounds

    #@+node:eugeneai.20110117171340.1645: *4* _do_paint
    def _do_paint(self, canvas, bounds, scale):
        #print bounds.x1, bounds.y1, bounds.x2, bounds.y2
        #return
        canvas.set_line_width(1.0)
        m = canvas.get_matrix()

        module = self.module

        x, y = self.graph.get_position(module)

        canvas.translate(x,y)
        canvas.translate(-16,-16)

        selected = False

        if selected:
            self.graph.module_icon_toolboxed.render_cairo(canvas)
        else:
            self.graph.module_icon_background.render_cairo(canvas)
        if module:
            view=IModuleCanvasView(module)
            view.set_parent(self.graph)
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

    #@+node:eugeneai.20110122224638.1646: *4* do_simple_create_path
    def do_simple_create_path(self, canvas):
        #print bounds.x1, bounds.y1, bounds.x2, bounds.y2
        #return
        canvas.set_line_width(1.0)
        m = canvas.get_matrix()

        module = self.module
        print "Paint", module

        x, y = self.graph.get_position(module)

        canvas.translate(x,y)
        canvas.translate(-16,-16)

        #canvas.rectangle(0,0,32,32)
        #canvas.stroke()


        selected = False

        if selected:
            self.graph.module_icon_toolboxed.render_cairo(canvas)
        else:
            self.graph.module_icon_background.render_cairo(canvas)
        if module:
            view=IModuleCanvasView(module)
            view.set_parent(self.graph)
            #view.render_on_canvas(canvas)
            #we will draw text ourselves
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

    #@+node:eugeneai.20110117171340.1644: *4* _do_get_bounds
    def _do_get_bounds(self):
        print "!"
        return self.bounds
    #@-others
#@+node:eugeneai.20110117171340.1636: *3* register PicItem in gobject
gobject.type_register(PicItem)
#@+node:eugeneai.20110116171118.1481: ** class Canvas
TBL_ACTIONS=[
    ( 1,-1, "remove", 'ui/pics/close.svg', True),
    (-1, 1, "rename", 'ui/pics/name.svg', True),
    ( 1, 1, "info", 'ui/pics/info.svg', True),
    (-1,-1, "edit", 'ui/pics/edit.svg', True),

    ( 1, 0, "right", 'ui/pics/right.svg', 'outputs'),
    (-1, 0, "left", 'ui/pics/right.svg', 'inputs'),
    ( 0,-1, "up", 'ui/pics/down.svg', False),
    ( 0, 1, "down", 'ui/pics/down.svg', False),
    ]

class Canvas(View):
    implements(ICanvasView)
    ZC.adapts(mdli.ICanvas, IView)

    template = "ui/canvas_view.glade"
    widget_names = ['vbox', 'main_frame']

    #@+others
    #@+node:eugeneai.20110116171118.1482: *3* __init__
    def __init__(self, model = None, app=None, parent=None):
        View.__init__(self, model=None, parent=parent)
        self.state=Ui()
        self.selected_module=None # module and its
        self.selected_item = None # corresponding icon
        self.selected_tool = None # and icon's tool icon
        self.module_movement=False
        self.tmp_toolbox = [] # Temporary local toolbox group
        self.paths=[]

        self.active_group = None  # active icon group, where mouse entered.
        self.active_area = None   # active area in the icon group, where mouse entered.
        self.area_conn_ids = None

        self.new_connection = None # Widget used to track new connction creation
        self.connect_to=None # used during tracking new connection to track possible modules to connect to

        self.ui.canvas=canvas=goocanvas.Canvas()
        canvas.set_size_request(1024,768)
        canvas.set_bounds(0,0, 2000, 2000)
        canvas.connect_after('motion-notify-event', self.on_canvas_motion)
        root=canvas.get_root_item()
        root.connect('motion-notify-event', self.on_root_motion)
        root.connect('button-release-event', self.on_root_press_release)

        #root.connect('enter-notify-event', self.on_root_enter_leave)
        #root.connect('leave-notify-event', self.on_root_enter_leave)

        self.ui.vbox.add(canvas)
        self.set_model(model)

    #@+node:eugeneai.20110116171118.1483: *3* get_position
    def get_position(self, module):
        return self.model.get_position(module)

    #@+node:eugeneai.20110117171340.1641: *3* set_model
    def set_model(self, model):
        View.set_model(self, model)
        if model == None:
            return
        root = self.ui.canvas.get_root_item()
        self.paths=[]

        for mf, l in self.model.forwards.iteritems():
            for mt in l:
                b,f = self.create_connection(mf, mt, state=None)



        for m in self.model.modules:
            self.create_module(m)


    #@+node:eugeneai.20110116171118.1484: *3* init_resources
    def init_resources(self):
        View.init_resources(self)
        icon_registry=ZC.getUtility(IIconRegistry, name='svg')
        self.module_icon_background = icon_registry.resource("ui/pics/background.svg")
        self.module_icon_selected = icon_registry.resource("ui/pics/selected.svg")
        self.module_icon_toolboxed = icon_registry.resource("ui/pics/toolboxed.svg")
        self.toolbox_background = self.module_icon_toolboxed = icon_registry.resource("ui/pics/tool-bkg.svg")

    #@+node:eugeneai.20110116171118.1485: *3* _module
    def _module(self, module, selected=False):
        h=w=44

        pattern=self.draw_module_pattern(module, bheight=h, bwidth=w, fheight=32, fwidth=32, selected=selected)

        img = goocanvas.Image(x=-w/2., y=-h/2., width=w, height=h, pattern=pattern)
        text = goocanvas.Text(text=module.name, x=0, y=22, anchor=gtk.ANCHOR_NORTH, fill_color="black", font='Sans 8', ) # XXX change name to title and edit both
        img.text = text

        return img, text

    #@+node:eugeneai.20110123122541.1644: *3* draw_module_pattern
    def draw_module_pattern(self, module, bheight=44, bwidth=44, fheight=32, fwidth=32, selected=False):
        h,w=bheight,bwidth

        sx,sy=(bwidth-fwidth)/2., (bheight-fheight)/2.

        surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,h,w)
        canvas=cairo.Context(surface)
        canvas.set_line_width(1.0)

        canvas.translate(sx,sy)

        if selected:
            #self.module_icon_toolboxed.render_cairo(canvas)
            self.module_icon_selected.render_cairo(canvas)
        else:
            self.module_icon_background.render_cairo(canvas)
        if module:
            view=IModuleCanvasView(module)
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
        return cairo.SurfacePattern(surface)
    #@+node:eugeneai.20110116171118.1486: *3* _connection
    def _connection(self, x1, y1, x2, y2, selected=False, absolute = (False, False)):

        data=self.draw_curve(x1,y1, x2,y2, absolute)

        bkg_path = goocanvas.Path(data=data, line_width=6.0, stroke_color='white')

        frg_path = goocanvas.Path(data=data, line_width=4.0, stroke_color='brown')

        frg_path.bkg_path=bkg_path

        return (bkg_path, frg_path)


    #@+node:eugeneai.20110123122541.1647: *3* draw_curve
    def draw_curve(self, x1, y1, x2, y2, absolute = (False, False)):
        dx=x2-x1
        dy=y2-y1
        sc=100
        dx=sc # sc*sign(dx)
        dy=sc*sign(dy)
        _dsx=16+2
        sx1=sx2=0.0
        if not absolute[0]:
            sx1=_dsx
        if not absolute[1]:
            sx2=_dsx
        return 'M%s,%s C%s,%s %s,%s %s,%s' % (x1+sx1, y1,  x1+sx1+dx, y1,  x2-sx2-dx, y2,  x2-sx2, y2)

    #@+node:eugeneai.20110123122541.1670: *3* on_canvas_motion
    def on_canvas_motion(self, canvas, event):
        if not self.module_movement and not self.new_connection and self.active_group and not self.active_area:
            # disconnecting events from area, which will be not active anymore
            for i in self.area_conn_ids:
                self.active_group.disconnect(i)

            self.active_group=None
            self.remove_selection()

    #@+node:eugeneai.20110117171340.1633: *3* on_text_enter_notify_event
    def on_text_enter_notify_event(self, item, target, event):
        #print "Enter", item, target, event
        item.rotate(10, 300, 300)
        #pass
    #@+node:eugeneai.20110117171340.1646: *3* on_module_enter_leave
    def on_module_enter_leave(self, item, target, event):
        # print "Module:", event.type
        if event.type==gtk.gdk.ENTER_NOTIFY:
            if not self.selected_module and not self.tmp_toolbox:
                module=self.selected_module = item.module
                self.selected_item=item
                self.tmp_toolbox_group = item.get_parent()
                group=self.active_group = item.get_parent()
                id1 = group.connect('leave-notify-event', self.on_module_group_enter_leave)
                id2 = group.connect('enter-notify-event', self.on_module_group_enter_leave)
                self.area_conn_ids = (id1, id2)

                """
                _it=self.tmp_toolbox_group
                for pspec in _it.props:
                    pname=pspec.name
                    print dir(pspec)
                    print pname
                    if not pname in ['transform', 'stroke-pattern', 'fill-pattern', 'stroke-color', 'stroke-pixbuf',]:
                        _it.get_property(pspec.name)
                """


                self.tmp_toolbox=[]
                for (dx, dy, name, ui, cond) in TBL_ACTIONS:
                    if type(cond) == types.StringType:
                        if hasattr(module,cond):
                            cond=getattr(module, cond)
                        else:
                            cond=False
                    if cond:
                        px, py = 20*dx-7, 20*dy-7 # XXX monkey patch.
                        tool=SVGImage([self.toolbox_background, ui], height=12, width=12, x=px, y=py)
                        tool.item=item # Whose tool it is.
                        tool.name=name
                        self.tmp_toolbox_group.add_child(tool, -1)
                        self.tmp_toolbox.append(tool)
                        tool.connect('button-press-event', self.on_tool_pressed_released)
                        tool.connect('button-release-event', self.on_tool_pressed_released)

                item.set_property('pattern', self.draw_module_pattern(item.module, selected = self.selected_module))
                item.get_parent().raise_(None)
                self.tmp_toolbox_group.raise_(None)
    #@+node:eugeneai.20110123122541.1658: *3* on_module_press_release
    def on_module_press_release(self, item, target, event):
        if event.type==gtk.gdk.BUTTON_PRESS:
            self.module_movement=True
            self.smx=event.x_root
            self.smy=event.y_root
            x,y = self.get_position(item.module)

            # shift from the center of the image
            self.dx=self.smx - x
            self.dy=self.smy - y


            self.paths_from=[p for p in self.paths if p.mfrom==item.module]
            self.paths_to  =[p for p in self.paths if p.mto  ==item.module]
            for p in self.paths_from+self.paths_to:
                p.bkg_path.raise_(None)
                p.raise_(None)
                self.set_curve_state(p, "on_move")

            item.raise_(None)
            item.get_parent().raise_(None)
        elif event.type==gtk.gdk.BUTTON_RELEASE:
            x,y = self.get_position(item.module)
            mx,my=event.x_root, event.y_root
            dx=mx-self.smx
            dy=my-self.smy
            x=mx-self.dx
            y=my-self.dy
            self.model.place(item.module, x,y)
            self.module_movement=False
            self.smx=None
            self.smy=None
            item.lower(None)
            for p in self.paths_from+self.paths_to:
                self.set_curve_state(p, None)
            self.paths_from = []
            self.paths_to   = []

    #@+node:eugeneai.20110123122541.1659: *3* on_module_motion
    def on_module_motion(self, item, target, event):
        #print dir(event)
        pass
    #@+node:eugeneai.20110123122541.1662: *3* on_module_text_clicked
    def on_module_text_clicked(self, item, target, event):
        if event.type == gtk.gdk.BUTTON_RELEASE:
            self.set_module_name(self.selected_item)

    #@+node:eugeneai.20110117171340.1649: *3* on_curve_enter_leave
    def on_curve_enter_leave(self, item, target, event, fore_path):
        #print "Enter:", item, target, event
        if self.new_connection:
            return
        state=None
        if event.type==gtk.gdk.ENTER_NOTIFY:
            state='selected'
        self.set_curve_state(fore_path, state)

    def on_curve_press_release(self, item, target, event, fore_path):
        #print "Enter:", item, target, event
        if self.new_connection:
            return
        state=None
        if event.type==gtk.gdk.BUTTON_RELEASE:
            state='selected'
            self.set_curve_state(fore_path, state)
            d=InputDialog("test")
            state=None
            self.set_curve_state(fore_path, state)


    #@+node:eugeneai.20110123122541.1663: *3* on_tool_pressed_released
    def on_tool_pressed_released(self, item, target, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button==1:
                item.button_pressed=True
            if item.name=="right":
                root = self.ui.canvas.get_root_item()
                (x, y) = self.get_position(self.selected_module)
                b, self.new_connection = self._connection(x,y, event.x_root,event.y_root, absolute=(False, True))
                root.add_child(b, -1)
                root.add_child(self.new_connection)
                self.set_curve_state(self.new_connection,'on_move')


        elif event.type == gtk.gdk.BUTTON_RELEASE:
            try:
                item.button_pressed
            except AttributeError:
                return
            if item.button_pressed:
                self.on_tool_clicked(item, target, event=event)
                del item.button_pressed


    #@+node:eugeneai.20110124104607.1655: *3* on_tool_clicked
    def on_tool_clicked(self, item, target, event):
        mitem=item.item # Module item
        m=mitem.module
        if item.name=='remove':
            self.remove_selection()
            rem=[]
            for p in self.paths:
                if m in [p.mfrom, p.mto]:
                    p.bkg_path.remove()
                    p.remove()
                    rem.append(p)
            for p in rem:
                self.paths.remove(p)
            mitem.get_parent().remove()
        elif item.name=="rename":
            self.set_module_name(self.selected_item)
        elif item.name=="edit":
            #editor=None
            view=IAdjustenmentView(self.selected_module)
            view.set_parent(self)
    #@+node:eugeneai.20110123122541.1664: *3* on_tool_enter_leave
    def on_tool_enter_leave(self, item, target, event):
        if event.type == gtk.gdk.ENTER_NOTIFY:
            self.selected_tool = item
        elif event.type == gtk.gdk.LEAVE_NOTIFY:
            self.selected_tool = None
        #print "Tool:", event.type, self.selected_tool
        pass
    #@+node:eugeneai.20110123122541.1665: *3* on_root_enter_leave
    def on_root_enter_leave(self, item, target, event):
        #print "Root", event, "Item:", self.selected_item, "Tool:", self.selected_tool
        if self.selected_item and self.tmp_toolbox and not self.selected_tool:
            if self.tmp_toolbox!=None:
                self.tmp_toolbox_group.remove()
                self.tmp_toolbox = []

            self.remove_selection()
        else:
            pass


    #@+node:eugeneai.20110215120545.1660: *3* on_root_press_release
    def on_root_press_release(self, item, target, event):
        if self.new_connection:
            self.new_connection.bkg_path.remove()
            self.new_connection.remove()
            self.new_connection=None # release the tracking process
            mt=None
            if self.connect_to:
                mt=self.connect_to.module
                self.connect_to.set_property('pattern', self.draw_module_pattern(mt, selected = False))

                self.connect_to=None

            else:
                # There shoul be a dialog for module choice.
                m_name = self.choose_module(event, 'inputs')
                if m_name:
                    mt=self.create_module(m_name, event.x_root, event.y_root)
                else:
                    mt=None
            if mt:
                self.create_connection(self.selected_module, mt)
                self.model.connect(self.selected_module, mt)
            self.selected_item.get_parent().raise_(None)
            self.remove_selection()
        elif not self.selected_module:
            m_name = self.choose_module(event, 'outputs')
            if m_name:
                mt=self.create_module(m_name, event.x_root, event.y_root)
            else:
                mt=None


    def choose_module(self, event, kind):
        name=ModuleChooseDialog(message='Choose a module',
                                filter=lambda x: getattr(x, kind))
        return name

    #@+node:eugeneai.20110213211825.1656: *3* on_root_motion
    def on_root_motion(self, group, target, event):
        if self.selected_module:
            item=self.selected_item
            module=self.selected_module
            x,y = self.get_position(module)
            mx,my=event.x_root, event.y_root
            parent = item.get_parent()
            root=self.ui.canvas.get_root_item()

        if self.module_movement:
            dx=mx-self.smx
            dy=my-self.smy
            x=mx-self.dx
            y=my-self.dy
            self.smx=mx
            self.smy=my
            self.model.place(module, x, y)
            item.get_parent().translate(dx, dy)

            for p in self.paths_from:
                m = p.mto
                x2,y2 = self.get_position(m)
                curve = self.draw_curve(x,y, x2,y2)
                p.set_property('data', curve)
                p.bkg_path.set_property('data', curve)

            for p in self.paths_to:
                m = p.mfrom
                x2,y2 = self.get_position(m)
                curve = self.draw_curve(x2,y2, x,y)
                p.set_property('data', curve)
                p.bkg_path.set_property('data', curve)

        if self.new_connection:
            p=self.new_connection

            # This is workaround, as enter and leave events do not work while a button pressed.
            i=None
            its=self.ui.canvas.get_items_at(mx, my, is_pointer_event=False)

            if its:
                for _i in its:
                    if _i == self.selected_item:
                        continue
                    if _i.__class__!=goocanvas.Image:
                        continue
                    if hasattr(_i,'module') and _i.module.inputs:
                        i=_i
                        break

            if i:
                self.connect_to=i
                i.set_property('pattern', self.draw_module_pattern(item.module, selected = True))
                mx,my = self.get_position(i.module)
            else:
                if self.connect_to:
                    self.connect_to.set_property('pattern', self.draw_module_pattern(item.module, selected = False))
                    self.connect_to=None
            # end of the workaround

            curve = self.draw_curve(x,y, mx, my, absolute=(False, i == None))
            p.set_property('data', curve)
            p.bkg_path.set_property('data', curve)

    #@+node:eugeneai.20110123122541.1669: *3* on_module_group_enter_leave
    def on_module_group_enter_leave(self, item, target, event):
        if event.type == gtk.gdk.ENTER_NOTIFY:
            self.active_area = target
        elif event.type == gtk.gdk.LEAVE_NOTIFY:
            self.active_area = None
        self.active_group = item
    #@+node:eugeneai.20110116171118.1491: *3* leaved_selection
    def leaved_selection(self, module, x, y):
        return not self.is_spotted(module, x,y, 26)

    #@+node:eugeneai.20110116171118.1494: *3* draw_model_on
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
                emph1=emph
                (x2, y2) = self.model.get_position(mt)
                if mt == exc_mod:
                    if not selected:
                        continue
                    else:
                        emph1 = True
                if exc_mod == None or not selected or emph1:
                    self._connection(canvas, x1, y1, x2, y2, selected=emph1)
        for m in self.model.modules:
            if m == exc_mod:
                if selected:
                    self._module(canvas, m, selected = True)
            else:
                if not selected:
                    self._module(canvas, m)


    #@+node:eugeneai.20110125174013.1654: *3* remove_selection
    def remove_selection(self):
        if self.selected_item:
            self.selected_item.set_property('pattern', self.draw_module_pattern(self.selected_module))
            for tool in self.tmp_toolbox:
                tool.remove()

        self.tmp_toolbox=[]
        self.tmp_toolbox_group=None

        self.movement_mode = False
        self.selected_module = None
        self.selected_item = None
    #@+node:eugeneai.20110213211825.1661: *3* set_module_name
    def set_module_name(self, item):
        module = item.module
        name = InputDialog(
                message='Enter the block <b>indetifier</b> (name)',
                value=module.name,
                field='Name:',
                secondary='It could be used for Your convenience as a comment.')
        module.modified = module.modified or name != module.name
        module.name = name
        item.text.set_property("text", name)

    #@+node:eugeneai.20110215215529.1657: *3* set_curve_state
    def set_curve_state(self, link, state=None):
        if state == None:
            stroke_color='brown'
            bkg_stroke_color='white'
        elif state=='on_move':
            #stroke_color= 'white'
            #bkg_stroke_color= 'brown'
            stroke_color= 'green'
            bkg_stroke_color= 'black'
        elif state=='selected':
            stroke_color='yellow'
            bkg_stroke_color='brown'

        link.set_property('stroke-color',stroke_color)
        link.bkg_path.set_property('stroke-color',bkg_stroke_color)

    #@+node:eugeneai.20110217131909.1658: *3* create_connection
    def create_connection(self, mf, mt, state=None):
        x1,y1 = self.get_position(mf)
        x2,y2 = self.get_position(mt)
        b,f = self._connection(x1,y1,x2,y2)
        self.set_curve_state(f, None)
        f.mfrom, f.mto = mf, mt
        self.paths.append(f)
        f.connect('enter-notify-event', self.on_curve_enter_leave, f)
        f.connect('leave-notify-event', self.on_curve_enter_leave, f)
        f.connect('button-press-event', self.on_curve_press_release, f)
        f.connect('button-release-event', self.on_curve_press_release, f)
        root=self.ui.canvas.get_root_item()
        root.add_child(b,-1)
        root.add_child(f,-1)
        return b,f
    #@+node:eugeneai.20110217131909.1661: *3* create_module

    def create_module(self, module, x=None, y=None):
        """x=y=None means that the coordinates are taken
        from model.
        """

        if type(module) in [types.UnicodeType, types.StringType]:
            module = ZC.createObject(module)

        if module in self.model.modules:

            if x == None or y == None and module in self.model.modules:
                x,y = self.get_position(module)

        else:
            # XXX x and y should be checked on nonNone.
            self.model.place(module, x, y)


        group=goocanvas.Group(x=x, y=y)
        #pic = PicItem(m, self)
        pic, text=self._module(module)
        pic.module = module
        text.module = module
        group.add_child(pic, -1)
        group.add_child(text, -1)
        pic.connect('enter-notify-event', self.on_module_enter_leave)
        pic.connect('leave-notify-event', self.on_module_enter_leave)
        pic.connect('motion-notify-event', self.on_module_motion)
        pic.connect('button-press-event', self.on_module_press_release)
        pic.connect('button-release-event', self.on_module_press_release)
        text.connect('button-press-event',self.on_module_text_clicked)
        text.connect('button-release-event',self.on_module_text_clicked)
        root=self.ui.canvas.get_root_item()
        root.add_child(group, -1)

        return module
    #@+node:eugeneai.20110311095959.1663: *3* _dbm (debug module)
    def _dbm(self, event=None, x=None, y=None):
        if event:
            x=event.x
            y=event.y
        mt=self.create_module(mdl.LmModule(), x, y)
    #@-others
#@+node:eugeneai.20110116171118.1495: ** class ModuleCanvasView
class ModuleCanvasView(View):
    ZC.adapts(mdli.IModule, IView)
    #@+others
    #@+node:eugeneai.20110116171118.1496: *3* set_model
    def set_model(self, model):
        if self.model != model:
            View.set_model(self, model)
            self.init_resources()

    #@+node:eugeneai.20110116171118.1497: *3* set_parent
    def set_parent(self, parent):
        View.set_parent(self, parent)
        self.init_resources()

    #@+node:eugeneai.20110116171118.1498: *3* init_resources
    def init_resources(self):
        View.init_resources(self)
        self.icon = None
        if self.parent_view:
            if self.model != None and self.model.__class__.icon:
                if self.model.__class__.icon:
                    icon_registry=ZC.getUtility(IIconRegistry, name='svg')
                    self.icon = icon_registry.resource(self.model.__class__.icon)


    #@+node:eugeneai.20110116171118.1499: *3* render_on_canvas
    def render_on_canvas(self, canvas):
        """Render myself on a cairo canvas"""
        if self.icon:
            self.icon.render_cairo(canvas)

    #@-others
#@+node:eugeneai.20110116171118.1500: ** class AdjustenmentView
class AdjustenmentView(View):
    implements(IAdjustenmentView)

    ZC.adapts(mdli.IModule, IView)
    template = "ui/adjustenment_window.glade"
    widget_names = ['vbox', 'main_window',
                    'tree_inputs', 'tree_outputs',
                    'listinputs', 'listoutputs',
                    'title']

    #@+others
    #@+node:eugeneai.20110116171118.1501: *3* __init__
    def __init__(self, model, parent=None):
        View.__init__(self, model, parent=parent)
        self.ui.main_window.set_title(self.model.name)
        self.ui.main_window.show_all()

    #@+node:eugeneai.20110116171118.1502: *3* on_ok_button_clicked
    def on_ok_button_clicked(self, button, data=None):
        self.ui.main_window.destroy()
        self.parent_view.selected_module=None
        self.parent_view.force_paint=True
        self.parent_view.modify_paint=False
        #self.parent_view.queue_draw()

    #@-others

def ModuleChooseDialog(message, filter=None):
    d=ModuleChooseDialogView(message=message, filter=filter)
    v=d.run()
    d.destroy()
    return v

class DialogView(View):
    widget_names = ['dialog']
    def __init__(self, model=None, buttons=(), **kwargs):
        View.__init__(self, model=model, parent=kwargs.get('parent', None))
        self.ui.dialog_vbox=self.ui.dialog.vbox
        kw={}
        kw.update(kwargs)
        self.setup(**kw)
        self.add_buttons(buttons)

    def setup(self, **kw):
        pass

    def add_buttons(self, buttons=()):
        self.ui.dialog.add_buttons(*buttons)

    def run(self):
        result = self.ui.dialog.run()
        if result == gtk.RESPONSE_OK:
            value = self.get_value()
        else:
            value = None
        self.ui.dialog.destroy()
        return value

    def get_value(self):
        raise RuntimeError, "should be implemented by subclass"

    def destroy(self):
        self.ui.dialog.destroy()

class ModuleChooseDialogView(DialogView):
    implements(IApplication)
    template = "ui/module_choose_dialog.glade"
    widget_names = ['dialog', 'vbox', 'title', 'categories',
                    'categories_view', 'description']

    def __init__(self, model=None, **kwargs):
        f=kwargs.pop('filter', None)
        self.set_filter(f)
        DialogView.__init__(self, model=model, **kwargs)

    def set_filter(self, filter):
        self.filter=filter

    def setup(self, message=""):
        fil = self.filter
        def cat_cat(parent, tree):
            for ck, c in tree.iteritems():
                pix=pixbuf_registry.resource(c.icon)
                it = cs.append(parent, [pix, c.name, c.title, True])
                cat_cat(it, c.cats)

                for k, f in c.modules.iteritems():
                    name=k
                    category=f.category
                    title=f.title
                    pix=pixbuf_registry.resource(f._callable.icon)
                    if fil:
                        en = fil(f._callable)
                    else:
                        en = True
                    _ = cs.append(it, [pix, name, title, en])

        self.module_registry=ZC.getUtility(module_is.IModuleRegistry)
        pixbuf_registry=ZC.getUtility(IIconRegistry, name='pixbuf')
        cs=categories=self.ui.categories
        mr=self.module_registry
        cat_cat(None, mr.tree)
        if message:
            self.ui.title.set_markup("<b>"+message+"</b>")

        self.ui.button_cancel=self.ui.dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
        self.ui.button_ok=self.ui.dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        ok=self.ui.button_ok
        ok.set_sensitive(False)

    def get_value(self):
        return self.get_selection()

    def get_selection(self, tv=None, column=1):
        if tv == None:
            tv=self.ui.categories_view
        cm=self.ui.categories
        sel=tv.get_selection()
        m,i=sel.get_selected()
        if i:
            return cm.get_value(i, column)
        return None

    def on_categories_view_cursor_changed(self, tree_view, _):
        name=self.get_selection(tree_view)
        enabled=self.get_selection(tree_view, column=3)
        try:
            f=self.module_registry.modules[name]
            self.ui.description.set_markup(f.description)
            self.ui.button_ok.set_sensitive(enabled)
            return
        except KeyError:
            pass
        try:
            c=self.module_registry.categories[name]
            self.ui.description.set_markup("<b>Category</b>:"+c.description)
            self.ui.button_ok.set_sensitive(False)
            return
        except KeyError:
            pass

_mark554=object()

class IconRegistry(object):
    implements(IIconRegistry)
    def __init__(self, conv=None, attr=None, parent=None):
        self.icons = {}
        self.names = {}
        self.conv=(conv,)
        self.attr=attr
        self.parent=parent

    def resource(self, r=None, name = None):
        if r == None:
            if name != None:
                return self.names[name]
        if r in self.icons:
            return self.icons[r]
        if name == None:
            name=os.path.splitext(os.path.basename(r))[0]
        return self.new_resource(r, name)

    def new_resource(self, r=None, name = None, icon=None):
        if icon == None:
            icon = self.load(r, name)
            answer = self.new_resource(r, name, icon)
            return answer
        conv = self.conv[0]
        if self.conv[0] != None:
            if self.attr:
                kwargs={self.attr:icon}
                icon = conv(**kwargs)
            else:
                icon = conv(icon)
        self.icons[r] = icon
        if name:
            self.names[name] = icon
        return icon

    def load(self, r, name = None):
        if self.parent:
            return self.parent.resource(r=r, name=name)

        ### split : etc..

        if r.find(':')!=-1:
            mod, path = r.split(":",1)
        else:
            mod  = __name__
            path = r

        if os.path.isabs(path):
            path = r
            mod  = None

        if mod == None:
            f=open(r)
            s=f.read()
            f.close()
        else:
            s = resource_string(mod, path)
        return s


icon_registry = IconRegistry(conv=rsvg.Handle, attr='data')

def to_pixbuf(handle=None):
    w=h=32
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c=cairo.Context(s)
    bg = icon_registry.resource(name='selected')
    bg.render_cairo(c)
    handle.render_cairo(c)
    pm=gtk.gdk.pixbuf_new_from_data(s.get_data(),gtk.gdk.COLORSPACE_RGB, True, 8,
                                    s.get_width(), s.get_height(), s.get_stride())
    return pm

pixbuf_registry = IconRegistry(conv=to_pixbuf, attr='handle', parent=icon_registry)

#@-others
#@-leo
