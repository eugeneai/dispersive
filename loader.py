#!/usr/bin/python
from lxml import etree
import subprocess as spp


TMP_DIR='/tmp'

class Spectrums(object):
    def __init__(self, source):
        self.source = source
        if source.lstrip().startswith('<?'):
            raise RuntimeError('Not implemented')
        self.xml=self.spectra=None
        self.load(open(self.source))
        
    def load(self, source):
        self.xml= etree.parse(source)

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
                o.write("plot(x=X, y=%s, type='%s', col=cols[%i])\n" % (Y, type_, ci))
                first = False
            else:
                o.write("lines(x=X, y=%s, col=cols[%i], type='%s')\n" % (Y, ci, type_))
            ci+=1
        o.write('} # plot.spectra\n\n')
        o.write(PLOT_POSTAMBLE)
        o.close()
        p=spp.Popen(['R', '--no-save'], stdin=spp.PIPE, stdout=spp.PIPE, stderr=None)
        out,err = p.communicate(PLOT_CMD % tmp_file)
        print out,err
        

    def _get_tmp(self, ext):
        return TMP_DIR+'/temp.'+ext

PLOT_CMD='''
source('%s')
quit(save='no')
'''

PLOT_PREAMBLE='''source('global.R')

cols=colors()
'''

PLOT_POSTAMBLE="""
G = gauss(X, l5_9, 2000000, sc=sc)
postscript(file='plot.eps')
plot.spectra()
lines(X,G, type='l')
dev.off()
"""
        

def test0(filename, spectrum=None):
    ss = Spectrums(filename)
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
    
