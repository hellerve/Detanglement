import random

from django.conf import settings as preferences
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

import pygeoip
from geopy import exc, distance
from geopy.point import Point
from geopy.geocoders import GeoNames

from .models import Settings, Api
from .plugins.APIInterface import APIInterface

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
    objects = []
    plugindir = os.listdir(path + "/src/plugins")
    apis = Api.objects.filter(user=request.user)
    if not apis:
        error = "'Could not load API " + api + ". No API selected.'"
        dajax.script("toastr.warning(" + error + ", 'API warning')")
        return dajax.json()
    for api in apis:
        if not api + ".py" in plugindir:
            error = "'Could not load API " + api + ". No such API.'"
            dajax.script("toastr.error(" + error + ", 'API error')")
        credentials = ApiKey.objects.get(identification=api)
        if not credentials:
            error = "'Could not load API " + api + ". No credentials.'"
            dajax.script("toastr.error(" + error + ", 'API error')")
            continue
        impobj = getattr(__import__("plugins", fromlist=[api]), api)
        objects.append(APIInterface(api, impobj,
                credentials.authentication))
    return dajax.json()

@dajaxice_register
def load(request):
    dajax = Dajax()
    script = "markers = ["
    for i in range(100):
        script += ("[" + str(random.randrange(-180.0, 180.0)) + ", "  +
                str(random.randrange(-180.0, 180.0)) + ", 'test" +
                str(i) + "'],")
    script = script[:-1] + script[-1:].replace(",","]")
    dajax.script(script)
    return dajax.json()

@dajaxice_register
def visualize_location_trends(request, lat, lon):
    return
