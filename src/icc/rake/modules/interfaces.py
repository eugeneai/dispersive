
from zope.interface import Interface
from zope.configuration import fields, xmlconfig


def IRegisterModule(Interface):
    
    factory = fields.GlobalObject(
        title=u"Module factory",
        description=u"This is the factory of the module."
        )

    source=fields.Path(
        title=u"R module source path",
        description=u"This is the path name of the corresponding R module to be associated with registered module.",
        required = False
        )

    title = schema.Text(
        title=u"Short summary of the module",
        description=u"This will be used in module list",
        required = True
        )

    icon = fields.Path(
        title=u"Path to the icon file .svf",
        description=u"Icon, depicting the module in all the graphics interfaces.",
        required = False
        )

    
