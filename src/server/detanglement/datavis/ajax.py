from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

import pygeoip
from geopy import exc, distance
from geopy.point import Point
from geopy.geocoders import GeoNames

from .models import Settings

@dajaxice_register
def geolocate(request):
    dajax = Dajax()
    g = pygeoipGeoIP('static/rc/GeoLiteCity.dat', pygeoip.GEOIP_STANDARD)
    ip = request.META.get('REMOTE_ADDR', None)
    if ip:
        dajax.add_data(list(g.record_by_addr(ip).split()),
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
def mapchoice(request):
    dajax = Dajax()
    m = Settings.objects.get(username=request.user).get('uses_map', None)
    if m == "Google":
        dajax.script("tangle.mapchoice = 0")
    elif m == "OSM":
        dajax.script("tangle.mapchoice = 0")
    elif m == "Kartograph":
        dajax.script("tangle.mapchoice = 0")
    return dajax.json()

@dajax_register
def refresh():
    dajax = Dajax()
    dajax.script("load();")
    return dajax.json()

@dajax_register
def visualize(request):
    dajax = Dajax()
    apis = Settings.objects.get(username=request.user).get('apis', None)
    if m == None:
        return dajax.json()
    for api in apis:
        # get location for api and add a marker
        pass
    return dajax.json()
