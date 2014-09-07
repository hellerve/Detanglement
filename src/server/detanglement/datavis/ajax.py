import random
import os
import importlib

from django.conf import settings as preferences
from django.contrib.auth.models import User
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

import pygeoip
from geopy import exc, distance
from geopy.point import Point
from geopy.geocoders import GeoNames

from .models import Settings, Api, ApiKey
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
    m = Settings.objects.filter(user=User.objects.get(username=request.user))
    if not m:
        m = Settings(user=User.objects.get(username=request.user),
            uses_map="OSM", geolocation=False)
        m.save()
    else:
        m = m[0]
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
def visualize(request, location, fro, to, filters):
    dajax = Dajax()
    location = name.split(", ") if ", " in name else name
    data = []
    dajax.script("toastr.warning('Not implemented yet.', 'Visualization warning');")
    return dajax.json()
    for api in api_objects:
        if api.requiresFilter():
            dajax.script("askForFilter(" + api.filters + ")")
        else:
            make_graph()
            if filters:
                src = api.api_name
                req = {}
                for i in filters: pass
        locations = api.getLocations()
        #location = title.split(", ") if ", " in title else title
        #data = []
        #for api in self.apis:
        #    if api.requiresFilter():
        #        self._askForFilter(api)
        #        if self.filters:
        #            src = api.api_name
        #            req = {}
        #            for i in self.filters:
        #                if self.date:
        #                    x, t = api.getDataForLocation(location[0], i, self.date)
        #                else:
        #                    x, t = api.getDataForLocation(location[0], i)
        #                if not t:
        #                    self.web_view.warning("No datasets for filter " +
        #                            i + "!")
        #                else: req.update({k+'/'+i:v for k,v in t.items()})
        #        else:
        #            src, req = None, None
        #    else:
        #        src, req = api.getDataForLocation(location, [], self.date)
        #    if req:
        #        data += [req, src]
        #    else:
        #        self.web_view.warning("Got no datasets from API " +
        #                api.api_name + "!")

@dajaxice_register
def load(request):
    dajax = Dajax()
    apis = Api.objects.filter(user=User.objects.get(username=request.user))
    api_objects = []
    if not apis:
        error = "'Could not load data. No API available.'"
        dajax.script("toastr.warning(" + error + ", 'API warning')")
        dajax.script("markers = []")
        return dajax.json()
    plugindir = os.listdir(preferences.BASE_DIR + "/datavis/plugins")
    for api in apis:
        if not api.api + ".py" in plugindir:
            error = "'Could not load API " + api.api + ". No such API.'"
            dajax.script("toastr.error(" + error + ", 'API error')")
        credentials = ApiKey.objects.filter(identification=api)
        if api.needs_credentials and not credentials:
            error = "'Could not load API " + api.api + ". No credentials.'"
            dajax.script("toastr.error(" + error + ", 'API error')")
            continue
        impobj = getattr(__import__("datavis.plugins." + api.api,
                                    fromlist=[api.api]),
                        api.api)
        if credentials:
            api_objects.append(APIInterface(api.api, impobj,
                    credentials[0].authentication))
        else:
            api_objects.append(APIInterface(api.api, impobj))
    script = "markers = ["
    g = GeoNames(None, "veitheller")
    for api in api_objects:
        for entry in api.locations:
            entry_name = api.locations[entry][0] + ", " + entry
            try:
                place, (lat, lon) = g.geocode(entry_name)
            except (TypeError, exc.GeopyError):
                continue
            script += str([lat, lon, entry_name]) + ","
    script = script[:-1] + script[-1:].replace(",","]")
    dajax.script(script)
    return dajax.json()

@dajaxice_register
def visualize_location_trends(request, lat, lon):
    dajax = Dajax()
    dajax.script("toastr.warning('Not implemented yet.', 'Visualization warning');")
    return dajax.json()

@dajaxice_register
def get_filters_for(request):
    dajax = Dajax()
    apis = Api.objects.filter(user=User.objects.get(username=request.user))
    api_objects = []
    plugindir = os.listdir(preferences.BASE_DIR + "/datavis/plugins")
    for api in apis:
        credentials = ApiKey.objects.filter(identification=api)
        if api.needs_credentials and not credentials:
            error = "'Could not load API " + api.api + ". No credentials.'"
            dajax.script("toastr.error(" + error + ", 'API error')")
            continue
        impobj = getattr(__import__("datavis.plugins." + api.api,
                                    fromlist=[api.api]),
                        api.api)
        if credentials:
            api_objects.append(APIInterface(api.api, impobj,
                    credentials[0].authentication))
        else:
            api_objects.append(APIInterface(api.api, impobj))
    script = "available_filters = "
    for api in api_objects:
        filter_list = api.getIndicators()
        filter_list = filter_list[1]
        filter_list = [i if type(i) is str else str(i) for i in filter_list]
        script += ("[" + str(filter_list)[1:-1] + ",")
    script = script[:-1] + script[-1:].replace(",","]")
    dajax.script(script)
    return dajax.json()
