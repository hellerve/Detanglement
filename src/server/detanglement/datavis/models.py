from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Api(models.Model):
    api = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    needs_credentials = models.BooleanField()

    list_display = ('api', 'user', 'needs_creedentials')

    def __unicode__(self):
        return self.api


class ApiKey(models.Model):
    identification = models.ForeignKey(Api)
    authentication = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.identification


class Settings(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    geolocation = models.BooleanField(default=False)
    uses_map = models.CharField(choices=(("OSM", "Open Street Maps"),
                                         ("Google", "Google Maps"),
                                         ("Kartograph", "Kartograph")),
                                default='OSM', max_length=25)

    list_display = ('user', 'geolocation', 'uses_map')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = "Settings"
