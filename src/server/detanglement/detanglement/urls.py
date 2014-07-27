from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/?', 'django.contrib.auth.views.login',
        {'template_name': 'authentication/login.html',
        'redirect_field_name': 'datavis/index.html',
        'current_app': 'Detanglement'}),
    url(r'^[home]?$', 'datavis.views.serve',
        {'site': 'datavis/index.html'}),
    url(r'^settings/$', 'datavis.views.serve',
        {'site': 'datavis/settings.html'}),
    url(r'^apis/$', 'datavis.views.serve', {'site': 'datavis/apis.html'}),
    url(r'^accounts/profile/$', 'datavis.views.profile'),
)
