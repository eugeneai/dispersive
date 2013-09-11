#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1453: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1454: ** components declarations
#!/usr/bin/python

from gi.repository import Gtk, GObject

import sys


import icc.rake.views.interfaces
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
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO,
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
    ZC.adapts(mdli.IModel, icc.rake.views.interfaces.IView)

    #@+others
    #@+node:eugeneai.20110116171118.1459: *3* __init__
    def __init__(self, model = None, parent = None):
        GObject.GObject.__init__(self)
        if parent != None:
            if not icc.rake.views.interfaces.IView.providedBy(parent):
                raise ValueError, "Parent does not implement icc.rake.views.interfaces.IView interface."
        if model != None:
            if icc.rake.views.interfaces.IView.providedBy(model):
                raise ValueError, "Model implements icc.rake.views.interfaces.IView interface. It seems You swapped the parameters."
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
        #import pdb; pdb.set_trace()
        #GObject.GObject.connect(self, "get-widget", self.on_get_widget)
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

        if icc.rake.views.interfaces.IView.providedBy(view):
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

    def remove_from(self, box):
        widget = self.get_main_frame()
        if widget != None:
            box.remove(widget)

    def insert_into(self, box):
        box.pack_start(self.get_main_frame(), True, True, 0)

    def get_main_frame(self):
        main_widget_name = self.__class__.main_widget_name
        if self.ui != None: # TODO: Strange bug one appeared.
            if hasattr(self.ui, main_widget_name):
                return getattr(self.ui, main_widget_name)
            else:
                return None
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

    def connect(self, sid, fun, *args):
        to=fun.__self__
        cid=GObject.GObject.connect(self, sid, fun, *args)
        if not hasattr(to, '_sig_conn'):
            to._sig_conn={}
        if not hasattr(self, '_sig_conn'):
            self._sig_conn={}
        l=to._sig_conn.get(sid,[])
        l.append((cid, self))
        to._sig_conn[sid]=l
        self._sig_conn[cid]=l
        print "CConn:", cid, sid, self
        return cid

    def disconnect(self, cid):
        l=self._sig_conn[cid]
        l.remove((cid, self))
        del self._sig_conn[cid]
        rc = GObject.GObject.disconnect(self, cid)
        print "DConn:", cid, rc
        return rc

    def destroy(self):
        print "Destroy:", self
        self.emit('destroy-view', self)
        main_frame = self.get_main_frame()
        if main_frame != None :
            main_frame.destroy()
        self.ui=None
        # GObject.GObject.destroy(self)
        if not hasattr(self, '_sig_conn'):
            return
        all_sids=[]
        t1L=type(1L)
        for k, v in self._sig_conn.iteritems():
            if not type(k) == t1L:
                all_sids.extend(v)
        for sid, ob in all_sids:
            GObject.GObject.disconnect(ob, sid)
            print "GDisconnect:", sid
        del self._sig_conn

GObject.type_register(View)

    #@-others
#@+node:eugeneai.20110116171118.1466: ** class Application
class Application(View):
    __gsignals__ = {
        'startup-open': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
        'project-open': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, (GObject.TYPE_STRING,)),
        'project-save': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_BOOLEAN, (GObject.TYPE_STRING,)),
    }
    implements(icc.rake.views.interfaces.IApplication)
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
                print "Writing user file:", filename_
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
            filename_=self.normalize_file_ext(filename_, self.FILE_PATTERNS)
        else:
            filename_=None
        if not filename_:
            filename_=self.get_filename(patterns=self.FILE_PATTERNS, save=True)

        if not filename_:
            return # user rejected to write data

        print "Saving the data of the project to file '%s'" % filename_
        success=self.emit("project-save", filename_)
        self.ui.ac_save.set_sensitive(not success)
        if success:
            self.filename=filename_
            set_user_config_option('last_project_file_name', filename_, type='string', keys='startup')


    #@+node:eugeneai.20110116171118.1475: *3* error_message
    def error_message(self, message):

        # log to terminal window
        # print message

        # create an error message dialog and display modally to the user
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
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
        view = ZC.getMultiAdapter((self.model, self), icc.rake.views.interfaces.IProjectView)
        self.insert_active_view(view)

    #@+node:eugeneai.20110116171118.1480: *3* main
    def main(self):
        rc = Gtk.main()
        #import pdb; pdb.set_trace()
        self.remove_active_view()
        return rc

    #@-others
    run = main

GObject.type_register(Application)
