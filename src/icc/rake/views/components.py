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
import os

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
class View(object):
    template = None
    widget_names = None
    resource = __name__
    main_widget_name = 'main_frame'
    #implements(IView)
    ZC.adapts(mdli.IModel)

    #@+others
    #@+node:eugeneai.20110116171118.1459: *3* __init__
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

    #@+node:eugeneai.20110116171118.1460: *3* init_resources
    def init_resources(self):
        pass

    #@+node:eugeneai.20110116171118.1461: *3* connect
    def connect(self, signal, method, user_data=None):
        l = self.signals.setdefault(signal, [])
        l.append((method, user_data))

    #@+node:eugeneai.20110116171118.1462: *3* emit
    def emit(self, signal, arg=None):
        d = self.signals.get(signal, [])
        for method, user_data in d:
            args = []
            if arg is not None:
                args.append(arg)
            if user_data is not None:
                args.append(user_data)
            method(self, *args)

    #@+node:eugeneai.20110116171118.1463: *3* set_model
    def set_model(self, model):
        if self.model != model:
            self.model=model
            # some update needed???

    #@+node:eugeneai.20110116171118.1464: *3* set_parent
    def set_parent(self, view):
        """Set parent view. Used for some reason"""
        self.parent_view=view

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
                    setattr(self.ui, name, widget)

    #@-others
#@+node:eugeneai.20110116171118.1466: ** class Application
class Application(View):
    implements(IApplication)
    template = "ui/main_win_gtk.glade"
    widget_names = ['main_window', 'statusbar', 'toolbar',
             "main_vbox"]

    #@+others
    #@+node:eugeneai.20110116171118.1467: *3* __init__
    def __init__(self, model = None):
        View.__init__(self, model=model)
        self.ui.window=self.ui.main_window
        self.ui.window.show_all()
        self.active_view=None

        # Shoul be the last one, it seems
        if 0:
            self.default_view()
            self.open_project(self, LOAD_FILE)

    #@+node:eugeneai.20110116171118.1468: *3* set_model
    def set_model(self, model = None):
        # There shoul be event created to force model creation
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
    def on_file_new(self, widget, data=None):
        # print "Created"
        # check wether data has been saved. YYY
        c=ZC.getUtility(ri.IConfiguration)
        factory_name=c.add_option('factory_name', default='main_model')
        self.set_model(ZC.createObject(factory_name.get()))
        self.insert_project_view(self.ui)

    #@+node:eugeneai.20110116171118.1472: *3* open_project
    def open_project(self, filename=None):
        if filename is None:
            filename = self.get_open_filename()
        if filename:
            self.model = mdl.Project(filename)
            self.default_action()

    #@+node:eugeneai.20110116171118.1473: *3* on_file_open
    def on_file_open(self, widget, data=None):
        return self.open_project()

    #@+node:eugeneai.20110116171118.1474: *3* get_open_filename
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
        if self.active_view is None:
            return
        main_widget = self.active_view.ui.main_frame
        self.ui.main_vbox.remove(main_widget)
        main_widget.destroy()
        self.active_wiew=None

    #@+node:eugeneai.20110116171118.1478: *3* insert_active_view
    def insert_active_view(self, view):
        if self.active_view:
            self.remove_active_view()
        self.active_view = view
        main_widget_name = view.__class__.main_widget_name
        self.ui.main_vbox.pack_start(getattr(view.ui, main_widget_name), True, True)
        view.ui.main_frame.show_all()

    #@+node:eugeneai.20110116171118.1479: *3* insert_project_view
    #def insert_plotting_area(self, ui):
    #    view = IPlottingView(self.model)
    #    self.insert_active_view(view)

    def insert_project_view(self, ui):
        view = IProjectView(self.model)
        self.insert_active_view(view)

    #@+node:eugeneai.20110116171118.1480: *3* main
    def main(self):
        return gtk.main()

    #@-others
    run = main

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
                return rsvg.Handle(data=resource_string(__name__, resource))
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
    ( 1,-1, "remove", 'ui/pics/close.svg'),
    (-1, 1, "rename", 'ui/pics/name.svg'),
    ( 1, 1, "info", 'ui/pics/info.svg'),
    (-1,-1, "edit", 'ui/pics/edit.svg'),

    ( 1, 0, "right", 'ui/pics/right.svg'),
    (-1, 0, "left", 'ui/pics/right.svg'),
    ( 0,-1, "up", 'ui/pics/down.svg'),
    ( 0, 1, "down", 'ui/pics/down.svg'),
    ]

class Canvas(View):
    implements(ICanvasView)

    template = "ui/canvas_view.glade"
    widget_names = ['vbox', 'main_frame']

    #@+others
    #@+node:eugeneai.20110116171118.1482: *3* __init__
    def __init__(self, model = None):
        View.__init__(self, model=None)
        self.icon_cache={}
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

        """
        text=goocanvas.Text(text="Touch me, and I will rotate!",
                       x=300, y=300,
                       anchor=gtk.ANCHOR_CENTER,
                       font="Sans 24", parent=root)
        text.rotate(45, 300, 300)

        text.connect('enter-notify-event', self.on_text_enter_notify_event)
        """

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
        self.module_icon_background = rsvg.Handle(
                data=resource_string(__name__,
                      "ui/pics/background.svg"))
        self.module_icon_selected = rsvg.Handle(
                data=resource_string(__name__,
                      "ui/pics/selected.svg"))
        self.module_icon_toolboxed = rsvg.Handle(
                data=resource_string(__name__,
                      "ui/pics/toolboxed.svg"))
        self.toolbox_background = rsvg.Handle(
                data=resource_string(__name__,
                      'ui/pics/tool-bkg.svg'))

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
                for (dx, dy, name, ui) in TBL_ACTIONS:
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
                m_name = self.choose_module(event)
                if m_name:
                    mt=self.create_module(m_name, event.x_root, event.y_root)
                else:
                    mt=None
            if mt:
                self.create_connection(self.selected_module, mt)
                self.model.connect(self.selected_module, mt)
            self.selected_item.get_parent().raise_(None)
            self.remove_selection()

    def choose_module(self, event):
        name=ModuleChooseDialog(message='Choose a module')
        print name
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
                    if hasattr(_i,'module'):
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
                self.icon = self.parent_view.icon_cache.get(self.model.__class__, None)
                if self.icon == None:
                    self.icon = rsvg.Handle(
                        data=open(self.model.__class__.icon).read())
                    self.parent_view.icon_cache[self.model.__class__]=self.icon

    #@+node:eugeneai.20110116171118.1499: *3* render_on_canvas
    def render_on_canvas(self, canvas):
        """Render myself on a cairo canvas"""
        if self.icon:
            self.icon.render_cairo(canvas)
        """
        canvas.move_to(16, 38)
        canvas.select_font_face ("Sans")
        text = self.model.name
        x_bearing, y_bearing, width, height, x_advance, y_advance = canvas.text_extents(text)
        canvas.rel_move_to(-width/2., height)
        canvas.set_source_rgb(0,0,0)
        canvas.show_text(text)
        canvas.stroke()
        """


    #@-others
#@+node:eugeneai.20110116171118.1500: ** class AdjustenmentView
class AdjustenmentView(View):
    implements(IAdjustenmentView)

    template = "ui/adjustenment_window.glade"
    widget_names = ['vbox', 'main_window']

    #@+others
    #@+node:eugeneai.20110116171118.1501: *3* __init__
    def __init__(self, model):
        View.__init__(self, model)
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

def ModuleChooseDialog(message):
    d=ModuleChooseDialogView(message=message)
    v=d.run()
    d.destroy()
    return v

class DialogView(View):
    widget_names = ['dialog']
    def __init__(self, model=None, buttons=(), **kwargs):
        View.__init__(self, model=model)
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
        DialogView.__init__(self, model=model, **kwargs )

    def setup(self, message=""):
        self.module_registry=ZC.getUtility(module_is.IModuleRegistry)
        cs=categories=self.ui.categories
        mr=self.module_registry
        for k, f in mr.modules.iteritems():
            name=k
            category=f.category
            title=f.title
            pix=gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 32, 32)
            it = cs.append([pix, name, title])
        if message:
            self.ui.title.set_markup("<b>"+message+"</b>")

        self.add_buttons((gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                      gtk.STOCK_OK, gtk.RESPONSE_OK))

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
        f=self.module_registry.modules[name]
        self.ui.description.set_markup(f.description)
        
        

#@-others
#@-leo
