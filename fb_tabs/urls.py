from django.conf.urls.defaults import patterns, url

from django.views.decorators.csrf import csrf_exempt

from fb_tabs.views import TabView, TabLandingView

urlpatterns = patterns('',
        url('^(?P<app_slug>[\w\-]+)/(?P<tab_slug>[\w\-]+)/(?P<user_uid>.*)/$', TabView.as_view(), name="fb_tabs.TabView"),
        url('^(?P<app_slug>[\w\-]+)/(?P<tab_slug>[\w\-]+)/$', csrf_exempt(TabLandingView.as_view()), name="fb_tabs.TabLandingView"),
)
