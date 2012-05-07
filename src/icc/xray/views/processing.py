import icc.xray.analysis.scaling as scaling
import icc.xray.analysis.lines as lines
import threading
import pygtk
pygtk.require('2.0')
import gtk, gobject, sys, os

if os.name!="nt":
    ldb=lines.Lines(dbname='/home/eugeneai/Development/codes/dispersive/data/EdxData1.sqlite3')
else:
    ldb=lines.Lines(dbname='C:\\dispersive\\data\\EdxData1.sqlite3')


class Parameters(threading.Thread):
    e_0 = 0.0086
    e_mo= 17.48
    def __init__(self, model, view):
        threading.Thread.__init__(self)
        self.model = model
        self.view = view
        if self.model.parameters == None:
            self.model.parameters = scaling.Parameters(model.channels)
        par=self.model.parameters
        par.set_line_db_conn(ldb)
        self._methods=[]
        self._active=False

    stopthread = threading.Event()

    def set_progressbar(self, pb):
        self.progressbar=pb

    def set_max_step(self, steps):
        self.pb_max=steps
        self.set_fraction(0., steps)

    def set_step(self, step):
        self.pb_step=step
        self.set_fraction(step, self.pb_max)

    def reset_progress(self, steps=None):
        self.pb_step=0
        if steps:
            self.set_max_step(steps)
        else:
            self.set_fraction(step, self.pb_max)

    def next_step(self):
        self.pb_step+=1
        self.set_fraction(self.pb_step, self.pb_max)

    def set_fraction(self, step, steps=None):
        if steps != None:
            frac=float(step)/steps
        else:
            frac=step
        gtk.threads_enter()
        #print step, "of", steps
        self.progressbar.set_fraction(frac)
        gtk.threads_leave()

    def methods(self, names):
        self._methods=names

    def run(self):
        if not self.stopthread.isSet() :
            self._active=True
            for m in self._methods:
                getattr(self, m)()
            self._active=False

    def scaling(self):
        #While the stopthread event isn't setted, the thread keeps going on
        self.reset_progress(9)

        par=self.model.parameters
        pb=self.progressbar
        # Acquiring the gtk global mutex
        ##gtk.threads_enter()
        #Setting a random value for the fraction
        ##progressbar.set_fraction(random.random())
        # Releasing the gtk global mutex
        ##gtk.threads_leave()

        #Delaying 100ms until the next iteration
        ##time.sleep(0.1)

        par.set_scale_lines_kev([self.e_0, self.e_mo])
        par.calculate(plot=False, pb=self.next_step)
        #par.scan_peakes_cwt(plot=True)

    def show(self):
        return
        par=self.model.parameters
        par.set_figure(self.view.ui.ax)
        elements=self.model.elements
        ls = ldb.as_deltafun(order_by="keV", element=elements,
                where="not l.name like 'M%' and keV<20.0")
        ls=list(ls)
        gtk.threads_enter()
        par.line_plot(ls)
        gtk.threads_leave()

    def refine(self):
        par=self.model.parameters
        self.scaling()
        elements=self.model.elements
        par.line_plot(ls)

        ls = ldb.as_deltafun(order_by="keV", element=elements,
                where="not l.name like 'M%' and keV<20.0")
                #where="not l.name like 'M%' and keV<20.0", analytical=True)
        ls=list(ls)
        #pprint.pprint(ls)

        #par.refine_scale(elements=elements-set(['Mo']))
        par.refine_scale(elements=set(['As', 'V']))
        #par.scale.k=0.005004
        #par.scale.b=-0.4843
        par.line_plot(ls)
        ybkg = par.approx_background(elements=elements, plot=True)

        p.plot(par.x, par.channels, color=(0,0,1), alpha=0.6,)
        p.plot(par.x, ybkg, color=(0,1,1), alpha=0.5, linestyle='-')
        par.set_active_channels(par.channels-ybkg)

        par.refine_scale(elements=set(['As', 'V', 'W', 'Mo', 'Zr']), background=False, plot=False)
        par.model_spectra(elements=elements)

        p.plot(par.x, par.channels-ybkg, color=(0,0,0))
        p.axis('tight')
        ax=list(p.axis())
        ax[2]=-ax[-1]/100.
        ax[-1]=ax[-1]*1.1
        p.axis(ax)
        p.axhline(y=0, xmin=0, xmax=1, color=(0,0,0), alpha=0.3, linestyle='--')
        p.show()

    def stop(self):
        """Stop method, sets the event to terminate the thread's main loop"""
        #self.stopthread.set()

    def is_active(self):
        return self._active

