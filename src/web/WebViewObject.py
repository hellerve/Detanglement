#!/usr/bin/env python3

from PyQt5 import QtWebKit, QtCore, QtWebKitWidgets, QtWidgets

from web.WebPlugins import TangleInterfaces
from util.GeoLocate import GeoLocate

class WebViewObject(QtWebKitWidgets.QWebView):
    """
    Class used for the creation and management of the WebView.
    """
    def __init__(self, path, apis, preferences):
        """
        Instantiates the class.

        Keyword arguments:
        path -- path to the applications main directory
        apis -- list of api objects
        preferences -- the config object file name
        """
        QtWebKitWidgets.QWebView.__init__(self)
        self.path = path
        self.interfaces = TangleInterfaces(self, apis, path)
        self.location_marker = False
        self.location = None
        self.preferences = preferences
        self.page().mainFrame().addToJavaScriptWindowObject("interfaces",
                                self.interfaces)
        self.setUrl(QtCore.QUrl.fromLocalFile(self.path +
                                                "/html/index.html"))
        self.settings().setAttribute(
                QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls,
                True)
        self._setupInspector()

    def _setupInspector(self):
        """
        Creates the JavaScript WebInspector.
        This is for debugging purposes and will eventually vanish.
        """
        page = self.page()
        page.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QtWebKitWidgets.QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QtWidgets.QShortcut(self)
        shortcut.setKey(QtCore.Qt.Key_F6)
        shortcut.activated.connect(self._toggleInspector)
        self.webInspector.setVisible(False)

    def _toggleInspector(self):
        """
        Toggles the JavaScript WebInspector via F12.
        This is for debugging purposes and will eventually vanish.
        """
        self.webInspector.setVisible(not self.webInspector.isVisible())

    #locates the user via pygeoip
    def locateUser(self, country=None, city=None):
        """
        Locates the user via the GeoLocate class.

        Keyword arguments:
        country -- the country name as a string (default None)
        city -- the city name as a string (default None)
        """
        loc = GeoLocate(self.path + "/rc/GeoLiteCity.dat",
                self.preferences.configs.value("gnames", None))
        if country and city:
            check = loc.ownCoordsFromAddr(country, city)
            if check == False:
                self.error("Could not locate provided address.")
                return
        else:
            loc.getOwnAddress()
        self.location = [loc.country, loc.city, loc.lat, loc.lon]
        self.addLocationMark()

    def redrawMap(self, maps):
        """
        Redraws the map. Invoked when switching between Kartograph,
        OSM and Google Maps.

        Keyword arguments:
        maps -- the map framework as string
        """
        js = self.page().mainFrame()
        if (maps == "google" and
                js.evaluateJavaScript("getMap()") != 0):
            js.evaluateJavaScript("setMap(0)")
            js.evaluateJavaScript("initializeGoogleMap()")
        elif (maps == "kartograph" and
                js.evaluateJavaScript("getMap()") != 1):
            js.evaluateJavaScript("setMap(1)")
            js.evaluateJavaScript("initializeKartograph()")
        elif (maps == "osm" and
                js.evaluateJavaScript("getMap()") != 2):
            js.evaluateJavaScript("setMap(2)")
            js.evaluateJavaScript("initializeOSM()")

    def addLocationMark(self):
        """Adds a location mark to the location which webView knows of."""
        if self.location_marker:
            self.page().mainFrame().evaluateJavaScript(
                            'deleteLocationMarker()')
        add_location_command = ("addLocationMarker('" +
                                str(self.location[2]) + "', '" +
                                str(self.location[3]) + "')")
        self.page().mainFrame().evaluateJavaScript(add_location_command)
        self.location_marker = True

    #adds a marker to the location specified via the API
    def addMarker(self, place):
        """
        Adds a marker to a place specified.

        Keyword arguments:
        place -- the specified location
        """
        add_marker_command = ("addMarker('" + str(place[2]) +
                              "', '" + str(place[3]) + "', '" +
                              str(place[0]) + ", " + str(place[1]) + "')")
        self.page().mainFrame().evaluateJavaScript(add_marker_command)

    def getZoomLevel(self):
        """Gets the maps' zoom level(wrapper around JS' getZoom())."""
        return self.page().mainFrame().evaluateJavaScript(
                                            'tangle.map.getZoom()')

    def success(self, message):
        """
        This is a wrapper method around the JS function toastr.success().

        Keyword arguments:
        message -- the message that is to be displayed by the function
        """
        self.page().mainFrame().evaluateJavaScript(
                            'toastr.success("'+ message +'", "Success")')

    def warning(self, message):
        """
        This is a wrapper method around the JS function toastr.warning().

        Keyword arguments:
        message -- the message that is to be displayed by the function
        """
        self.page().mainFrame().evaluateJavaScript(
                            'toastr.warning("'+ message +'", "Warning")')

    def error(self, message):
        """
        This is a wrapper method around the JS function toastr.error().

        Keyword arguments:
        message -- the message that is to be displayed by the function
        """
        self.page().mainFrame().evaluateJavaScript(
                            'toastr.error("'+ message +'", "Error")')


#Not a  main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
