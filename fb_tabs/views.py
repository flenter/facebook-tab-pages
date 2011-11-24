# Create your views here.

from django.views.generic import TemplateView, View
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404, Http404
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.encoding import smart_str

from fb_tabs.models import AppTab, ApplicationInfo
from fb_tabs.forms import AppTabForm, ApplicationInfoForm

import base64
import hashlib
import hmac
import simplejson as json

class TabbedPageMixin(object):
    """ Mixin implementing the get_correct_view method. This checks for publish state yes/no and such.
    It returns the related view as set in the database (or none if the view is not valid anymore"""

    def get_correct_view(self, request, *args, **kwargs):
        query_kwargs = {
                'app_info__slug': kwargs['app_slug'],
                'slug': kwargs['tab_slug'],
                }

        tab = get_object_or_404(AppTab, **query_kwargs)
        self.tab = tab

        if not tab.is_published() or not tab.app_info.is_published():
            print "not published"
            raise Http404

        new_view = tab.tab_type.related_view

        from fb_tabs import tab_types

        return tab_types.get_view(new_view)


class TabLandingView(TemplateView, TabbedPageMixin):
    """Initial view that handles retrieving the signed_request data and after that redirects to the TabView view
    There's already a start of some implemtation to test the applicaiton outside of facebook. But that has not 
    been fully implemented yet.
    """

    def dispatch(self, request, *args, **kwargs):

        try:
            self.get_correct_view(request, *args, **kwargs)
        except Http404, e:
            print request.user.is_staff
            if not request.user.is_staff:
                raise

        return super(TabLandingView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        from django.conf import settings
        if settings.DEBUG == False:
            pass

        return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):

        from uuid import uuid4
        from django.core.cache import cache
        import marshal

        signed_request = request.POST.get('signed_request', None)

        secret = self.tab.app_info.app_secret

        data = None
        if signed_request:
            data = self.parse_signed_request(smart_str(signed_request), smart_str(secret))

        if data:
            data_to_store = {
                    'page_id': int(data['page']['id']),
                    'liked': bool(data['page']['liked']),
                    'locale': smart_str(data['user']['locale']),
                    'country': smart_str(data['user']['country']),
                    }

            uid = uuid4()

            cache.set(uid.get_hex(), marshal.dumps(data_to_store))

            new_kwargs = kwargs.copy()
            new_kwargs['user_uid'] = uid.get_hex()

        if request.user.is_staff:
            if signed_request:
                request.method = "GET"


            print "self.tab.page_id", self.tab.page_id

            if (self.tab.app_info.app_id == '0' or self.tab.app_info.app_secret == '0'):

                new_kwargs = {'slug': kwargs['app_slug']}
                return EditAppView.as_view()(request, **new_kwargs)

            elif (self.tab.page_id == '0'):

                new_kwargs = {'slug': kwargs['tab_slug']}

                if data:
                    instance = EditTabView.as_view(page_id=data_to_store['page_id'], user_uid=uid.get_hex())
                else:
                    instance = EditTabView.as_view()
                return instance(request, **new_kwargs)

        if not signed_request:
            # raise a 404 when there's a post to this page without a nice signed_request parameter
            raise Http404

        if unicode(data_to_store['page_id']) != self.tab.page_id:
            raise Http404


        if data == None:
            raise Http404

        return HttpResponseRedirect(reverse('fb_tabs.TabView', args=args, kwargs=new_kwargs))

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

    """ The core view of the app, it calls the associated view with some additional parameters"""

    template_name = 'fb_tabs/index.html'

    def get_stored_data(self, user_uid):

        from django.core.cache import cache
        import marshal

        data = cache.get(user_uid)

        if not(data):
            raise Http404

        loaded_data = marshal.loads(data)

        return loaded_data

    def validate_url_data(self, loaded_data):

        if unicode(loaded_data['page_id']) != self.tab.page_id:
            raise Http404

        data_tab = get_object_or_404(AppTab, page_id = loaded_data['page_id'])

        if data_tab.app_info.pk != self.tab.app_info.pk:
            raise Http404

        return True

    def dispatch(self, request, *args, **kwargs):

        real_view = self.get_correct_view(request, *args, **kwargs)

        self.loaded_data = self.get_stored_data(kwargs['user_uid'])

        if self.validate_url_data(self.loaded_data):

            if issubclass(real_view, View):

                instance = real_view.as_view()
                kwargs['local_data'] = self.loaded_data
                kwargs['tab'] = self.tab
                print dir(instance)

                return instance(request, *args, **kwargs)

        return super(TabView, self).dispatch(request, *args, **kwargs)


class EditAppView(UpdateView):
    model = ApplicationInfo

    form_class = ApplicationInfoForm

    def get_success_url(self):
        return self.request.get_full_path()


class EditTabView(UpdateView):
    model = AppTab
    form_class = AppTabForm
    page_id = ''
    user_uid = ''

    def get_initial(self):
        return {'user_uid': self.user_uid}

    def get_form_kwargs(self, *args, **kwargs):
        data = super(EditTabView, self).get_form_kwargs(*args, **kwargs)
        data['instance'].page_id = self.page_id

        return data

    def get_success_url(self):
        form = self.get_form(self.get_form_class())
        form.is_valid()
        return '%s%s/' % (self.request.get_full_path(), form.cleaned_data['user_uid'])


from fb_tabs import autodiscover
autodiscover()
