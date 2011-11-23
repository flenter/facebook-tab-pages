# Create your views here.

from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, Http404
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.encoding import smart_str

from fb_tabs.models import AppTab

import base64
import hashlib
import hmac
import simplejson as json

class TabbedPageMixin(object):

    def get_correct_view(self, *args, **kwargs):
        tab = get_object_or_404(AppTab, app_info__slug = kwargs['app_slug'], slug = kwargs['tab_slug'])

        if not tab.is_published() or not tab.app_info.is_published():
            raise Http404

        self.tab = tab

        new_view = tab.tab_type.related_view

        from fb_tabs import tab_types

        real_view = tab_types.get_view(new_view)

        return real_view


class TabLandingView(TemplateView, TabbedPageMixin):

    def dispatch(self, request, *args, **kwargs):

        self.get_correct_view(request, *args, **kwargs)

        return super(TabLandingView, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):

        from django.conf import settings
        if settings.DEBUG == False:
            pass

        return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        signed_request = request.POST['signed_request']

        secret = self.tab.app_info.app_secret

        data = self.parse_signed_request(smart_str(signed_request), smart_str(secret))

        data_to_store = {
                'page_id': int(data['page']['id']),
                'liked': bool(data['page']['liked']),
                'locale': smart_str(data['user']['locale']),
                'country': smart_str(data['user']['country']),
                }

        if unicode(data_to_store['page_id']) != self.tab.page_id:
            raise Http404

        from uuid import uuid4

        from django.core.cache import cache
        import marshal

        uid = uuid4()

        cache.set(uid.get_hex(), marshal.dumps(data_to_store))

        new_kwargs = kwargs.copy()
        new_kwargs['user_uid'] = uid.get_hex()

        return HttpResponseRedirect(reverse('fb_tabs.TabView', args=args, kwargs=new_kwargs))

        return HttpResponseBadRequest()

    def base64_url_decode(self, inp):
        padding_factor = (4 - len(inp) % 4) % 4
        inp += "="*padding_factor
        return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

    def parse_signed_request(self, signed_request, secret):

        l = signed_request.split(u'.', 2)

        encoded_sig = l[0]
        payload = l[1]

        sig = self.base64_url_decode(encoded_sig)
        data = json.loads(self.base64_url_decode(payload))

        if data.get('algorithm').upper() != 'HMAC-SHA256':
            return None
        else:
            expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

            if sig != expected_sig:
                return None
            else:
                return data


class TabView(TemplateView, TabbedPageMixin):

    template_name = 'fb_tabs/index.html'

    def get_correct_view(self, *args, **kwargs):
        view = super(TabView, self).get_correct_view(*args, **kwargs)

        user_uid = kwargs['user_uid']

        from django.core.cache import cache

        data = cache.get(user_uid)

        import marshal

        loaded_data = marshal.loads(data)

        if unicode(loaded_data['page_id']) != self.tab.page_id:
            raise Http404

        self.loaded_data = loaded_data

        return view

    def dispatch(self, request, *args, **kwargs):

        real_view = self.get_correct_view(request, *args, **kwargs)

        if issubclass(real_view, View):
            instance = real_view.as_view()
            kwargs['local_data'] = self.loaded_data
            kwargs['tab'] = self.tab
            return instance(request, *args, **kwargs)

        return super(TabView, self).dispatch(request, *args, **kwargs)


from fb_tabs import autodiscover

autodiscover()
