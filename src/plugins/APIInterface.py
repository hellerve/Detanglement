#!/usr/bin/env python3

class RequestError(Exception):
    """Error that is raised whenever a request goes wrong."""
    def __init__(self, api_message):
        """
        Initialize the error.

        Keyword arguments:
        api_message -- message that is displayed when the exception is raised
        """
        self.message = ("Error " + str(api_message[0]['code']) +
                       " occurred with message: \"" +
                       str(api_message[0]['message']) + "\"")

    def __str__(self):
        """Returns the exception as a string"""
        return repr(self.message)


class APIInterface():
    """
    This class provides an interface to the APIs.
    A pure wrapper class.
    """
    def __init__(self, api_name, api_object, args=None):
        """
        Initializes the wrapper class.

        Keyword arguments:
        api_name -- Name of the API
        api_object -- API object to be wrapped
        args -- API object arguments (default None)
        """
        self.api_name = api_name
        self.api_object = (api_object(*args) if not args == None
                           else api_object())
        self.locations = self.api_object.getLocations()

    def getIndicators(self):
        """
        Standard function that must be present in every API that is wrapped

        Return value:
            List of:
                Indicators
        """
        return self.api_name, self.api_object.getIndicators()

    def requiresFilter(self):
        return self.api_object.requiresFilter

    def getDataForLocation(self, location, filters, date):
        """
        Standard function that must be present in every API that is wrapped

        Keyword arguments:
        location -- the location for which data should be returned

        Return value:
            Tuple of:
                - Name of the API
                - Data
        """
        return self.api_name, self.api_object.getDataForLocation(location, filters, date)


#Not a main class
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
