#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1336: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1337: ** components declarations
#!/usr/bin/python
"""Module for modelling Energy Dispersive XRF Analysis.
"""
from lxml import etree
import subprocess as spp
import os, os.path
from zope.interface import implements
from icc.xray.models.interfaces import *
import cStringIO as StringIO

DEBUG = True

if os.name=='nt':
    R_CMD="C:\\Program Files\\R\\R-2.10.1\\bin\\R.exe"
else:
    R_CMD="R"

if DEBUG:
    TMP_DIR=os.getcwd()
else:
    if os.name=='nt':
        TMP_DIR="C:\\WINDOWS\\TEMP"
    else:
        TMP_DIR="/tmp"

#@+node:eugeneai.20110116171118.1338: ** class Scale
#print TMP_DIR

class Scale(object):
    """This holds scale calibration constants for X axis (Energies):
    zerov  - channel number of the middle of "zero" pike,
    scalev - keV/channel multiplier.
    """
    #@+others
    #@+node:eugeneai.20110116171118.1339: *3* __init__
    def __init__(self, zero=0, scale=1):
        """Constructs the Scale Calibration
        """
        self._scale = scale
        self._zero  = zero

    #@+node:eugeneai.20110116171118.1340: *3* to_keV
    def to_keV(self, x_array):
        """Given array of channels, e.g., numpy.array([0,...,1024]),
        convert in to enargies.
        """
        return (x_array-self._zero) * self._scale

    to_kev=to_keV

    #@+node:eugeneai.20110116171118.1341: *3* to_channel
    def to_channel(self, kev_array):
        """Given array of keV values, return their channel
        numbers.
        """
        return (kev_array/self.scale)+self._zero

    #@-others
#@+node:eugeneai.20110116171118.1342: ** class Spectra
scale_none=Scale()

class Spectra(object):
    implements(ISpectra)
    #@+others
    #@+node:eugeneai.20110116171118.1343: *3* __init__
    def __init__(self, spectra=None):
        """Paramter spectra is a list the following structure:
        (channel_array, showing notation).
        """
        if spectra is None:
            spectra = []
        self.spectra = spectra
        self.scale = scale_none

    #@+node:eugeneai.20110116171118.1344: *3* set_scale
    def set_scale(self, scale):
        self.scale=scale

    #@+node:eugeneai.20110116171118.1345: *3* r_vect
    def r_vect(self, spectrum, name):
        return '%s = c(%s)\n' % (name, ','.join(map(str, spectrum)))

    #@+node:eugeneai.20110116171118.1346: *3* r_plot
    def r_plot(self, func = '',type_='l', spectrum=None):
        if self.spectra is None:
            self.get_spectra()
        tmp_file = self._get_tmp('R')
        o=open(tmp_file,'w')
        o.write('# Automatically generated, do not edit\n\n')
        o.write(PLOT_PREAMBLE)
        if spectrum is not None:
            spectra=[self.spectra[spectrum]]
        else:
            spectra=self.spectra
        o.write('cols=topo.colors(%i)\n' % (len(spectra)+1))
        i = 0
        names = []
        for sp in spectra:
            i+=1
            name = 'spec%i' % i
            ssp = self.r_vect(sp, name)
            o.write(ssp)
            names.append(name)

        o.write('plot.spectra=function() {\n')
        first = True
        ci = 2
        for name in names:
            Y = '%s(%s)' % (func, name)
            if first:
                o.write("plot(x=scale_X(X), y=%s, type='%s', col=cols[%i])\n" % (Y, type_, ci))
                first = False
            else:
                o.write("lines(x=scale_X(X), y=%s, col=cols[%i], type='%s')\n" % (Y, ci, type_))
            ci+=1
        o.write('} # plot.spectra\n\n')
        o.write(PLOT_POSTAMBLE)
        o.close()
        p=spp.Popen([R_CMD, '--no-save'], stdin=spp.PIPE, stdout=spp.PIPE, stderr=None)
        out,err = p.communicate(PLOT_CMD % tmp_file)
        print out,err


    #@+node:eugeneai.20110116171118.1347: *3* _get_tmp
    def _get_tmp(self, ext):
        return os.path.join(TMP_DIR,'temp.'+ext)


    #@-others
#@+node:eugeneai.20110116171118.1348: ** class Project
class Project(object):
    implements(IProject)
    """Set of spectra with the same Energy axis scale (x-axis)
    """
    #@+others
    #@+node:eugeneai.20110116171118.1349: *3* __init__
    def __init__(self, source=None, scale=None): # scale here is not of use!! YYY
        self.set_source(source)
        if scale is None:
            self.set_scale(scale_none)
        else:
            self.set_scale(scale)

        self.xml=self.spectra=None

    #@+node:eugeneai.20110116171118.1350: *3* load_xml
    def load_xml(self):
        if self.source:
            if self.source.lstrip().startswith('<?'):
                self.load(StringIO.StringIO(self.source))
            else:
                self.load(open(self.source))
            return
        raise ValueError("wrong xml")

    #@+node:eugeneai.20110116171118.1351: *3* load
    def load(self, source):
        self.xml = etree.parse(source)

    #@+node:eugeneai.20110116171118.1352: *3* get_xml
    def get_xml(self):
        if self.xml is not None:
            return self.xml
        self.load_xml()
        return self.xml

    #@+node:eugeneai.20110116171118.1353: *3* set_scale
    def set_scale(self, scale):
        self.scale=scale

    #@+node:eugeneai.20110116171118.1354: *3* get_header
    def get_header(self):
        try:
            creator = self.get_xml().xpath("//Creator/text()")[0]
        except IndexError:
            creator = ''
        try:
            comment = self.get_xml().xpath("//Comment/text()")[0]
        except IndexError:
            comment = ''
        return {'creator':creator, 'comment':comment}

    #@+node:eugeneai.20110116171118.1355: *3* get_objects
    def get_objects(self):
        d = self.get_header()
        xml = self.get_xml()
        try:
            o_root = xml.xpath("//ClassInstance[@Type='TRTBase']")[0]
        except IndexError:
            o_root = xml
        spectra = o_root.xpath("//ClassInstance[@Type='TRTSpectrum']/@Name")
        d['root']=o_root
        d['spectra']=[{'name':spectrum} for spectrum in spectra]
        return d

    def set_source(self, source):
        self.source=source
        self.xml=None
        if self.source:
            self.load_xml()

    #@-others
#@+node:eugeneai.20110116171118.1356: ** class SpectraOfProject
class SpectraOfProject(Spectra):
    implements(ISpectra)
    #@+others
    #@+node:eugeneai.20110116171118.1357: *3* __init__
    def __init__(self, project):
        self.set_project(project)

    #@+node:eugeneai.20110116171118.1358: *3* set_project
    def set_project(self, project):
        self.project = project
        self.get_spectra(self.project)
        self.scale = project.scale
        return project

    #@+node:eugeneai.20110116171118.1359: *3* get_spectra
    def get_spectra(self, project = None):
        self.project.spectra=[]
        def _c(x):
            return int(x)

        print "HERE1"
        if project is None:
            project = self.project

        print "HERE2"
        if project is None:
            return []

        # print self.source
        print "HERE3"
        try:
            xml = project.get_xml()
        except ValueError:
            return []
        print "HERE"
        spectra = xml.xpath('//Channels/text()')
        spectra = [map(_c, sp.split(',')) for sp in spectra]
        names = xml.xpath('//Channels/../@Name')
        spectra = [{"spectrum": sp, "label":nm} for sp, nm in zip(spectra, names)]
        #self.spectra = spectra
        self.project.spectra=spectra
        return spectra

    spectra = property(get_spectra)

    #@-others
#@+node:eugeneai.20110116171118.1360: ** test0
PLOT_CMD='''
source('%s')
quit(save='no')
'''

PLOT_PREAMBLE='''source('global.R')
cols=colors()
'''

PLOT_POSTAMBLE="""
G = gauss(X, l5_9, 2000000)
postscript(file='plot.eps')
plot.spectra()
lines(scale_X(X),G, type='l')
dev.off()
"""


def test0(filename, spectrum=None):
    ss = Spectra(filename)
    ss.r_plot(func='', spectrum=spectrum)
    print 'Spectra length:', len(ss.spectra[0])
    print 'Spectra count:', len(ss.spectra)

#@-others
if __name__=='__main__':
    import sys
    print "ok"
    if len(sys.argv)==1:
        print 'Test run'
        test0('test.rtx')
    else:
        test0(sys.argv[1], spectrum=0)

#@-leo
