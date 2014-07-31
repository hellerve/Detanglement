from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^accounts/?', include('registration.backends.default.urls')),
    url(r'^login/?', 'datavis.views.redir',
        {'site': '/accounts/login/'}),
    url(r'^[home]?$', 'datavis.views.serve',
        {'site': 'datavis/index.html'}),
    url(r'^settings/?', 'datavis.views.serve',
        {'site': 'datavis/settings.html'}),
    url(r'^apis/?', 'datavis.views.serve', {'site': 'datavis/apis.html'}),
    url(r'^accounts/profile/?', 'datavis.views.profile'),
)
