==================
facebook-tab-pages
==================

A system that allows to assign a certain app/tab to a view. Created as our/my 
own extendable variant of the statichtml site. It was important to be able to 
create forms and stuff like that.

The application contains two apps:
fb_tabs (the core)
tb_static (an example app that allows static pages to be displayed, and displays different content if a user has liked the person/group/company etc on facebook)

============
installation
============

You will need to add ``fb_tabs`` and/or ``fb_static``. to your ``INSTALLED_APPS``::

    INSTALLED_APPS = {
        'fb_tabs',
        'fb_static',
    }

Run ``python manage.py syncdb`` in your application's directory to create the tables.

Finally don't forget to include fb_tabs.urls in your urls.py. 


===================
Extending the views
===================
Right now only class based views are supported and will have to be registered like this::

    from django.views.generic import Templateview

    class MyCustomView(TemplateView):
        template_name = 'some/template.html'


    from fb_tabs import tab_types
    tab_types.register(MyCustomView)


