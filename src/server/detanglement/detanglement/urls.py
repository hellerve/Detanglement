from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

def login():
    return redirect('/accounts/login/')

def profile():
    return PermissionDenied()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^login/?', 'datavis.views.auth_check',
        {'fun': login}),
    url(r'^accounts/?', include('registration.backends.default.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', 'datavis.views.serve', {'site': 'datavis/index.html'}),
    url(r'^home/?$', 'datavis.views.serve',
        {'site': 'datavis/index.html'}),
    url(r'^settings/?', 'datavis.views.serve',
        {'site': 'datavis/settings.html'}),
    url(r'^apis/?', 'datavis.views.serve', {'site': 'datavis/apis.html'}),
    url(r'^accounts/profile/?', 'datavis.views.auth_check',
        {'fun': profile}),
)

urlpatterns += staticfiles_urlpatterns()
