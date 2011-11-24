__version__ = (0, 1, 2)

class TabTypeAdmin:
    def __init__(self):
        self._registry = {}

    def register(self, view, name=None):
        if not name:
            name = "%s.%s" % (view.__module__, view.__name__)

        self._registry[name] = view

    def get_view(self, name):
        return self._registry[name]

    def get_view_names(self):
        return self._registry.keys()

tab_types = TabTypeAdmin()

def autodiscover():
     """$
     Auto-discover code copied/modified django.admin
     """

     import copy
     from django.conf import settings
     from django.utils.importlib import import_module
     from django.utils.module_loading import module_has_submodule

     for app in settings.INSTALLED_APPS:
         mod = import_module(app)
         # Attempt to import the app's admin module.
         try:
             before_import_registry = copy.copy(tab_types._registry)
             import_module('%s.views' % app)
         except:
             # Reset the model registry to the state before the last import as$
             # this import will have to reoccur on the next request and this$
             # could raise NotRegistered and AlreadyRegistered exceptions$
             # (see #8245).
             tab_types._registry = before_import_registry

             # Decide whether to bubble up this error. If the app just
             # doesn't have an admin module, we can ignore the error
             # attempting to import it, otherwise we want it to bubble up.
             if module_has_submodule(mod, 'views'):
                 raise
