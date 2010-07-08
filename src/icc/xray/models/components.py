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
    
#print TMP_DIR

class Scale(object):
    """This holds scale calibration constants for X axis (Energies):
    zerov  - channel number of the middle of "zero" pike,
    scalev - keV/channel multiplier.
    """
    def __init__(self, zero=0, scale=1):
        """Constructs the Scale Calibration
        """
        self._scale = scale
        self._zero  = zero
        
    def to_keV(self, x_array):
        """Given array of channels, e.g., numpy.array([0,...,1024]),
        convert in to enargies.
        """
        return (x_array-self._zero) * self._scale

    to_kev=to_keV
    
    def to_channel(self, kev_array):
        """Given array of keV values, return their channel
        numbers.
        """
        return (kev_array/self.scale)+self._zero

scale_none=Scale()

class Spectra(object):
    implements(ISpectra)
    def __init__(self, spectra=None):
        """Paramter spectra is a list the following structure:
        (channel_array, showing notation).
        """
        if spectra is None:
            spectra = []
        self.spectra = spectra
        self.scale = scale_none
        
    def set_scale(self, scale):
        self.scale=scale
        
    def r_vect(self, spectrum, name):
        return '%s = c(%s)\n' % (name, ','.join(map(str, spectrum)))
    
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
        

    def _get_tmp(self, ext):
        return os.path.join(TMP_DIR,'temp.'+ext)


class Project(object):
    implements(IProject)
    """Set of spectra with the same Energy axis scale (x-axis)
    """
    def __init__(self, source=None, scale=None): # scale here is not of use!! YYY
        self.source = source
        if scale is None:
            self.set_scale(scale_none)
        else:
            self.set_scale(scale)
            
        self.xml=self.spectra=None

    def load_xml(self):
        if self.source:
            if self.source.lstrip().startswith('<?'):
                self.load(StringIO.StringIO(self.source))
            else:
                self.load(open(self.source))
            return
        raise ValueError("wrong xml")
        
    def load(self, source):
        self.xml = etree.parse(source)

    def get_xml(self):
        if self.xml is not None:
            return self.xml
        self.load_xml()
        return self.xml

    def set_scale(self, scale):
        self.scale=scale

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

    def get_objects(self):
        d = self.get_header()
        xml = self.get_xml()
        try:
            o_root = xml.xpath("//ClassInstance[@Type='TRTBase']")[0]
        except IndexError:
            o_root = xml
        spectra = o_root.xpath("//ClassInstance[@Type='TRTSpectrum']/@Name")
        d['root']=o_root
        d['spectra']=spectra
        return d

class SpectraOfProject(Spectra):
    implements(ISpectra)
    def __init__(self, project):
        self.set_project(project)

    def set_project(self, project):
        self.project = project
        self.get_spectra(self.project)
        self.scale = project.scale
        return project
        
    def get_spectra(self, project = None):
        def _c(x):
            return int(x)

        if project is None:
            project = self.project

        if project is None:
            return []
        
        # print self.source
        try:
            xml = project.get_xml()
        except ValueError:
            self.spectra = []
            return
        spectra = xml.xpath('//Channels/text()')
        spectra = [(map(_c, sp.split(',')), True) for sp in spectra]
        self.spectra = spectra

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

if __name__=='__main__':
    import sys
    print "ok"
    if len(sys.argv)==1:
        print 'Test run'
        test0('test.rtx')
    else:
        test0(sys.argv[1], spectrum=0)
    
