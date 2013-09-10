#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1453: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1454: ** components declarations
#!/usr/bin/python

from gi.repository import Gtk, GObject

import sys

#import goocanvas, gobject

#Gtk.threads_init()
#print "Threads init."

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
#import rsvg

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
        dialog = Gtk.MessageDialog(
            None,
            Gtk.DialogType.MODAL | Gtk.DialogType.DESTROY_WITH_PARENT,
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsTypeOK,
            None)
        dialog.set_markup(message)
        #create the text input field
        entry = Gtk.Entry()
        #allow the user to press enter to do ok
        entry.connect("activate", responseToDialog, dialog, Gtk.ResponseType.OK)
        #create a horizontal box to pack the entry and a label
        entry.set_text(value)
        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label(field), False, True, 5)
        hbox.pack_end(entry)
        #some secondary text
        dialog.format_secondary_markup(secondary)
        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()
        #go go go
        result = dialog.run()
        if result == Gtk.ResponseType.OK:
            value = entry.get_text()
        dialog.destroy()
        return value
    return getText(value)

#@+node:eugeneai.20110116171118.1457: ** ConfirmationDialog
def ConfirmationDialog(message, secondary=''):
    dialog = Gtk.MessageDialog(
            None,
            Gtk.DialogType.MODAL | Gtk.DialogType.DESTROY_WITH_PARENT,
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsTypeOK.YES_NO,
            None)
    dialog.set_markup(message)
    dialog.format_secondary_markup(secondary)
    rc = dialog.run() == Gtk.ResponseType.YES
    dialog.destroy()
    return rc

#@+node:eugeneai.20110116171118.1458: ** class View
class View(GObject.GObject):
    __gsignals__ = {
        'get-widget': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN,
                       (GObject.TYPE_STRING, GObject.TYPE_PYOBJECT,)),
        'destroy-view': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                       (GObject.TYPE_PYOBJECT,)),
        'model-changed': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
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
        GObject.GObject.__init__(self)
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
        self.connect("model-changed", self.do_model_changed)

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
            # emit signal?

    def on_model_changed(self, model):
        pass

    def do_model_changed(self, model):
        self.on_model_changed(model)

    def invalidate_model(self, model):
        self.on_model_changed(model)

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
            builder=self.ui._builder = Gtk.Builder()
            builder.add_from_string(resource_string(self.resource, template))
            builder.connect_signals(self)
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
        main_frame = self.get_main_frame()
        if main_frame != None :
            main_frame.destroy()
        self.ui=None
        # GObject.GObject.destroy(self)

    def remove_from(self, box):
        widget = self.get_main_frame()
        if widget != None:
            box.remove(widget)

    def insert_into(self, box):
        box.pack_start(self.get_main_frame(), True, True, 0)

    def get_main_frame(self):
        main_widget_name = self.__class__.main_widget_name
        if self.ui != None: # TODO: Strange bug one appeared.
            return getattr(self.ui, main_widget_name)
        else:
            return None

    def on_parent_destroy(self, parent, data=None):
        self.destroy()

    def add_actions_to_menu(self, a_group, label=None, before=None):
        if label == None:
            label = a_group.get_name()

        # find the position of 'before'

        mb = self.locate_widget('menubar')
        if mb == None:
            return

        menu_name="menu_"+label.lower()
        mi_name=a_group.get_name()+"_menu"

        mi = None

        new_menu=True
        for w in mb:
            if w.get_name()==menu_name:
                mi = w
                new_menu=False
                m=mi.get_submenu()
        if mi == None:
            mi = Gtk.MenuItem(label=label)
            mi.set_name(menu_name)

            #Create menu
            m=Gtk.Menu()
            mi.set_submenu(m)

        for a in a_group.list_actions():
            m.append(a.create_menu_item())

        setattr(self.ui, mi_name, mi)

        if new_menu:
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
            separator = Gtk.SeparatorToolItem()
            tb.insert(separator, -1)
            widgets.append(separator)
            separator.show()

        for a in a_group.list_actions():
            if not important or a.get_is_important():
                ti = a.create_tool_item()
                tb.insert(ti, -1)
                widgets.append(ti)
                ti.show()
            #else:
            #    print a, 'did not created', a.get_is_important()

        return widgets

    def del_actions_from_toolbar(self, a_group, widgets):
        tb = self.locate_widget('toolbar')
        if tb == None:
            return

        for w in widgets:
            w.hide()
            tb.remove(w)

        return []

    def get_filename(self, patterns, save=False, open_msg="Open file...", save_msg="Save file...",
            filter_name='Project Files', filename=None):
        if save:
            msg = save_msg
            # msg="Save the project..."
            ac = Gtk.FileChooserAction.SAVE
            icon = Gtk.STOCK_SAVE
        else:
            msg = open_msg
            # msg="Open a project..."
            ac = Gtk.FileChooserAction.OPEN
            icon = Gtk.STOCK_OPEN

        chooser = Gtk.FileChooserDialog(msg, self.locate_widget('main_window'),
            ac,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                icon, Gtk.ResponseType.OK))
        chooser.set_default_response(Gtk.ResponseType.OK)
        chooser.set_current_folder('.')

        ffilter = Gtk.FileFilter()
        ffilter.set_name(filter_name)
        #print "Patterns:", patterns
        for pattern, name in patterns:
            p="*"+pattern
            ffilter.add_pattern(p)
        chooser.add_filter(ffilter)

        if len(patterns)>1:
            for pattern, name in patterns:
                p="*"+pattern
                ffilter = Gtk.FileFilter()
                ffilter.add_pattern(p)
                ffilter.set_name(name+" "+p)
                chooser.add_filter(ffilter)

        ffilter = Gtk.FileFilter()
        ffilter.set_name("All Files")
        ffilter.add_pattern("*")
        chooser.add_filter(ffilter)

        if filename:
            chooser.set_current_name(filename)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
        chooser.destroy()

        if filename != None:
            return self.normalize_file_ext(filename, patterns)
        else:
            return None

    def normalize_file_ext(self, filename, patterns):

        # def_file_ext=self.FILE_PATTERNS[0][0]
        def_file_ext=patterns[0][0]

        (_,ext) = os.path.splitext(filename)
        if not ext:
            filename+=def_file_ext
        return filename



GObject.type_register(View)

    #@-others
#@+node:eugeneai.20110116171118.1466: ** class Application
class Application(View):
    __gsignals__ = {
        'startup-open': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
        'project-open': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, (GObject.TYPE_STRING,)),
        'project-save': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, (GObject.TYPE_STRING,)),
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
        self.FILE_PATTERNS=[e.split(':') for e in opt.get().split('|')]

        self.connect("startup-open", self.on_startup_open)
        self.connect("model-changed", self.on_model_changed_)

                #put event to load project.
                #self.open_project(lo_f)

    def on_model_changed_(self, view, model):
        self.ui.ac_save.set_sensitive(True)

    #@+node:eugeneai.20110116171118.1468: *3* set_model
    def set_model(self, model = None):
        # There should be event created to force model creation
        #if model is None:
        #    model = mdl.Project()
        return View.set_model(self, model)

    #@+node:eugeneai.20110116171118.1469: *3* main_window_delete_event_cb
    # Signal connection is linked in the glade XML file
    def main_window_delete_event_cb(self, widget, data1=None, data2=None):
        Gtk.main_quit()
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
        self.set_model(ZC.createObject(factory_name.get().strip()))
        self.insert_project_view(self.ui)
        self.ui.ac_save.set_sensitive(True)

    #@+node:eugeneai.20110116171118.1472: *3* open_project
    def open_project(self, filename=None):
        if filename is None:
            filename_ = self.get_filename(patterns=self.FILE_PATTERNS, open_msg="Open a project ...", save_msg="Save the project ...")
        else:
            filename_=self.normalize_file_ext(filename, self.FILE_PATTERNS)
        if filename_:
            self.on_file_new()
            success=self.emit("project-open", filename_)
            self.ui.ac_save.set_sensitive(not success)
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
            filename_=self.get_filename(patterns=self.FILE_PATTERNS, save=True)

        if not filename_:
            return # user rejected to write data

        print "Saving the data of the project to file '%s'" % filename_
        success=self.emit("project-save", filename_)
        self.ui.ac_save.set_sensitive(not success)
        self.filename=filename_


    #@+node:eugeneai.20110116171118.1475: *3* error_message
    def error_message(self, message):

        # log to terminal window
        # print message

        # create an error message dialog and display modally to the user
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogType.MODAL | Gtk.DialogType.DESTROY_WITH_PARENT,
                                   Gtk.MessageType.ERROR, Gtk.ButtonsTypeOK.OK, message)

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
        view.connect('model-changed', self.on_model_changed_)
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
        return Gtk.main()

    #@-others
    run = main

GObject.type_register(Application)

#@+node:eugeneai.20110117171340.1635: ** Pictogramm machinery
#@+node:eugeneai.20110123122541.1648: *3* class SVGImage
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
        if result == Gtk.RESPONSE_OK:
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

        self.ui.button_cancel=self.ui.dialog.add_button(Gtk.STOCK_CANCEL, Gtk.RESPONSE_REJECT)
        self.ui.button_ok=self.ui.dialog.add_button(Gtk.STOCK_OK, Gtk.RESPONSE_OK)
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


def to_pixbuf(handle=None):
    w=h=32
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c=cairo.Context(s)
    bg = icon_registry.resource(name='selected')
    bg.render_cairo(c)
    handle.render_cairo(c)
    pm=Gtk.gdk.pixbuf_new_from_data(s.get_data(),Gtk.gdk.COLORSPACE_RGB, True, 8,
                                    s.get_width(), s.get_height(), s.get_stride())
    return pm

#@-others
#@-leo
