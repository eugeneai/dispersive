
from zope.interface import Interface
from zope import schema
from zope.configuration import fields, xmlconfig


class IRegisterModule(Interface):
    
    factory = fields.GlobalObject(
        title=u"Module factory",
        description=u"This is the factory of the module."
        )

    src=fields.Path(
        title=u"R module source path",
        description=u"This is the path name of the corresponding R module to be associated with registered module.",
        required = True
        )

    lang = schema.Text(
        title=u"Language of the module",
        description=u"Implementation language of the module",
        required = True
        )

    func = schema.Text(
        title=u"Short summary of the module",
        description=u"This will be used in module list",
        required = True
        )


    title = schema.Text(
        title=u"Short summary of the module",
        description=u"This will be used in module list",
        required = True
        )

    category = schema.Text(
        title=u"Short summary of the module",
        description=u"This will be used in module list",
        required = True
        )

    description = schema.Text(
        title=u"Long Description of the module",
        description=u"This will be used, e.g., as help messages",
        required = False
        )

    icon = fields.Path(
        title=u"Path to the icon file .svf",
        description=u"Icon, depicting the module in all the graphics interfaces.",
        required = False
        )

    
