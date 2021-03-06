#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1370: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1371: ** components declarations
#!/usr/bin/python

import sys
from gi.repository import Gtk,GObject
from gi.repository.GdkPixbuf import Pixbuf

import drawing

if __name__=="__main__":
    sys.path.append("..")

from icc.xray.views.interfaces import *
from zope.interface import implements, implementsOnly
import zope.component as ZC
import zope.component.interfaces as ZCI
from zope.component.factory import Factory
from pkg_resources import resource_stream, resource_string
from icc.rake.views import get_global_configuration

import icc.xray.models.components as mdl
import icc.xray.models.interfaces as mdli
import icc.rake.views.base as rakeviews
import icc.rake.views.interfaces as rakeints
from icc.xray.views.interfaces import *
import os, os.path
import subprocess as spp

from numpy import arange, sin, pi, array
import numpy as np

import icc.xray.pt.ptwidget as ptwidget

from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas


#import processing as proc

CHANNEL_NO=4096
CALIBR_ZERO=90
CALIBR_KEV=20./(CHANNEL_NO-CALIBR_ZERO)

DEBUG = 2
if DEBUG>2:
    LOAD_FILE="test.rtx"

if os.name!='nt':
    #EPS_CMD="evince"
    EPS_CMD="xdg-open" # YYY Needs to be corrected
else:
    #EPS_CMD="C:\\Program Files\\Ghostgum\\gsview\\gsview32.exe"
    EPS_CMD="start"


FILE_PATTERNS = {
    "*.rtx": "Spectra file, many spectra",
    "*.spx": "Single spectra file",
    }

XPM_META = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "                ",
  "   ......       ",
  "   .XXX.X.      ",
  "   .XXX.XX.     ",
  "   .XXX.....    ",
  "   .XXXXXXX.    ",
  "   .XXX.XXX.    ",
  "   .XXX.XXX.    ",
  "   .XXX.XXX.    ",
  "   .XXX.XXX.    ",
  "   .XXXXXXX.    ",
  "   .XXX.XXX.    ",
  "   .XXXXXXX.    ",
  "   .........    ",
  "                ",
  "                "
  ]

XPM_FILE = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "                ",
  "   ......       ",
  "   .XXX.X.      ",
  "   .XXX.XX.     ",
  "   .XXX.....    ",
  "   .XXXXXXX.    ",
  "   .X.....X.    ",
  "   .X.XXXXX.    ",
  "   .X.XXXXX.    ",
  "   .X...XXX.    ",
  "   .X.XXXXX.    ",
  "   .X.XXXXX.    ",
  "   .XXXXXXX.    ",
  "   .........    ",
  "                ",
  "                "
  ]

XPM_EMPTY = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "................",
  ".XX.XX.XX.XX.XX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XX.XX.XX.XX.XX.",
  "................"
  ]

XPM_SPECTRUM = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "................",
  ".XX.XX.XX.XX.XX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXX.XXXXXXX..",
  ".XXXXX.XXXXXXXX.",
  ".XXXXX.XXXXXXXX.",
  "..XXXX.XXXXXXX..",
  ".XXXXX.XXXXXXXX.",
  ".XXXX.X.XXXXXXX.",
  "..XXX.X.XXXXXX..",
  ".XXXX.X.XXXXXXX.",
  ".XXX.XXX.XXX..X.",
  "....XXXXX...XX..",
  ".XXXXXXXXXXXXXX.",
  ".XX.XX.XX.XX.XX.",
  "................"
  ]

XPM_PROJECT = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "    .......     ",
  "    .XXXXX.     ",
  "    .XXXXX.     ",
  "    .XXXXX.     ",
  "    .XXXXX.     ",
  "    .......     ",
  "     .XXX.      ",
  "     .....      ",
  "      .X.       ",
  "      .X.       ",
  "      .X.       ",
  "   .........    ",
  "   .XXXXXXX.    ",
  "   .XXXXXXX.    ",
  "   .........    ",
  "                "
  ]


XPM_STYLE = [
  "16 16 4 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "O      c #FFFF0000FFFF",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "................",
  ".OOOOOOOOOOOOOO.",
  ".OOOOOOOOOOOOOO.",
  "................",
  "                ",
  "                ",
  "                ",
  "                ",
  "                "
  ]

XPM_NONE = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                "
  ]




#@+node:eugeneai.20110116171118.1372: ** gsm
def gsm():
    return ZC.getGlobalSiteManager()




#@+node:eugeneai.20110116171118.1373: ** class TXRFNavigationToolbar
class TXRFNavigationToolbar(drawing.NavigationToolbar):
    toolitems = drawing.NavigationToolbar.toolitems + (
        # (None, None, None, None, None, None),
        (False, 'Subplots', 'Configure subplots','subplots.png', 'configure_subplots', 'gtk-preferences'),
        (False, 'Save', 'Save the figure','filesave.png', 'save_figure', 'gtk-convert'),
        (True,  'Channels', 'Explore channel counts','filesave.png', 'explore_channels', 'gtk-color-picker'),
        )

#@+node:eugeneai.20110116171118.1391: ** class View
class View(rakeviews.View):
    resource=__name__
    def __init__(self, model=None, parent=None):
        rakeviews.View.__init__(self, model=model, parent=parent)

#@+node:eugeneai.20110116171118.1392: ** class PlottingView
class PlottingView(View):
    __gsignals__ = {
        'spectrum-clicked': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
            (GObject.TYPE_PYOBJECT,
            GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT)),
    }
    implements(IPlottingView)
    ZC.adapts(mdli.IProject, rakeints.IView)
    #@+others
    #@+node:eugeneai.20110116171118.1393: *3* __init__
    def __init__(self, model=None, parent=None):
        #View.__init__(self, model=model, parent=parent)
        if mdli.IProject.providedBy(model):
            model=None
        View.__init__(self, model=model, parent=parent)
        self.plot_options={'show-lines':True}
        self.set_axis_labels()
        #self.ui=rakeviews.Ui()
        self.ui.win=Gtk.Frame()

        #parent_ui= ui = parent.ui #gsm().getUtility(rakeints.IApplication).ui
        parent_ui= ui = gsm().getUtility(rakeints.IApplication).ui

        local=rakeviews.Ui()
        self.local=local

        self.ui.main_frame = win = self.ui.win
        win.set_shadow_type(Gtk.ShadowType.NONE)

        vbox = Gtk.VBox()
        win.add(vbox)

        fig = Figure(figsize=(5,4), dpi=120,
            subplotpars=matplotlib.figure.SubplotParams(left=0.03, right=0.96, bottom=0.03, top=0.96)
         )
        self.ui.fig = fig
        self.ui.ax = fig.add_subplot(111)
        #self.ui.ax2=self.ui.ax.twinx()
        #self.ui.ay2=self.ui.ax.twiny()

        canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
        self.ui.canvas = canvas
        canvas.set_size_request(600, 400)
        vbox.pack_start(canvas, True, True, 0)
        toolbar_ = TXRFNavigationToolbar(canvas, self)

        self.ui.sb=ui.statusbar
        local.msg_id=None
        local.ctx_id=self.ui.sb.get_context_id("plotting")

        self.ui.cid = canvas.mpl_connect('button_press_event', self.on_click)
        # self.ui.check_buttons = widgets.CheckButtons(ax, ['1']*20, [True]*20)

    def set_axis_labels(self, x='', y=''):
        self.axis=rakeviews.Ui()
        self.axis.x_lab=x
        self.axis.y_lab=y
        self.invalidate_model(self.model)
        #self.ui.canvas.draw_idel()

    def on_model_changed(self, view, model):
        self.paint_model(model, conserve=False)

    def set_plot_options(self, options, draw=True):
        self.plot_options=options
        self.paint_model(self.model, draw=draw)

    def paint_model(self, model, draw=True, conserve=True):
        if not hasattr(self.ui,'fig'):
            return
        fig = self.ui.fig
        if conserve:
            lims, pos= self._scan_view(fig)
        fig.clear()

        #self.ui.ax2=self.ui.ax.twinx()
        #self.ui.ay2=self.ui.ax.twiny()
        ax = self.ui.ax
        #ax2 = self.ui.ax2
        #ay2 = self.ui.ay2
        ax.set_ylabel(self.axis.x_lab)
        ax.set_xlabel(self.axis.y_lab) #k$e$V
        if not model:
            t = arange(0.0,3.0,0.01)
            s = sin(2*pi*t)
            pl=ax.plot(t,s, aa=True, linewidth=0.5, alpha=0.5)
        else:
            if model.__class__==mdl.SpectralData:
                m=model.data
            else:
                m=model

            po=self.plot_options
            for i, spec in enumerate(m):
                spectrum = spec.channels
                sp_len = len(spectrum)
                X = arange(sp_len)
                #kevs = self.model.scale.to_keV(X)
                ssp={}
                ssp.setdefault('aa', True)
                #ssp.setdefault('linewidth', 1)
                ssp.setdefault('alpha',0.6)
                kwargs = {}
                kwargs.update(ssp)
                #del kwargs['spectrum']
                #pl, = ax.plot(kevs, spectrum, **kwargs)
                if po.get('channels', True):
                    pl, = ax.plot(X, spectrum, **kwargs)
                    ax.axis('tight')
                    _ax=list(ax.axis())
                    print "A", _ax
                    _ax[-1]=np.max(spectrum[150:])
                    _ax[2]=-_ax[-1]/100.
                    _ax[-1]=_ax[-1]*1.1
                    ax.axis(_ax)
                if spec.parameters and po.get('background', False) and spec.parameters.bkg!=None:
                    kwbkg={}
                    kwbkg.update(kwargs)
                    kwbkg['alpha']=0.6
                    kwbkg['color']='blue'
                    pl, = ax.plot(X, spec.parameters.bkg, **kwbkg)

                ax.axhline(y=0, xmin=0, xmax=1, color=(0,0,0), alpha=0.3, linestyle='--')
                #ax.set_yticklabels([])
                #ax.set_xticklabels([])
                #spec['line2D'] = pl

            #ax.set_title('Spectra plot')
            #ax.set_xlim(kevs[0],kevs[-1])
            ax.set_xlim(X[0],X[-1])
            # ax.set_yscale('log')
            ax.grid(b=True, aa=False, alpha=0.3)
            #ax.legend()
            ax.minorticks_on()
            #ax.ticklabel_format(style='sci', scilimits=(3,0), axis='y')
            for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(5)
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(5)
            #ax2=ax.twinx()
            #ax2.set_xticklabels(["0", r"$\frac{1}{2}\pi$",
            #         r"$\pi$", r"$\frac{3}{2}\pi$", r"$2\pi$"])
            #ax.set_xticklabels(["0", r"$\frac{1}{2}\pi$",
            #         r"$\pi$", r"$\frac{3}{2}\pi$", r"$2\pi$"])
            #ax2.set_xlim(ax.get_xlim())
            #pyplot.setp(ax2, xticklabels=['1', '2'])
            #top.set_xlabels(ax.get_xlabels())
            #for tick in ax2.get_xticklabels():
            #    tick.set_fontsize(5)
        if conserve:
            self._update_view(fig, lims, pos)
        if draw:
            self.ui.canvas.draw_idle()

    def _update_view(self, figure, lims,  pos):
        for i, a in enumerate(figure.get_axes()):
            xmin, xmax, ymin, ymax = lims[i]
            a.set_xlim((xmin, xmax))
            a.set_ylim((ymin, ymax))
            # Restore both the original and modified positions
            a.set_position( pos[i][0], 'original' )
            a.set_position( pos[i][1], 'active' )

    def _scan_view(self, figure):
        lims = []; pos = []
        for a in figure.get_axes():
            xmin, xmax = a.get_xlim()
            ymin, ymax = a.get_ylim()
            lims.append( (xmin, xmax, ymin, ymax) )
            # Store both the original and modified positions
            pos.append( (
                    a.get_position(True).frozen(),
                    a.get_position().frozen() ) )
        return lims, pos

    #@+node:eugeneai.20110116171118.1394: *3* on_click
    def on_click(self, event, data=None):
        local = self.local
        if local.msg_id is not None:
            self.ui.sb.remove(local.ctx_id, local.msg_id)
        if event.xdata and event.ydata:
            s='button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
                event.button, event.x, event.y, event.xdata, event.ydata)
        else:
            s=' '.join([str(x) for x in [event.button, event.x, event.y, event.xdata, event.ydata]])

        local.msg_id=self.ui.sb.push(local.ctx_id, s)

        self.emit('spectrum-clicked', event.button, event.x, event.y, event.xdata, event.ydata)

    #@+node:eugeneai.20110116171118.1395: *3* on_spectra_clicked
    def on_spectra_clicked(self, project_view):
        #print "Spectra_clicked!!"
        any_vis = False
        for sp in self.model.spectra:
            alpha = sp.setdefault('alpha',1.0)
            if alpha>0.1:
                any_vis = True
        [self._set(sp, not any_vis) for sp in self.model.spectra]
        self.ui.canvas.draw_idle()

    #@+node:eugeneai.20110116171118.1396: *3* on_spectrum_clicked
    def on_spectrum_clicked(self, project_view, spectrum_data, user_data=None):
        #print "Spectrum selected:", spectrum_data
        path = spectrum_data['path']
        index = path[-1]
        s=self.model.spectra
        spec = s[index]
        spec['path'] = path
        if spec['label'] != spectrum_data['name']:
            print "Warning: name difference!!"

        # print spec
        self._toggle(spec)
        self.ui.canvas.draw_idle()

    #@+node:eugeneai.20110116171118.1397: *3* _toggle
    def _toggle(self, spec):
        line = spec['line2D']
        newalpha = 1.0 - spec.get('alpha', 1.0)
        line.set(alpha=newalpha)
        spec['alpha']=newalpha

    #@+node:eugeneai.20110116171118.1398: *3* _set
    def _set(self, spec, vis):
        line = spec['line2D']
        newalpha = int(vis) * 1.0
        line.set(alpha=newalpha)
        spec['alpha']=newalpha

GObject.type_register(PlottingView)

    #@-others
#@+node:eugeneai.20110116171118.1399: ** class ProjectView
#pffactory = Factory(PlottingFrame, 'PlottingFrame', 'Frame, where one can plot spectra.')
#gsm().registerUtility(pffactory, ZCI.IFactory, 'PlottingFrame')

class ProjectView(View):
    __gsignals__ = {
        'spectrum-clicked': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
            (GObject.TYPE_STRING, GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT)), # filename and spectrum choosen
        'file-clicked': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
            (GObject.TYPE_STRING, GObject.TYPE_PYOBJECT)), # filename and all its spectra
    }
    template = "ui/project_frame.glade"
    widget_names = ["project_frame",
                    "project_tree_view", "main_vbox", "common_label",
                    "project_list_model", "project_tree_model", "paned_top", "paned_bottom",
                    "ag_spectra", "ag_process",
                    "ag_other", "ac_convert_to",
                    'ac_ptable','ac_scaling',
                    'progressbar',
                    ]
    implements(rakeints.IProjectView)
    ZC.adapts(mdli.IProject, rakeints.IView)
    #@+others
    #@+node:eugeneai.20110116171118.1400: *3* __init__
    def __init__(self, model=None, parent=None):
        self.active_view = None
        View.__init__(self, model=model, parent=parent)
        self.ui.main_frame=self.ui.project_frame
        self.active_fpath=None # active filename and path as a tuple or None

        _conf=get_global_configuration()
        opt=_conf.add_option('spectra_file_ext', default='.*:All Files', keys='app')
        self.FILE_PATTERNS=[e.split(':') for e in opt.get().split('|')]

        self.active_view = ZC.getMultiAdapter((self.model, self), IPlottingView)
        self.active_view.connect('spectrum-clicked', self.on_plot_spectrum_clicked)
        #self.connect('spectrum-clicked', self.active_view.on_spectrum_clicked)
        #self.connect('file-clicked', self.active_view.on_spectra_clicked)
        self.connect('spectrum-clicked', self.on_spectrum_clicked)
        self.connect('spectrum-clicked', self.on_refine_scaling)
        self.connect('file-clicked', self.on_file_clicked)
        self.ui.main_vbox.pack_start(self.active_view.ui.main_frame, True, True, 0)
        self.ui.hpaned_list=[self.ui.paned_top, self.ui.paned_bottom]

        self.add_actions_to_menu(self.ui.ag_spectra, label='Spectra')
        self.ui.tb_widgets=self.add_actions_to_toolbar(self.ui.ag_spectra)

        self.add_actions_to_menu(self.ui.ag_process, label='Spectra')
        self.ui.tb_widgets2=self.add_actions_to_toolbar(self.ui.ag_process)

        self.add_actions_to_menu(self.ui.ag_other, label='Spectra')

        parent.connect('project-open', self.on_file_open)
        parent.connect('project-save', self.on_file_save)

        self.project_tree_selection = self.ui.project_tree_view.get_selection()
        self.project_tree_selection.connect('changed',self.on_project_tree_selection_changed)

        self.ui.ag_process.set_sensitive(False)
        self.p_thread=None

    def do_destroy_view(self, self_widget, data=None):
        self.del_actions_from_menu(self.ui.ag_spectra)
        self.del_actions_from_toolbar(self.ui.ag_spectra, self.ui.tb_widgets)
        self.del_actions_from_menu(self.ui.ag_process)
        self.del_actions_from_toolbar(self.ui.ag_process, self.ui.tb_widgets2)
        rc=gsm().queryUtility(IPeriodicTableView)
        if rc:
            rc.destroy()
            gsm().unregisterUtility(rc, IPeriodicTableView)

    def on_file_open(self, app, filename, data=None):
        try:
            self.model.load(filename)
        except OSError:
            return False
        self.set_model(self.model)
        return True

    def on_file_save(self, app, filename, data=None):
        self.model.save(filename)
        return True

    def on_periodic_table(self, widget):
        active = widget.get_active()
        rc=gsm().queryUtility(IPeriodicTableView)
        if rc==None:
            #factory=gsm().queryUtility(IPeriodicTableView, 'periodic-table-factory')
            pt=ZC.createObject('periodic-table-factory')
            gsm().registerUtility(pt, IPeriodicTableView)
            pt.connect("window-hide",
                lambda x: self.ui.ac_ptable.set_active(False)
            )
            pt.connect("selected", self.on_ptable_selected)
            pt.connect("refine", self.on_refine_scaling)
            pt.connect('clear-scaling', self.on_clear_scaling)
            pt.connect('external-scaling', self.on_external_scaling)
            pt.connect('interval-changed', self.on_interval_changed)
            pt.connect('show-lines', self.on_adjust_graphics)
            pt.connect('background', self.on_show_background)
        else:
            pt=rc
        if active:
            pt.show()
            self.ui.ac_scaling.set_active(True)
        else:
            pt.hide()

    def on_scaling_toggled(self, widget, *args):
        if widget.get_active():
            print "Scaling started"
            self.p_thread_tasks(['scaling', 'show'])
        else:
            print "Scaling stopped"
            if self.p_thread:
                self.p_thread.stop()
            self.ui.ac_ptable.set_active(False)

    def on_external_scaling(self, widget, active):
        if active:
            amp=self.active_view.model[0].parameters
            eamp=self.active_view.model[0].extparams
            amp.scale.b=eamp.scale.b
            amp.scale.k=eamp.scale.k
            self.p_thread_tasks(['show'])
        else:
            self.active_view.model[0].parameters.scale.done=False
            self.p_thread_tasks(['scaling', 'show'])

    def on_clear_scaling(self, widget):
        print "Clear scaling"

    def on_show_background(self, widget, active):
        self.active_view.plot_options['background']=active
        if active:
            self.active_view.plot_options
            self.p_thread_tasks(['scaling','background','show'])
        else:
            self.p_thread_tasks(['show'])

    def on_adjust_graphics(self, widget, options):
        self.active_view.set_plot_options(options, draw=False)
        self.p_thread_tasks(['show'])

    def on_ptable_selected(self, table, list):
        self.active_view.model[0].ptelements=list
        self.p_thread_tasks(['show'])

    def p_thread_tasks(self, tasks):
        if self.p_thread == None or not self.p_thread.is_active():
            self.p_thread=proc.Parameters(self.active_view.model[0], self.active_view) # adapter ??
            self.p_thread.set_progressbar(self.ui.progressbar)
            self.p_thread.methods(tasks)
            self.p_thread.start()

    def on_plot_spectrum_clicked(self, plot, button, x,y, xdata, ydata):
        if self.ui.ac_ptable.get_active():
            pt = gsm().queryUtility(IPeriodicTableView)
            pt.cursor_clicked=(button, x,y, xdata, ydata)
            self.show_local_lines(pt)

    def on_interval_changed(self, widget, value):
        pt = widget
        if pt.cursor_clicked != None:
            self.show_local_lines(pt)

    def show_local_lines(self, pt):
        if pt != None:
            model=self.active_view.model[0]
            params=model.parameters
            if params==None:
                return
            conn=proc.line_db_conn()
            line_list=pt.ui.line_list
            line_list.clear()
            (button, x,y, xdata, ydata)=pt.cursor_clicked
            interval=pt.ui.interval.get_value()
            x0=model.parameters.channel_to_keV(xdata)
            gen=conn.select(
                    where="abs(keV-(%f))<(%f)" % (x0, interval),
                    order_by="abs(keV-(%f))" % x0,
                )
            lines=list(gen)
            #lines.sort(key=lambda l: abs(l.keV - x0))
            lines.sort(key=lambda l: l.name)
            for l in lines:
                line_list.append((l.element, l.line, "%6.3f" % l.keV, l.Z))

    def on_refine_scaling(self, view, filename=None, spectrum=None, sp_data=None):
        if sp_data != None:
            (sp, spec_no) = sp_data
        print "Refine scaling..."
        # self.p_thread_tasks(['refine','show'])
        print "Refine scaling ended."

    #@+node:eugeneai.20110116171118.1401: *3* get_objects
    def get_objects(self):
        try:
            d = self._obj_cache
            return d
        except AttributeError:
            try:
                int('df')
                d = self.model.get_objects()
                self._obj_cache = d
            except ValueError, exc:
                #print "EXC:", exc
                d = {"creator":'', 'comment':'',
                     'spectra':[]}
                # skip cache !!!
        return d

    #@+node:eugeneai.20110116171118.1402: *3* set_model
    def set_model(self, model=None):
        View.set_model(self, model=model)
        #if self.active_view:
        #    self.active_view.set_model(mdli.ISpectra(self.model))
        #    self.active_view.invalidate_model(self.active_view.model)

        try:
            t = self.ui.project_tree_model
        except AttributeError:
            return
        t.clear()

        d = self.get_objects()

        pb = Pixbuf.new_from_xpm_data(XPM_PROJECT)
        pm = Pixbuf.new_from_xpm_data(XPM_META)
        pc = Pixbuf.new_from_xpm_data(XPM_SPECTRUM)
        ps = Pixbuf.new_from_xpm_data(XPM_STYLE)
        pn = Pixbuf.new_from_xpm_data(XPM_NONE)
        pf = Pixbuf.new_from_xpm_data(XPM_FILE)
        self.ui.pb_project = pb
        self.ui.pb_meta = pm
        self.ui.pb_file = pf
        self.ui.pb_spectrum = pc
        self.ui.pb_empty = Pixbuf.new_from_xpm_data(XPM_EMPTY)
        self.ui.pb_none = pn
        self.ui.ps_style= ps
        root = t.append(None, ('Project', pb, False, False, pn))
        meta = t.append(root, ('Info', pm, False, False, pn))
        #print self.model.spectral_data
        for name, sd in self.model.spectral_data.iteritems():
           f = t.append(root, (sd.name, pf, False, False, pn))
           for sp in sd().data:
               s = t.append(f, (sp.name, pc, False, False, ps))
        """
        self.spectra_it = spectra
        for sp in d['spectra']:
            sp_it = t.append(spectra, (sp['name'], pc, False, False, ps))
            sp['path']=t.get_path(sp_it)
        """
        self.ui.project_tree_view.expand_all()


    #@+node:eugeneai.20110116171118.1403: *3* set_pb
    def set_pb(self, path, pb):
        tm =  self.ui.project_tree_model
        it = tm.get_iter(path)
        tm.set_value(it, 1, pb)

    #@+node:eugeneai.20110116171118.1404: *3* on_spectra_clicked
    def on_file_clicked(self, widget, filename, sp, user_data=None):
        self.active_view.set_model(sp)
        self.active_view.invalidate_model(sp)
        self.set_element_list()

    #@+node:eugeneai.20110116171118.1405: *3* on_spectrum_clicked
    def on_spectrum_clicked(self, widget, filename, spec, sp_and_no, user_data=None):
        self.active_view.set_model([spec])
        self.active_view.invalidate_model([spec])
        self.set_element_list(spec, sp_and_no)

    def set_element_list(self, spec=None, sp_and_no=None):
        elems=self.ui.project_list_model
        elems.clear()
        if not spec:
            return
        (sp, spec_no) = sp_and_no
        return #FIXME
        for el in spec.elements.values():
            row=(int(el.Atom), 'Xx', el.XLine,
                -1, int(el.Cycles), float(el.NetIntens), float(el.Background),
                float(el.Sigma),
                float(el.Chi), float(el.MassPercent), -1, -1)
            elems.append(row)

    #@+node:eugeneai.20110116171118.1406: *3* _renew_vis_project_tree
    def _renew_vis_project_tree(self,spec=None):
        if spec == None:
            pass
        any_vis = False
        channels=spec.channels
        name=spec.name
        #~ sd = self.get_objects()['spectra']
        #~ t = self.ui.project_tree_model
        #~ for i, sp in enumerate(self.active_view.model.spectra):
            #~ alpha = sp.setdefault('alpha', 1.0)
            #~ path = sp.setdefault('path', sd[i].get('path', None))
            #~ if path is None:
                #~ continue
            #~ if alpha>0.1:
                #~ self.set_pb(path, self.ui.pb_spectrum)
                #~ any_vis = True
            #~ else:
                #~ self.set_pb(path, self.ui.pb_empty)
        #~ path = t.get_path(self.spectra_it)
        #~ if any_vis:
            #~ self.set_pb(path, self.ui.pb_spectrum)
        #~ else:
            #~ self.set_pb(path, self.ui.pb_empty)


    #@+node:eugeneai.20110116171118.1407: *3* on_row_activated

    def interp_path(self, path):
        lp=len(path)
        if lp==1:
            return ('root',)
        if path[1]==0:
            return ('info',)
        file_no=path[1]-1 # Minus info node
        filename, sp=self.model.spectral_data.items()[file_no]
        if lp==2:
            return ('file', filename, sp)
        else:
            spec_no=path[-1]
            return ('spectrum', filename, sp.data[spec_no], (sp, spec_no))

    def on_row_activated(self, tree_view, path, column, data=None):
        #print 'Clicked:', tree_view, path, column, data
        #if self.p_thread and self.p_thread.is_alive():
        if self.p_thread:
            self.p_thread.stop()
            self.p_thread=None
        self.ui.progressbar.set_fraction(0.)
        lp=len(path)
        self.ui.ac_scaling.set_active(False)
        if lp==1:
            # root clicked
            self.ui.ag_process.set_sensitive(False)
            return
        file_no=path[1]-1 # Minus info node
        filename, sp=self.model.spectral_data.items()[file_no]
        if lp==2:
            #file clicked
            self.emit('file-clicked', filename, sp)
            self.ui.ag_process.set_sensitive(False)
            return
        else:
            spec_no=path[-1]
            self.ui.ag_process.set_sensitive(True)
            self.emit('spectrum-clicked', filename, sp.data[spec_no], (sp, spec_no))

    def on_project_tree_selection_changed(self, selection):
        pm, it = selection.get_selected()
        path = pm.get_path(it)
        rc=self.interp_path(path)
        self.active_fpath=(rc, path)
        # print "Selection", self.active_fpath

    #Horizontal paned synchronisation.

    def on_paned_notify(self, paned, spec, data=None):
        if spec.name=='position':
            pos=paned.get_property('position')
            [p.set_position(pos) for p in self.ui.hpaned_list if p!=paned] # recursion breaks due to position property: it can be unchanged.

    def on_spectra_close(self, widget, data=None):
        if self.p_thread:
            self.p_thread.stop()
            self.p_thread=None
        if self.active_fpath == None:
            return
        rc,path=self.active_fpath
        # print rc
        if rc[0]=='file':
            del self.model.spectral_data[rc[1]]
            pm=self.ui.project_tree_model
            pm.remove(pm.get_iter(path))
            self.set_model(self.model)
            #self.active_view.canvas.draw_idle()
            # print "removed"

    def on_spectra_export(self, widget, data=None):
        print "On spectra export", widget, data

    def on_spectra_load(self, widget, data=None):
        file_name = self.get_filename(self.FILE_PATTERNS,
            open_msg="Load spectra ...",
            filter_name='Spectra Files')
        if file_name != None:
            self.load_spectra(file_name)

    def on_convert_to(self, widget, data=None):
        print "Ok", widget, data
        if self.active_fpath == None:
            return
        rc,path=self.active_fpath
        print rc
        # ('spectrum', filename, sp.data[spec_no], (sp, spec_no))
        if rc[0]=='spectrum':
            _, filename, sp_data, _ = rc
            print self.FILE_PATTERNS
            filename=self.get_filename(self.FILE_PATTERNS,
                save=True,
                open_msg="Export to a file...",
                save_msg="Save file...",
                filter_name='Spectra Files',
                filename=filename.replace('.','_')+'-'+sp_data.name+'.spe')
            if filename:
                self.convert_to(sp_data, filename)

    def convert_to(self, sp_data, filename):
        name, ext = os.path.splitext(filename)
        o=file(filename, "w")
        if ext=='.spe':
            print ">>> Exporting", sp_data.name, filename, ext
            o.write("$MEAS_TIM:\n    972    1000\n$DATE_MEA:\n12-03-2010  16:52:15\n")
            o.write("$MCA_CAL:\n 3\n 8.785848e-001 3.627669e-002 1.488566e-006\n$DATA:\n")
            ll=len(sp_data.channels)
            c1=np.zeros(ll/2)
            c2=np.zeros(ll/2)
            for i, ch in enumerate(sp_data.channels):
                if i % 2 == 0:
                    c1[i/2]=ch
                else:
                    c2[(i-1)/2]=ch
            c=c1+c2
            o.write("%9i%9i" % (0, len(c)-1))
            for i, ch in enumerate(c):
                if i % 10 == 0:
                    o.write("\n")
                o.write("%9i" % ch)
            o.write("\n")
        o.close()

    def load_spectra(self, file_name):
        self.model.add_spectral_data_source(file_name)
        self.set_model(self.model)
        #self.active_view.canvas.draw_idel()

    #@-others

GObject.type_register(ProjectView)

class PeriodicTableWindow(View):
    __gsignals__ = {
        'window-hide': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, tuple()),
        'refine': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, tuple()),
        'clear-scaling': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, tuple()),
        'external-scaling': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
        'background': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
        'show-lines': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
        'selected': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
        'interval-changed': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_FLOAT,)),
    }
    implements(IPeriodicTableView)
    template = "ui/periodic_table_window.glade"
    'Cl,Mo,Si,S,P,As,W,V,Zr,Ar,Hf'
    widget_names = ["pt_window",
            "hbox",
            "lines_view", 'line_list',
            'pt_place',
            'interval',
            'ac_refine_scaling', 'ac_clear',
            'ac_k', 'ac_l', 'ac_m', 'ac_peakes',
            'ac_show_lines', 'ac_an_lines',
            'ac_channels', 'ac_clean_channels',
            'ac_background'
    ]
    def __init__(self, model=None):
        if model == None:
            model=mdl.AnalysisTask()
        View.__init__(self, model=model)
        self.ui.pt_window.set_keep_above(True)
        self.ui.table=ptwidget.PTToggleWidget()
        self.ui.pt_place.add(self.ui.table)
        self.ui.table.connect('toggled', self.on_table_toggled)
        self.ui.pt_window.connect('delete-event', self.on_delete_event)
        label=self.ui.label=Gtk.Label("Elements:")
        self.ui.table.ui.pt.attach(label, 0, 2, 7,8)
        label.set_alignment(1., 0.5)
        in_list=self.ui.input_list=Gtk.Entry()
        in_list.connect('changed', self.on_input_list_changed)
        #in_list.connect('activate', self.on_input_list_activate)
        self.ui.table.ui.pt.attach(in_list, 2, 18, 7,8)
        self._list_block=False
        self.ui.ac_refine_scaling.set_sensitive(False)

        it=self.ui.interval
        it.set_range(0., 2.)
        it.set_increments(0.05, 0.1)
        it.set_value(0.1)

        self.cursor_clicked=None # Last cursor clicked here. Modified by a superior widget.

    def on_interval_changed(self, spb):
        self.emit('interval-changed', spb.get_value())

    def show(self):
        self.ui.pt_window.show_all()

    def hide(self):
        self.ui.pt_window.hide()

    def destroy(self):
        self.ui.pt_window.destroy()

    def on_table_toggled(self, table, Z, symbol, button):
        if button.get_active():
            self.model.elset.add(symbol)
        else:
            self.model.elset.remove(symbol)

        self.ui.input_list.set_text(','.join(self.model.elset))
        if not self._list_block:
            self.emit("selected", self.model.elset)

    #def on_input_list_changed(self, ib):
    #    self.ui.input_list.

    def on_input_list_changed(self, ib, *args):
        if self._list_block:
            return
        self._list_block=True
        list=ib.get_text()
        list=list.replace(';',',').strip().split(',')
        list=[l.strip() for l in list]
        bad=self.ui.table.select(list, active=True, only=True)
        """
        if bad:
            ib.modify_bg(Gtk.)
            style = el.get_style().copy()
        """
        ls=len(list)
        lb=len(bad)
        if ls-lb>=2:
            self.ui.ac_refine_scaling.set_sensitive(True)
        else:
            self.ui.ac_refine_scaling.set_sensitive(False)
        self._list_block=False
        self.emit("selected", self.model.elset)

    def on_delete_event(self, window, event):
        window.hide()
        self.emit("window-hide")
        return True

    def on_refine_scaling(self, window, *args):
        self.emit('refine')

    def on_clear_scaling(self, window, event):
        self.emit('clear-scaling')

    def on_use_ext_scaling(self, window, event):
        self.emit('external-scaling', window.get_active())

    def on_clear_all(self, window, event):
        if self._list_block:
            return
        self._list_block=True
        self.ui.table.select([], active=True, only=True)
        self._list_block=False
        self.ui.ac_refine_scaling.set_sensitive(False)
        self.emit("selected", self.model.elset)

    def on_list_row_activated(self, list, path, view_column, *args):
        m=list.get_model()
        symbol = m[path[0]][0]
        self.ui.table.select([symbol], active=True)

    def on_ac_background_toggled(self, widget, *args):
        #self.on_show_line_toggled(widget=widget, emit=True)
        self.emit("background", widget.get_active())

    def on_show_line_toggled(self, widget, emit=True, *args):
        d={}
        d['k']=self.ui.ac_k.get_active()
        d['l']=self.ui.ac_l.get_active()
        d['m']=self.ui.ac_m.get_active()
        d['analytical']=self.ui.ac_an_lines.get_active()
        d['peakes']=self.ui.ac_peakes.get_active()
        d['channels']=self.ui.ac_channels.get_active()
        d['clean-channels']=self.ui.ac_clean_channels.get_active()
        d['background']=self.ui.ac_background.get_active()
        sl=d['show-lines']=self.ui.ac_show_lines.get_active()
        self.ui.ac_k.set_sensitive(sl)
        self.ui.ac_l.set_sensitive(sl)
        self.ui.ac_m.set_sensitive(sl)
        self.ui.ac_an_lines.set_sensitive(sl)
        if emit:
            self.emit('show-lines', d)

GObject.type_register(PeriodicTableWindow)

if __name__=="__main__":
    # print "Cannot run without external support!!"
    import icc.icc_xray_app
    icc.icc_xray_app.main()


#@-others
#@-leo
