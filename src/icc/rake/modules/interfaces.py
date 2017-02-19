
from zope.interface import Interface, Attribute
from zope import schema
from zope.configuration import fields, xmlconfig

class IRegisterCategory(Interface):
    name = schema.Text(
        title="Categoey name",
        description="An identifier of the category",
        required = True
        )

    title = schema.Text(
        title="Short summary of the category",
        description="This will be used in module tree",
        required = True
        )

    category = schema.Text(
        title="Parent category of the category",
        description="Category denotes classification of the modules",
        required = False
        )

    description = schema.Text(
        title="Long Description of the category",
        description="This will be used, e.g., as help messages",
        required = False
        )

    icon = fields.Path(
        title="Path to the icon file .svg",
        description="Icon, depicting the module in all the graphics interfaces.",
        required = False
        )
 

class IRegisterModule(Interface):
    
    factory = fields.GlobalObject(
        title="Module factory",
        description="This is the factory of the module."
        )
    
    src=fields.Path(
        title="R module source path",
        description="This is the path name of the corresponding R module to be associated with registered module.",
        required = True
        )

    name = schema.Text(
        title="Module name",
        description="Module global identifier, used, e.g. to declare module constructor as factory",
        required = True
        )
    lang = schema.Text(
        title="Language of the module",
        description="Implementation language of the module",
        required = True
        )

    func = schema.Text(
        title="Function that process data",
        description="Data processing function in the module",
        required = True
        )


    title = schema.Text(
        title="Short summary of the module",
        description="This will be used in module tree",
        required = True
        )

    category = schema.Text(
        title="Category of the module",
        description="Category denotes classification of the modules",
        required = True
        )

    description = schema.Text(
        title="Long Description of the module",
        description="This will be used, e.g., as help messages",
        required = False
        )

    icon = fields.Path(
        title="Path to the icon file .svg",
        description="Icon, depicting the module in all the graphics interfaces.",
        required = False
        )
 
    inputs = schema.Text(
        title="Input variables",
        description="Mapping of the input variable names to their types in the target language",
        required = False
        )

    outputs = schema.Text(
        title="Output variables",
        description="Mapping of the output variable names to their types in the target language",
        required = False
        )

class IModuleRegistry(Interface):
    categories=Attribute("Category hiererchy of the module factorues")
    modules=Attribute("List of all the module factories")
