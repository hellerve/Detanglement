#!/usr/bin/env python3

import pygeoip

from geopy import exc, distance
from geopy.point import Point
from geopy.geocoders import GeoNames
from urllib import request


class GeoLocate(pygeoip.GeoIP):
    """
    Geolocation class that inherits from GeoIP.
    It also has an interface to geopy which
    all in all seems a bit hacky to me.
    You decide.
    """
    def __init__(self, filename, geo_identity=None):
        """
        Initializes the class.

        Keyword arguments:
        filename -- string representation of the file containing the geodata
        geo_identity -- string representation of the identity in geonames
        """
        pygeoip.GeoIP.__init__(self, filename)
        self._setup_segments()
        if geo_identity:
            self.gnames = GeoNames(None, geo_identity)

    def getOwnAddress(self):
        """Gets own address based on the IP Address of the user."""
        self.address = str(self._getIPAddress())[2:-1]
        (self.country, self.city, self.lat,
         self.lon) = self.coordsFromAddr(*self._locateAddress())

    def _getIPAddress(self):
        """
        Gets own IP address using a web service. Is that too sloppy?

        Returns:
        string -- IP address
        """
        return request.urlopen("http://bot.whatismyipaddress.com/").read()

    def _locateAddress(self):
        """
        Gets the city and country name for a certain location.

        Returns:
            Tuple of:
                string -- city name
                string -- country name
        """
        return (self.record_by_addr(self.address)['city'],
                self.record_by_addr(self.address)['country_name'])

    def coordsFromAddr(self, cityname, countryname):
        """
        Gets the coordinates for a certain city name.
        Currently problematic with Korea; geonames
        seems to have issues in that area.

        Keyword Arguments:
        cityname -- the name of the city searched for
        countryname -- the name of the country searched for

        Returns:
            List of:
                countryname -- country name provided
                cityname -- city name provided
                lat -- latitude of location (default None)
                lon -- longitude of location (default None)
        """
        try:
            place, (lat, lon) = self.gnames.geocode(str(cityname) +
                                                    ", " + str(countryname))
            return [countryname, cityname, lat, lon]
        except (TypeError, exc.GeopyError):
            return [countryname, cityname, None, None]

    def ownCoordsFromAddr(self, cityname, countryname):
        """
        Gets the coordinates for the own city name
        and makes the place found the own location.
        Currently problematic with Korea; geonames
        seems to have issues in that area.

        Keyword Arguments:
        cityname -- the name of the city searched for
        countryname -- the name of the country searched for

        Returns:
        Boolean -- Indicates whether the coordinates could be parsed
        """
        self.city = cityname
        self.country = countryname
        try:
            place, (lat, lon) = self.gnames.geocode(str(cityname) +
                                                    ", " + str(countryname))
            self.lat = lat
            self.lon = lon
            return True
        except (TypeError, exc.GeopyError):
            self.lat = None
            self.lon = None
            return False

    def lookForDup(self, location_list, location, treshold):
        """
        Searches for points to be merged in a list of locations
        within a certain treshold.

        Keyword Arguments:
        location_list -- list of known locations
        location -- the location to be tested
        treshold -- the treshold for the test

        Returns:
            Tuple of:
                - Boolean -- Indicates whether the location could be merged
                - ind -- Index of the location which fits (default None)

        Known Exceptions:
            Value Error:
                Raised when gnames does not know the location or is not set
        """
        if not self.gnames:
            raise ValueError
        try:
            loc_tuple = Point(location[2], location[3])
            d = distance.distance
            ind = 0
            for test in location_list:
                test_tuple = Point(test[2], test[3])
                if float(d(loc_tuple, test_tuple).miles) < treshold:
                    return False, ind
                ind += 1
            return True, None
        except ValueError:
            return True, None


# Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
