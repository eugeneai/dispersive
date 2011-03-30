from icc.rake.models.components import Module, OrderedDict


class FrameLoadModule(Module):
    outputs=OrderedDict(data = ('data.frame',))
    icon='ui/pics/frame_open.svg'
    name='Data Frame Loading' 


class FrameViewModule(Module):
    inputs=OrderedDict(data = ('data.frame',))
    icon='ui/pics/frame_view.svg'
    name='Data Frame Viewing'


class LmModule(Module):
    pass

class PlotModule(Module):
    inputs=OrderedDict(x = ('',), y=('',))
    outputs=OrderedDict()
    icon='ui/pics/plot.svg'
    name='Plot (anything)'

