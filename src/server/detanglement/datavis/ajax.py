from django.conf import settings as preferences
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

import pygeoip
from geopy import exc, distance
from geopy.point import Point
from geopy.geocoders import GeoNames

from .models import Settings, Api

@dajaxice_register
def geolocate(request):
    dajax = Dajax()
    g = pygeoip.GeoIP(preferences.BASE_DIR + '/static/rc/GeoLiteCity.dat')
    ip = request.META.get('REMOTE_ADDR', None)
    if ip:
        if ip == '127.0.0.1':
            ip = '141.45.146.48'
        data = g.record_by_addr(ip)
        dajax.add_data([round(data['latitude'], 2),
                        round(data['longitude'], 2)],
                        'addLocationMarker')
    return dajax.json()

@dajaxice_register
def locate(request, country, city):
    dajax = Dajax()
    g = GeoNames(None, "veitheller")
    place, (lat, lon) = g.geocode(str(city) + ", " + str(country))
    dajax.add_data([lat, lon], 'addLocationMarker')
    return dajax.json()

@dajaxice_register
def settings(request):
    dajax = Dajax()
    m = Settings.objects.get(user=request.user)
    if m == None:
        m = Settings.objects.create_settings(user=request.user,
                                            uses_map="OSM",
                                            geolocation=False)
        m.save()
    if m.uses_map == "Google":
        dajax.script("tangle.mapchoice = 0")
    elif m.uses_map == "Kartograph":
        dajax.script("tangle.mapchoice = 1")
    elif m.uses_map == "OSM":
        dajax.script("tangle.mapchoice = 2")
    if m.geolocation == True:
        dajax.script("tangle.geolocation = true")
    else:
        dajax.script("tangle.geolocation = false")
    return dajax.json()

@dajaxice_register
def visualize(request):
    dajax = Dajax()
    apis= []
    for api in Api.objects.all():
        if str(request.user) == str(getattr(api, 'user')):
            apis.append(getattr(api, 'api'))
    if not apis:
        return dajax.json()
    for api in apis:
        # get location for api and add a marker
        continue
    return dajax.json()

@dajaxice_register
def count_items(request):
    dajax = Dajax()
    dajax.script("max = 400")
    return dajax.json()
