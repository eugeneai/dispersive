#!/usr/bin/python
"""Module for modelling Energy Dispersive XRF Analysis.
"""
from lxml import etree
import subprocess as spp
import os, os.path
from zope.interface import implements
from interfaces import *

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
    """Set of spectra with the same Energy axis scale (x-axis)
    """
    def __init__(self, source, scale=None):
        self.source = source
        if scale is None:
            self.set_scale(scale_none)
        else:
            self.set_scale(scale)
            
        if source.lstrip().startswith('<?'):
            raise RuntimeError('Not implemented')
        self.xml=self.spectra=None
        self.load(open(self.source))
        
    def load(self, source):
        self.xml= etree.parse(source)

    def set_scale(self, scale):
        self.scale=scale

    def get_spectra(self):
        def _c(x):
            return int(x)
        
        spectra = self.xml.xpath('//Channels/text()')
        spectra = [map(_c, sp.split(',')) for sp in spectra]
        self.spectra = spectra
        if self.spectra:
            self.ch_len = len(self.spectra[0])
        else:
            self.ch_len = None

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
    
