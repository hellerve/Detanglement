#!/usr/bin/env python3

from PyQt5 import QtCore, QtWebKit

from web.PlotterTrotter import *
from widgets.FilterWindow import FilterWindow

class TangleInterfaces(QtCore.QObject):
    """
    Class that provides an interface between Javascript and Python.
    The methods in this class are all referenced by JS code,
    except for __init__ which is called in a Qt context.
    """
    def __init__(self, web_view, apis, path):
        """
        Initializes the class

        Keyword arguments:
        web_view -- a QtWebKit object
        apis -- the apis that are available
        path -- the path to the parent directory of the project
        """
        QtCore.QObject.__init__(self, web_view)
        self.filters = None
        self.date = None
        self.web_view = web_view
        self.apis = apis
        self.path = path

    @QtCore.pyqtSlot(str, str)
    def submitLocation(self, country, city):
        """
        Is called when the user submits his location by the form.
        Reads the input and adds the location.

        Keyword arguments:
        country -- country name
        city -- city name
        """
        self.web_view.location = self.web_view.locateUser(country, city)

    def _getInfo(self, title):
        """
        Gets the API data that is requested.

        Keyword arguments:
        title -- location as string

        Returns:
        data -- data that is available
        """
        location = title.split(", ") if ", " in title else title
        data = []
        for api in self.apis:
            if api.requiresFilter():
                self._askForFilter(api)
                if self.filters:
                    src = api.api_name
                    req = {}
                    for i in self.filters:
                        if self.date:
                            x, t = api.getDataForLocation(location[0], i, self.date)
                        else:
                            x, t = api.getDataForLocation(location[0], i)
                        if not t:
                            self.web_view.warning("No datasets for filter " +
                                    i + "!")
                        else: req.update({k+'/'+i:v for k,v in t.items()})
                else:
                    src, req = None, None
            else:
                src, req = api.getDataForLocation(location, [], self.date)
            if req:
                data += [req, src]
            else:
                self.web_view.warning("Got no datasets from API " +
                        api.api_name + "!")
        return data

    @QtCore.pyqtSlot(str)
    def visualizeTrends(self, loc):
        """
        Creates the window that visualizes the data for a given location.

        Keyword arguments:
        loc -- location to be visualized
        """
        data = self._getInfo(loc)
        try:
            if data:
                pt = PlotterTrotter(self.filters, data, self.date[0],
                        self.path)
        except VisualizeError as e:
            self.webView.page().mainFrame().evaluateJavaScript(
                                                "alert(" + str(e) + ")")

    def _askForFilter(self, api):
        filter_choice = FilterWindow(self.path, *api.getIndicators())
        filter_choice.appliedSignal.connect(self.setFilters)
        filter_choice.dateSignal.connect(self.setDate)
        filter_choice.exec()

    def setFilters(self, filters):
        self.filters = filters

    def setDate(self, date):
        self.date = date


#Warning: This class is a stub. Do not use it yet.
class Plugins(QtWebKit.QWebPluginFactory):
    """
        This class is a stub and should not be used yet.
    """
    def __init__(self, parent):
        """
            This method should not be called yet.
            It does nothing - useful.
        """
        QtWebKit.QWebPluginFactory.__init__(self, parent)


#Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
