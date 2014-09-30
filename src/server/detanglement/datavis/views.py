from django.conf import settings
from django.shortcuts import redirect, render
from django.forms.util import ErrorList
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.views.decorators.cache import cache_page

from .forms import ContactForm, SettingsForm, PasswordForm


# @cache_page(60 * 10)
def serve(request, site, auth=True):
    if not auth or request.user.is_authenticated():
        return render(request, site)
    return redirect('/login/')


def redir(request, site):
    return redirect(site)


def auth_check(request, fun):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('/home/')
    return fun()


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'

    def form_valid(self, form):
        form.save()
        return super(ContactFormView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ContactFormView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        return reverse('sent')


# @cache_page(60 * 10)
def settings(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    form = SettingsForm(request)
    if request.method == "POST":
        if form.is_valid():
            return redirect("/settings/success")
        else:
            form.full_clean()
            form._errors['email'] = ErrorList(['The email fields ' +
                                               'did not match'])
    return render(request, 'datavis/settings.html', {'form': form})


def password_change(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    form = PasswordForm(request)
    if request.method == "POST":
        if form.is_valid():
            return redirect("/settings/success")
        else:
            form.full_clean()
            form._errors['password'] = ErrorList(['The password fields ' +
                                                  'did not match'])
    return render(request, 'datavis/password_change.html', {'form': form})
