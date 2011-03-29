#!/bin/env python
from icc.rake.modules.interfaces import *
from icc.rake.modules.components import *

module_registry = []

def registerModule(context, factory, title, func, src, lang, category, icon=None, description='',
                   ):
    m=factory()
    m.title=title
    m.src=src
    m.lang=lang
    m.func=func
    m.icon=icon
    m.description=description
    m.category=category

    context.action(discriminator=('RegisterModule', src, func),
                   callable=module_registry.append,
                   args=(m,)
                   )

def get_module_registry():
    return module_registry

if __name__=="__main__":
    print "Engine to run mofule configuration."
