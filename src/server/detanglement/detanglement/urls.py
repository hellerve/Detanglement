from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from datavis.views import ContactFormView
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

admin.autodiscover()
dajaxice_autodiscover()


def login():
    return redirect('/accounts/login/')


def profile():
    return PermissionDenied()

urlpatterns = patterns('',
                       url(r'^admin/?', include(admin.site.urls)),
                       url(r'^login/$', 'datavis.views.auth_check',
                           {'fun': login}),
                       url(r'^help/?$', 'datavis.views.serve',
                           {'site': 'datavis/help.html'}),
                       url(r'^imprint/?$', 'datavis.views.serve',
                           {'site': 'datavis/imprint.html', 'auth': False}),
                       url(r'^accounts/?',
                           include('registration.backends.default.urls')),
                       url(r'^accounts/?',
                           include('django.contrib.auth.urls')),
                       url(r'^$', 'datavis.views.serve',
                           {'site': 'datavis/index.html'}),
                       url(r'^home/?$', 'datavis.views.serve',
                           {'site': 'datavis/index.html'}),
                       url(r'^settings/?$', 'datavis.views.settings'),
                       url(r'^passwordchange/?$',
                           'datavis.views.password_change'),
                       url(r'^settings/success/?$', 'datavis.views.serve',
                           {'site': 'datavis/settings_success.html'}),
                       url(r'^apis/$', 'datavis.views.serve',
                           {'site': 'datavis/apis.html'}),
                       url(r'^accounts/profile/?$', 'datavis.views.auth_check',
                           {'fun': profile}),
                       url(r'^contact/?$', ContactFormView.as_view(),
                           name='contact'),
                       url(r'^contact/sent/?$', 'datavis.views.serve',
                           {'site': 'contact/sent.html'}, name='sent'),
                       url(dajaxice_config.dajaxice_url,
                           include('dajaxice.urls')), )

urlpatterns += staticfiles_urlpatterns()
