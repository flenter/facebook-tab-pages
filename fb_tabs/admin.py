from django.contrib import admin

from fb_tabs.models import ApplicationInfo, AppTab, TabType

admin.site.register(ApplicationInfo)
admin.site.register(AppTab)
admin.site.register(TabType)
