#!/usr/bin/python
from lxml import etree
import subprocess as sp


TMP_DIR='/tmp'

class Spectrums(object):
    def __init__(self, source):
        self.source = source
        if source.lstrip().startswith('<?'):
            raise RuntimeError('Not implemented')
        self.xml=self.channels=None
        self.load(open(self.source))
        
    def load(self, source):
        self.xml= etree.parse(source)

    def get_channels(self):
        def _c(x):
            return int(x)
        
        channels = self.xml.xpath('//Channels/text()')
        channels = [map(_c, ch.split(',')) for ch in channels]
        self.channels = channels
        if self.channels:
            self.ch_len = len(self.channels[0])
        else:
            self.ch_len = None

    def r_vect(self, channel, name):
        return '%s = c(%s)\n' % (name, ','.join(map(str, channel)))
        
    
    def r_plot(self, func = '',type_='l'):
        if self.channels is None:
            self.get_channels()
        tmp_file = self._get_tmp('R')
        o=open(tmp_file,'w')
        o.write('# Automatically generated, do not edit\n\n')
        o.write(PLOT_PREAMBLE)
        o.write(self.r_vect(range(self.ch_len), 'X'))
        i = 0
        names = []
        for ch in self.channels:
            i+=1
            name = 'chan%i' % i
            o.write(self.r_vect(ch, name))
            names.append(name)

        o.write('chan_plot=function() {\n')
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
        o.write('} # chan_plot\n\n')
        o.write(PLOT_POSTAMBLE)
        o.close()
        p=sp.Popen(['R', '--no-save'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=None)
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
chan_plot()
lines(X,G, type='l')
dev.off()
"""
        

def test0(filename):
    ss = Spectrums(filename)
    ss.r_plot(func='')
    print 'Channel length:', len(ss.channels[0])
    print 'Channel count:', len(ss.channels)

if __name__=='__main__':
    import sys
    print "ok"
    if len(sys.argv)==1:
        print 'Test run'
        test0('test.rtx')
    else:
        test0(sys.argv[1])
    
