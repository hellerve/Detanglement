#!/usr/bin/env python3

import random

from PyQt5 import QtWidgets, QtCore, QtWebKit, QtGui, QtWebKitWidgets
from web.PlotterPlugins import PlotterInterfaces

#Python 3 Hack; QString is not compatible with Py3 :(
try:
    from PyQt4.QtCore import QString
except ImportError:
    #it's not defined :(
    QString = type("")


class VisualizeError(Exception):
    """Error that is raised whenever visualization fails."""
    def __init__(self, message):
        """
        Initialize the error.

        Keyword arguments:
        api_message -- message that is displayed when the exception is raised
        """
        self.message = message

    def __str__(self):
        """Returns the exception as a string"""
        return repr(self.message)


class PlotterTrotter(QtWidgets.QMainWindow):
    """
    Class that implements a window in which previously selected
    data is visualized.
    """
    def __init__(self, indicators, plottable_data, begin, path):
        """
        Initialization method

        Keyword arguments:
        stringed_data -- non-plottable string data
        plottable_data -- quantifiable plottable data
        begin -- the starting point of the time line
        path -- path to the parent directory of the project
        """
        super(QtWidgets.QMainWindow, self).__init__()
        self.begin = begin
        self.path = path
        self.left_data = indicators
        self.right_data = plottable_data
        self._initUI()

    def _initUI(self):
        """Creates the plotterUI."""
        self._setWindowStyle()
        self._addWebView()
        self.show()
        self.webview.loadFinished.connect(self._plot)

    def _setWindowStyle(self):
        """Sets the Plotter style."""
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Data Plotter')
        self.setWindowIcon(QtGui.QIcon(
                            QString(
                                self.path + '/images/icon.png')))

    def _addWebView(self):
        """
        Creates a WebView for the Plotter so we can draw
        fancy graphics with Javascript in it.
        """
        self.webview = QtWebKitWidgets.QWebView()
        self.interfaces = PlotterInterfaces(self)
        self.webview.page().mainFrame().addToJavaScriptWindowObject(
                                                            "interfaces",
                                                            self.interfaces)
        self.webview.setUrl(QtCore.QUrl.fromLocalFile(self.path +
                                                      "/html/plotter.html"))
        self.webview.settings().setAttribute(
                QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls,
                True)
        self._setupInspector()
        self.setCentralWidget(self.webview)


    def _setupInspector(self):
        """
        Creates the JavaScript WebInspector.
        This is for debugging purposes and will eventually vanish.
        """
        page = self.webview.page()
        page.settings().setAttribute(
                            QtWebKit.QWebSettings.DeveloperExtrasEnabled,
                            True)
        self.webInspector = QtWebKitWidgets.QWebInspector(self.webview)
        self.webInspector.setPage(page)

        shortcut = QtWidgets.QShortcut(self)
        shortcut.setKey(QtCore.Qt.Key_F6)
        shortcut.activated.connect(self._toggleInspector)
        self.webInspector.setVisible(False)

    def _toggleInspector(self):
        """
        Toggles the JavaScript WebInspector.
        This is for debugging purposes and will eventually vanish.
        """
        self.webInspector.setVisible(not self.webInspector.isVisible())

    def _createLeft(self):
        """This method creates a list of filters."""
        if self.left_data == None: return
        #for i in self.left_data:
        #    self.webview.page().mainWindow().evaluateJavascript('addFilter('+i+');')

    def _createRight(self):
        """
        This method mangles the given data into charts.
        WATCH OUT: STUB
        """
        js_obj = self.webview.page().mainFrame()
        names = []
        for country in self.right_data:
            if type(country) is dict:
                names.extend(list(country.keys()))
                data_list = self._getChildren(country)
        command = ('loadPinch(' + str(names) + ", " + str(data_list) +
                    ', ' + str([str(self.begin), '01', '01']) + ');')
        self.webview.page().mainFrame().evaluateJavaScript(command)
        self.webview.page().mainFrame().evaluateJavaScript('alert(' + str(country) + ');')

    def _getChildren(self, father):
        local = []
        if type(father) is dict:
            for k, v in father.items():
                if type(v) is dict:
                    local.append(self._getChildren(v))
                else:
                    local.append(v if v else 0)
        return local

    def _plot(self):
        self._createLeft()
        self._createRight()


#Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
