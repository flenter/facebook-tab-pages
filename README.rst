==================
facebook-tab-pages
==================

A system that allows to assign a certain app/tab to a view. Created as our/my 
own extendable variant of the statichtml site. It was important to be able to 
create forms and stuff like that.

The application contains two apps:

* fb_tabs (the core)
* tb_static (an example app that allows static pages to be displayed, and displays different content if a user has liked the person/group/company etc on facebook)


------------
installation
------------

You will need to add ``scm_core`` (see `django-scm_core`_) ``fb_tabs`` and/or ``fb_static``. to your ``INSTALLED_APPS``::

    INSTALLED_APPS = {
        'fb_tabs',
        'fb_static',
    }
Configure django's caching backend. This is used to store the information from the signed_request paramter send by facebook.

Run ``python manage.py syncdb`` in your application's directory to create the tables.

Finally don't forget to include fb_tabs.urls in your urls.py. For instance::

    urlpatterns = patterns('', 
        url('^tabs/', include('fb_tabs.urls')),
        )

------------
How it works
------------

First of all, what of information does this app store? Well, there are only 3 models:

* Tab Type. This holds a readable description of each django view you want to expose. So if fb_static is installed it holds:fb_static.views.StaticView
* Application Info. Most importantly, this holds the app_id and secret and has a slug to make it more easily accessible
* App Tab. This is the page/tab that is linked to both an application info item and a tab type. It also has a slug to make it once again easier to remember.

How to create a nice tab? Here's how (assuming you've already created tab types):

1. Create an Application Info item in the admin. You don't need to fill in the app_id or app_secret. Just keep them at 0, later the python code will display some forms if the values are 0. Remember the slug for the application.
2. Create an AppTab. You don't need to fill in the page id yet. Later in the process you wll be asked for this. Remember the slug for this model too
3. Remember your tab's url. It is constructed like this: ``domain.com/tabs/{{application_slug}}/{{tab_slug}}/``
4. Make an application on facebook at http://facebook.com/developers/ and fill in the preferred urls (see step 3 for the url on your django website)
5. With a browser that is logged in as a staff member on your django site, go to facebook and load the tab. Fill in the form asking for the apps id and secret (after saving you get an empty page)
6. Reload the page. the page_id will be taken from the facebook signed_request. After saving you should see the right view!


-------------------
Extending the views
-------------------
With this project, only one class based view is bundled. But adding one is easy, have a (class based view) registered like this::

    from django.views.generic import Templateview

    class MyCustomView(TemplateView):
        template_name = 'some/template.html'


    from fb_tabs import tab_types
    tab_types.register(MyCustomView)

.. _`django-scm_core`: http://bitbucket.org/flenter/django-scm_core/
