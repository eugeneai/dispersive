#!/bin/env python
from icc.rake.modules.interfaces import *
from icc.rake.modules.components import *
from icc.rake.models.components import Module, OrderedDict
import zope.component.factory as zope_factory
from zope.component import getGlobalSiteManager, getUtility
from zope.component.interfaces import IFactory
from zope.interface import implements

class ModuleRegistry(object):
    implements(IModuleRegistry)
    def __init__(self):
        self.categories=OrderedDict()
        self.tree=OrderedDict()
        self.modules=OrderedDict()

module_registry=ModuleRegistry()

class Factory(zope_factory.Factory):
    def __call__(self, *args, **kwargs):
        c=self._callable
        obj = c(*args, **kwargs)
        obj.name=c.name
        obj.title=self.title
        obj.description=''
        return obj

def registerModuleFactory(f):
    name=f._callable.name
    module_registry=getUtility(IModuleRegistry)
    cat=module_registry.categories[f.category]
    cat.modules[name]=f
    module_registry.modules[name]=f

    # Taken from ZCA
    gsm = getGlobalSiteManager()
    gsm.registerUtility(f, IFactory, name)

class Category(object):
    pass

def _registerCategory(name, title, icon, description, category):
    m_r=getUtility(IModuleRegistry)
    cat=Category()
    cat.name=name
    cat.icon=icon
    cat.title=title
    cat.description=description
    cat.cats=OrderedDict()
    cat.modules=OrderedDict()
    m_r.categories[name]=cat
    if category != None:
        parent = m_r.categories[category]
        parent.cats[name]=cat
    else:
        m_r.tree[name]=cat

def registerModule(context, name, factory, title, func, src, lang, category, icon=None, description='', inputs='{}', outputs='{}'
                   ):
    f=Factory(factory, title, description)
    factory.name=name
    factory.src=src
    factory.lang=lang
    factory.func=func
    factory.icon=icon
    f.category=category
    factory.inputs=OrderedDict(eval(inputs))
    factory.outputs=OrderedDict(eval(outputs))

    context.action(discriminator=('RegisterModule', src, func),
                   callable=registerModuleFactory,
                   args=(f,)
                   )

def registerCategory(context, name, title, icon, description='', category=None):
    context.action(discriminator=('RegisterCategory', name),
                   callable=_registerCategory,
                   args=(name, title, icon, description, category)
                   )


def get_module_registry():
    return module_registry

if __name__=="__main__":
    print "Engine to run mofule configuration."
