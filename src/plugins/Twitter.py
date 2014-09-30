#!/usr/bin/env python3

import json
import TwitterAPI


class RequestError(Exception):
    """
    The documentation for this Exception can be found
    in the APIIinterface module.
    """
    def __init__(self, api_message):
        self.message = ("Error " + str(api_message[0]['code']) +
                        " occurred with message: \"" +
                        str(api_message[0]['message']) + "\"")

    def __str__(self):
        return repr(self.message)


class Twitter(TwitterAPI.TwitterAPI):
    """
        Provides content from Twitter. Trends and tweets
        for specific locations plus a list of locations we have trends for.
    """
    def __init__(self, consumer_key, consumer_secret, access_key,
                 access_secret):
        """
        Initializes the class

        Keyword arguments:
        consumer_key -- the API consumer key
        consumer_secret -- the API consumer secret
        access_key -- ... you know what it is
        access_secret -- ...
        """
        TwitterAPI.TwitterAPI.__init__(self, consumer_key, consumer_secret,
                                       access_key, access_secret)
        self.requiresFilter = False
        self.country_list = {}
        self.city_list = {}
        self._getCities()

    def _getCities(self):
        """Gets a list of cities Twitter has got trends for."""
        request = json.loads(self.request("trends/available").text)
        self._testValidity(request)
        for data in request:
            if data['placeType']['name'] == "Country":
                self.country_list[data['name']] = data['woeid']
                continue
            if data['placeType']['name'] == "Town":
                self.city_list[data['name']] = [data['country'],
                                                data['woeid']]

    def _getTrends(self, woeid):
        """
        Gets a list of trends for a specific WOEID.

        Keyword arguments:
        woeid -- the WOEID we need trends for

        Returns:
        data -- the data that was requested
        """
        request = json.loads(self.request("trends/place", {'id': woeid}).text)
        self._testValidity(request)
        data = []
        for json_obj in request[0]["trends"]:
            data.append(json_obj["name"])
        return data

    def _testValidity(self, request):
        """
        Tests whether a request is valid. When an error is encountered,
        an exception is thrown.

        Keyword arguments:
        request -- the request that is to be tested

        Known Exceptions:
            RequestError -- raised when the request was not valid
        """
        if type(request) == dict and request['errors']:
            raise RequestError(request['errors'])

    def _getWOEIDbyCityName(self, city_name):
        """Returns the WOEID for a given city name."""
        return self.city_list[city_name][1]

    def getLocations(self):
        """
        The standardized method call for the wrapper.

        Returns:
        self.city_list -- a list of cities for which data exists
        """
        return self.city_list

    def getDataForLocation(self, loc_name, filt, date):
        """
        The standardized method call for the wrapper.

        Keyword arguments:
        loc_name -- name of the location we need data for

        Returns:
        the data that was requested(default None - when there is none)
        """
        try:
            return self._getTrends(self._getWOEIDbyCityName(loc_name[0]))
        except KeyError:
            return None

    def getIndicators(self):
        return None


# Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
