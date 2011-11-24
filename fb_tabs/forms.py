from django import forms

from fb_tabs.models import ApplicationInfo, AppTab

class ApplicationInfoForm(forms.ModelForm):

    class Meta:
        model = ApplicationInfo
        fields = ('app_id', 'app_secret',)

    def clean(self, *args, **kwargs):

        return super(ApplicationInfoForm, self).clean(*args, **kwargs)

class AppTabForm(forms.ModelForm):

    class Meta:
        model = AppTab
        fields = ('page_id',)

    def clean(self):
        values = super(AppTabForm, self).clean()

        return values

