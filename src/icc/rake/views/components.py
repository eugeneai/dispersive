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
from base import *

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
