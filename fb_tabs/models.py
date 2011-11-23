from django.db import models
from django.utils.functional import lazy

from django.core.urlresolvers import reverse

# Create your models here.

from core.models import PublishItem

class ApplicationInfo(PublishItem):
    title = models.CharField(max_length = 100)
    slug = models.SlugField()
    app_id = models.CharField(max_length = 25)
    app_secret = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.title

def get_view_types():
    from fb_tabs import tab_types

    types = [(name, name) for name in tab_types.get_view_names()]
    return types


class TabType(PublishItem):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    related_view = models.CharField(max_length = 255)#, choices=lazy(get_view_types, list)())#, choices=lazy(get_view_types))

    def __init__(self, *args, **kwargs):
        super(TabType, self).__init__(*args, **kwargs)

        self._meta.get_field_by_name('related_view')[0]._choices = lazy(get_view_types, list)()

    def __unicode__(self):
        return self.title

class AppTab(PublishItem):
    app_info = models.ForeignKey(ApplicationInfo)
    tab_type = models.ForeignKey(TabType)
    page_id = models.CharField(max_length = 100)
    title = models.CharField(max_length =100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('fb_tabs.TabView', kwargs={'tab_slug': self.slug, 'app_slug': self.app_info.slug})
