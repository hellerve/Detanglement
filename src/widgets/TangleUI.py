#!/usr/bin/env python3

import sys

# import web.WebPlugins

from PyQt5 import QtCore, QtWidgets, QtGui

from util.GeoLocate import GeoLocate
from util.ConfigObject import ConfigObject
from web.WebViewObject import WebViewObject
from widgets.SettingsWindow import SettingsWindow
from widgets.ProgressBar import ProgressBar
from widgets.TangleBase import TangleBase

# Python 3 Hack; QString is not compatible with Py3 :(
try:
    from PyQt5.QtCore import QString
except ImportError:
    # it's not defined :(
    QString = type("")


# Just an Exception I made up for debugging purposes
class UIError(Exception):
    """
    An unused exception. Might come in handy later.
    """
    def __init__(message, self):
        self.message = message


class TangleUI(QtWidgets.QMainWindow):
    """
    The main GUI class. Creates and manages the main app window.
    """
    increment = QtCore.pyqtSignal()
    updateApi = QtCore.pyqtSignal()

    def __init__(self, apis, app, path, preferences):
        """
        Initializes the class.

        Keyword arguments:
        apis -- a list of API objects
        app -- the main application
        path -- path to the parent directory of the project
        preferences -- file name of the config file
        """
        QtWidgets.QMainWindow.__init__(self)
        self.apis = apis
        self.location = False
        self.locations = []
        self.treshold = {1: 600, 2: 500, 3: 200, 4: 100, 5: 50}
        self.path = path
        self.app = app
        self.preferences = ConfigObject(path + preferences)
        self._initializeWindow()

    def _initializeWindow(self):
        """Initializes the window. Invoked at startup."""
        self.webView = WebViewObject(self.path, self.apis, self.preferences)
        self._setWindowStyle()
        self._setupBars()
        self.setCentralWidget(self.webView)
        self.webView.loadFinished.connect(self.show)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self._loadPrompt()

    def _loadPrompt(self):
        """
        Displays a prompt tht asks the user whether he wants to start
        over or continue where he left off.
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               'Loading Preferences',
                                               'Do you want to start where ' +
                                               'you left of last time?' +
                                               '\nOtherwise all Settings ' +
                                               'will be lost.',
                                               QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self._loadSettings(False)

    def _setupApis(self):
        """Sets up all the APIs and the loading bar."""
        loc = GeoLocate(self.path + "/rc/GeoLiteCity.dat",
                        self.preferences.configs.value('gnames', None))
        zoom = self.webView.getZoomLevel()

        # print("Start:" + str(datetime.datetime.now()))
        object_count = 0
        for api in self.apis:
            object_count += len(api.locations)
        pg = ProgressBar([x.api_name for x in self.apis], object_count,
                         self.path)
        self.increment.connect(pg.increment)
        self.updateApi.connect(pg.updateApi)
        pg.run()
        for api in self.apis:
            self.updateApi.emit()
            for entry in api.locations:
                location = loc.coordsFromAddr(api.locations[entry][0],
                                              entry)
                no, index = loc.lookForDup(self.locations, location,
                                           self.treshold.setdefault(zoom, 300))
                if no:
                    self.webView.addMarker(location)
                    self.locations.append(location)
                else:
                    self.locations[index].append(location)
                if pg.canceled:
                    self.webView.warning("Loading the data was " +
                                         "interrupted. All data prior " +
                                         "to cancellation was plotted.")
                    return
                else:
                    self.increment.emit()
                    QtWidgets.QApplication.processEvents()
        # print("End: " + str(datetime.datetime.now()) + "\n")
        self.webView.success("All data points added.")

    def _setWindowStyle(self):
        """Sets the window style."""
        height = QtWidgets.QStyle.PM_TitleBarHeight
        bar = QtWidgets.QStyleOptionTitleBar()
        titleBarHeight = self.style().pixelMetric(height, bar, self)
        geometry = self.app.desktop().availableGeometry()
        geometry.setHeight(geometry.height() - (titleBarHeight))
        self.setGeometry(geometry)
        self.setWindowTitle('Detanglement Home')
        self.setWindowIcon(QtGui.QIcon(QString(self.path +
                                               '/images/icon.png')))

    def _setupBars(self):
        """Creates the menu and its buttons. Trivial, but verbose."""
        self.homeAction = QtWidgets.QAction(QtGui.QIcon(QString(self.path +
                                                                "/images/" +
                                                                "home.png")),
                                            'Home', self)
        self.homeAction.setShortcut('Ctrl+B')
        self.homeAction.triggered.connect(self._showHome)
        self.refreshAction = QtWidgets.QAction(QtGui.QIcon(QString(self.path +
                                                                   "/images/" +
                                                                   "refresh" +
                                                                   ".png")),
                                               'Refresh', self)
        self.refreshAction.setShortcut('F5')
        self.refreshAction.triggered.connect(self._loadSettings)
        self.settingsAction = QtWidgets.QAction(QtGui.QIcon(QString(self.path +
                                                                    "/images" +
                                                                    "setting" +
                                                                    "s.png")),
                                                'Settings', self)
        self.settingsAction.setShortcut('Ctrl+E')
        self.settingsAction.triggered.connect(self._showSettings)
        self.helpAction = QtWidgets.QAction(QtGui.QIcon(QString(self.path +
                                                                "/images/" +
                                                                "help.png")),
                                            'Help', self)
        self.helpAction.setShortcut('Ctrl+H')
        self.helpAction.triggered.connect(self._showHelp)
        self.dbAction = QtWidgets.QAction(QtGui.QIcon(QString(self.path +
                                                              '/images/' +
                                                              'add.png')),
                                          'Add to APIs', self)
        self.dbAction.setShortcut('Ctrl+S')
        self.dbAction.triggered.connect(self._addToDatabase)
        self.exitAction = QtWidgets.QAction(QtGui.QIcon(QString(self.path +
                                                                '/images/' +
                                                                'exit.png')),
                                            'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self._doClose)

        self.fileMenu = self.menuBar().addMenu("File")
        self.fileMenu.addAction(self.homeAction)
        self.fileMenu.addAction(self.refreshAction)
        self.fileMenu.addAction(self.exitAction)

        self.settingsMenu = self.menuBar().addMenu("Settings")
        self.fileMenu.addAction(self.dbAction)
        self.settingsMenu.addAction(self.settingsAction)

        self.helpMenu = self.menuBar().addMenu("Help")
        self.helpMenu.addAction(self.helpAction)

        self.toolBar = self.addToolBar("Menu")
        self.toolBar.addAction(self.homeAction)
        self.toolBar.addAction(self.refreshAction)
        self.toolBar.addAction(self.settingsAction)
        self.toolBar.addAction(self.dbAction)
        self.toolBar.addAction(self.exitAction)
        self.toolBar.addAction(self.helpAction)

    def _showHome(self):
        """Brings the user back to the main page."""
        self.setWindowTitle('Detanglement Home')
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(self.path +
                                                      "/html/index.html"))
        self.webView.page().mainFrame().evaluateJavaScript("load()")

    def _showSettings(self):
        """
        Creates a window that displays the settings and enables the user
        to modify them to his likings.
        """
        api_names = [x.api_name for x in self.apis]
        self.settings = SettingsWindow(self.path, self.preferences, api_names)
        self.settings.exec()
        self.preferences.refresh()
        self.preferences.save()
        try:
            if self.preferences.configs.value("toggled", False):
                self._loadSettings()
                self.preferences.configs.remove("toggled")
                self.preferences.save()
        except KeyError:
            self._loadSettings()

    def _loadSettings(self, api_switch=True):
        """Loads the settings."""
        self.maps = self.preferences.configs.value('map')
        self.webView.redrawMap(self.maps)
        if not api_switch or self.preferences.configs.value('api_toggled',
                                                            False):
            self._setupApis()
            self.preferences.configs.remove('api_toggled')
        if not self.apis:
            self.webView.warning("No Datasets chosen!")
        self.geo_location = self.preferences.configs.value('geo_location',
                                                           False)
        if self.geo_location:
            self.webView.locateUser()

    def _eraseSettings(self):
        """Erases all preferences except regarding APIs and saves defaults."""
        self.preferences.configs.setValue('geo_location', False)
        self.preferences.configs.setValue('map', 'google')
        self.preferences.save()

    def _addToDatabase(self):
        """
        I do not know yet if this feature will be needed.
        Until then it remains a stub.
        """
        dbwin = TangleBase(self.path)
        dbwin.exec()

    def _showHelp(self):
        """Displays the HTML help file."""
        self.setWindowTitle('Detanglement Help')
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(self.path +
                                                      "/html/helpfiles/" +
                                                      "help.htm"))

    # Because Users hate it when that happens.
    def closeEvent(self, event):
        """
        Prompts the user whether he really wants to close the session.
        Redirect to _doClose, invoked when the user tries to exit with
        the exit button(x).
        """
        self._doClose()

    def _doClose(self):
        """
        Prompts the user whether he really wants to close the session.
        Obligatory annoying message, invoked when the user tries
        to exit with Ctrl-Q.
        """
        # reply = QtWidgets.QMessageBox.question(self,
        #                                   'Message',
        #                                   'Unsaved Progress will be lost.' +
        #                                   '\nAre you sure you want to quit?',
        #                                   QtWidgets.QMessageBox.Yes |
        #                                   QtWidgets.QMessageBox.No,
        #                                   QtWidgets.QMessageBox.No)
        # if reply == QtWidgets.QMessageBox.Yes:
        sys.exit(0)
        # else:
        #     pass


# Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
