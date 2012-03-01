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
from collections import OrderedDict

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
    def __init__(self, spectra=None, name=None):
        """Paramter spectra is a list the following structure:
        (channel_array, showing notation).
        """
        if spectra is None:
            spectra = []
        self.spectra = spectra
        self.scale = scale_none
        self.name=name

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

class Spectrum(object):
    def __init__(self, channels=None, name=None):
        self.channels=channels
        self.name=name

class SpectralData(object):
    def __init__(self, name, data=[], filename=None, scale=None):
        self.name=name
        self.data=data
        self.filename=filename

        if scale is None:
            self.set_scale(scale_none)
        else:
            self.set_scale(scale)

        self.xml=None

    def load_xml(self):
        if type(self.data) in [type(''), type(u'')]:
            return self.load(StringIO.StringIO(self.data))
        else:
            return self.load(open(self.filename))

    def load(self, source):
        self.xml = etree.parse(source)

    def get_xml(self):
        if self.xml is not None:
            return self.xml
        self.load_xml()
        return self.xml

    def set_scale(self, scale):
        self.scale=scale

    def get_meta(self):
        try:
            creator = self.get_xml().xpath("//Creator/text()")[0]
        except IndexError:
            creator = ''
        try:
            comment = self.get_xml().xpath("//Comment/text()")[0]
        except IndexError:
            comment = ''
        self.creator=creator
        self.comment=comment
        return self

    def __call__(self):
        d = self.get_meta()
        xml = self.get_xml()
        try:
            o_root = xml.xpath("//ClassInstance[@Type='TRTBase']")[0]
        except IndexError:
            o_root = xml
        spectra = o_root.xpath("//ClassInstance[@Type='TRTSpectrum']")
        nsp=[]
        for s in spectra:
            sname=s.get('Name')
            channels=eval("["+s.xpath("Channels/text()")[0]+"]")
            sp=Spectrum(channels,sname)
            nsp.append(sp)
        self.data=nsp
        return self

#@+node:eugeneai.20110116171118.1348: ** class Project
class Project(object):
    implements(IProject)
    """Project demotes a set of files with spectral data,
        the files are processed the same way.
    """
    #@+others
    #@+node:eugeneai.20110116171118.1349: *3* __init__
    def __init__(self, spectral_data=OrderedDict(), scale=None): # scale here is not of use!! YYY
        self.spectral_data=OrderedDict(spectral_data)

    def set_scale(self, scale):
        """Set this scale to all the files
        """
        for sd in self.spectral_data.items():
            sd.set_scale(scale)

    def add_spectral_data_source(self, filename, name=None):
        if name==None:
            name=os.path.split(filename)[-1] # Just filename and extension
        sd=SpectralData(filename=filename,
            name=name)
        self.spectral_data[filename]=sd
        return sd

    def save(self, filename):
        project=etree.Element("XRF_Project")
        files=etree.SubElement(project, "files")
        for name,sd in self.spectral_data.iteritems():
            file=etree.SubElement(files, "file", filename=name, name=sd.name)
            scale=etree.SubElement(file, "scale", zero=str(sd.scale._zero), scale=str(sd.scale._scale))
        o=open(filename,'w')
        o.write(etree.tostring(project, pretty_print=True))
        o.close()

    def load(self, filename):
        self.spectral_data=OrderedDict()
        i=open(filename)
        project=etree.parse(i)
        files=project.xpath("/XRF_Project/files/file")
        for file in files:
            scale=file.xpath("//scale")[0]
            z=int(scale.get('zero'))
            s=int(scale.get('scale'))
            fname=file.get('filename')
            name=file.get('name')
            sc=Scale(zero=z, scale=s)
            # Check the coincidence with scale_none
            sp=self.add_spectral_data_source(name=name, filename=fname)
            sp.set_scale(sc)

        i.close()

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
        #self.scale = project.scale
        return project

    #@+node:eugeneai.20110116171118.1359: *3* get_spectra
    def get_spectra(self, project = None):
        self.project.spectra=[]
        def _c(x):
            return int(x)

        if project is None:
            project = self.project

        if project is None:
            return []

        # print self.source
        return []
        try:
            xml = project.get_xml()
        except ValueError:
            return []
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
