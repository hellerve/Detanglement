from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Api(models.Model):
    api = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.api

class ApiKey(models.Model):
    identification = models.ForeignKey(Api)
    authentication = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.authentication
