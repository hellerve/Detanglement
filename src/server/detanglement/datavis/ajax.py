from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

import pygeoip
from geopy import exc, distance
from geopy.point import Point
from geopy.geocoders import GeoNames

@dajaxice_register
def geolocate(request):
    dajax = Dajax()
    g = pygeoipGeoIP('static/rc/GeoLiteCity.dat', pygeoip.GEOIP_STANDARD)
    ip = request.META.get('REMOTE_ADDR', None)
    if ip:
        dajax.add_data(list(g.record_by_addr(ip).split()), 'addLocationMarker')
    return dajax.json()

@dajaxice_register
def locate(request, country, city):
    dajax = Dajax()
    g = GeoNames(None, "veitheller")
    place, (lat, lon) = g.geocode(str(city) + ", " + str(country))
    dajax.add_data([lat, lon], 'addLocationMarker')
    return dajax.json()
