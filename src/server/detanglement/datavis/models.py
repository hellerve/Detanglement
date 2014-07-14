from django.db import models
from django.core.urlresolvers import reverse

class Api(models.Model):
    api = models.CharField(max_length=255)

    def __unicode__(self):
        return self.api

class Authentication(models.Model):
    identification = models.ForeignKey(Api)
    authentication = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.authentication
