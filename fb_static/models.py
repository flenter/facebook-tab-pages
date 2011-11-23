from django.db import models

# Create your models here.

from fb_tabs.models import AppTab
from scm_core.models import PublishItem

class StaticPage(PublishItem):
    tab = models.ForeignKey(AppTab)

    content = models.TextField()
    fan_content = models.TextField()

