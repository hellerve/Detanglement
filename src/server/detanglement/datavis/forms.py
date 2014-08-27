from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.template import loader
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite, Site

from .models import Api, Settings


class ContactForm(forms.Form):
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        super(ContactForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request

    name = forms.CharField(max_length=100,
                           label=u'Your name')
    email = forms.EmailField(max_length=200,
                             label=u'Your email address')
    body = forms.CharField(widget=forms.Textarea,
                            max_length=1000,
                              label=u'Your message')

    from_email = settings.DEFAULT_FROM_EMAIL

    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

    subject_template_name = "contact/subject.txt"

    template_name = 'contact/body.txt'

    def message(self):
        if callable(self.template_name):
            template_name = self.template_name()
        else:
            template_name = self.template_name
        return loader.render_to_string(template_name,
                                       self.get_context())

    def subject(self):
        subject = loader.render_to_string(self.subject_template_name,
                                          self.get_context())
        return ''.join(subject.splitlines())

    def get_context(self):
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(self.request)
        return RequestContext(self.request,
                              dict(self.cleaned_data,
                                   site=site))

    def get_message_dict(self):
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")
        message_dict = {}
        for message_part in ('from_email', 'message', 'recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = attr() if callable(attr) else attr
        return message_dict

    def save(self, fail_silently=False):
        send_mail(fail_silently=fail_silently, **self.get_message_dict())


class SettingsForm(forms.Form):
    privacy = forms.BooleanField(required=False)
    display = forms.ChoiceField(choices=(("OSM", "Open Street Maps"),
                                        ("Google", "Google Maps"),
                                        ("Kartograph", "Kartograph")),
                                required=False)
    apis = forms.MultipleChoiceField(choices=(), required=False)
    email = forms.EmailField(max_length=200, label="New email address",
                            required=False)
    email_sec = forms.EmailField(max_length=200, label="Retype email address",
                                required=False)

    def __init__(self, request):
        if request.method == 'GET':
            super(SettingsForm, self).__init__()
            choices = []
            for api in Api.objects.all():
                if str(request.user) == str(getattr(api, 'user')):
                    choices.append((getattr(api, 'api'), getattr(api, 'api')),)
            self.fields['apis'].choices = choices
            settings = Settings.objects.get(user=request.user)
            if settings.geolocation:
                self.fields['privacy'].initial = True
            self.fields['display'].initial = settings.uses_map
        if request.method == 'POST':
            super(SettingsForm, self).__init__()
            settings = Settings.objects.get(user=request.user)
            if request.POST.get('privacy', 'off') == 'on':
                settings.geolocation = True
                self.fields['privacy'].initial = True
            else:
                settings.geolocation = False
            settings.uses_map = request.POST.get('display', 'OSM')
            self.fields['display'].initial = settings.uses_map
            settings.save()
            email = request.POST.get('email', None)
            email_sec = request.POST.get('email_sec', None)
            print(email, email_sec)
            if email != email_sec:
                return None
            user = User.objects.get(username=request.user)
            user.email = email
            user.save()

