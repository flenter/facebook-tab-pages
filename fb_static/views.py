# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from fb_static.models import StaticPage

class StaticView(TemplateView):
    template_name = "fb_static/index.html"

    def get_context_data(self, *args, **kwargs):

        context = super(StaticView, self).get_context_data(*args, **kwargs)

        context['local_data'] = self.kwargs.get('local_data', None)
        context['content'] = self.kwargs.get('tab', None)

        content = get_object_or_404(StaticPage, tab=context['content'])

        context['content'] = content

        print context['local_data']
        print self.kwargs

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

print "...."
from fb_tabs import tab_types
tab_types.register(StaticView)

def test_method(self):
    pass
