#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets

#Python 3 Hack; QString is not compatible with Py3 :(
try:
    from PyQt5.QtCore import QString
except ImportError:
    #it's not defined :(
    QString = type("")

class SettingsWindow(QtWidgets.QDialog):
    """
    Creates a dialog that poses as the window where you can
    tweak on your settings. As such, it is also an interface
    between the WebView, the GUI and the Config Object
    """
    def __init__(self, path, config_object, api_names):
        """
        initializes the class

        Keyword arguments:
        path -- path to the parent directory of the project
        config_object -- a ConfigObject instance
        api_names -- names of the apis to be loaded
        """
        super(QtWidgets.QDialog, self).__init__()
        self.path = path
        self.config = config_object
        self.api_names = api_names
        self.toggled = False
        self.mapToggled = False
        self.apiToggled = False
        self._makeGUI()
        self._makeSettings()

    def _makeGUI(self):
        """Defines the GUI for the settings window."""
        self.setWindowTitle('Entanglement - Settings')
        self.setGeometry(QtCore.QRect(200, 100, 300, 400))
        self.setFixedSize(300, 400)
        self.setWindowIcon(QtGui.QIcon(
                            QString(
                                self.path + '/images/icon.png')))
        self.exitAction = QtWidgets.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self._doClose)

    def _makeSettings(self):
        """Creates the content for the Window(buttons and so on)."""
        self.locate = QtWidgets.QCheckBox("Geolocation", self)
        if self.config.configs["geo_location"] == True:
                self.locate.toggle()
        self.locate.move(10, 10)
        self.locate.stateChanged.connect(self._geoLocate)
        self.maplabel = QtWidgets.QLabel(self)
        self.maplabel.setGeometry(0, 30, 250, 20)
        self.maplabel.setText("Map to use:")
        self.google = QtWidgets.QCheckBox("Google Maps", self)
        if self.config.configs["map"] == "google":
            self.google.toggle()
        self.google.move(10, 50)
        self.google.stateChanged.connect(self._googleMaps)
        self.osm = QtWidgets.QCheckBox("OSM", self)
        if self.config.configs["map"] == "osm":
            self.osm.toggle()
        self.osm.move(130, 50)
        self.osm.stateChanged.connect(self._osm)
        #self.karto = QtWidgets.QCheckBox("Kartograph", self)
        #if self.config.configs["map"] == "kartograph":
        #    self.karto.toggle()
        #self.karto.move(200, 50)
        #self.karto.stateChanged.connect(self._kartograph)
        self.maps = QtWidgets.QButtonGroup()
        self.maps.setExclusive(True)
        self.maps.addButton(self.google)
        #self.maps.addButton(self.karto)
        self.maps.addButton(self.osm)
        self.apilabel = QtWidgets.QLabel(self)
        self.apilabel.setGeometry(0, 70, 280, 20)
        self.apilabel.setText("Data sets to use(will take effect at restart):")
        for i, api in enumerate(self.api_names):
            x = QtWidgets.QCheckBox(api, self)
            if api in self.config.configs['apis']:
                x.toggle()
            x.move(10, 90+(i*20))
            x.stateChanged.connect(self._twitterAPI)

    def _geoLocate(self, state):
        """
        Toggles the geo location. Invoked when the checkbox is clicked.

        Keyword arguments:
        state -- the state of the checkbox
        """
        self.toggled = True
        if state == QtCore.Qt.Checked:
            self.config.configs["geo_location"] = True
        else:
            self.config.configs["geo_location"] = False

    def _googleMaps(self, state):
        """
        Toggles google maps(exclusive with osm and kartograph).

        Keyword arguments:
        state -- the state of the checkbox
        """
        self.toggled = True
        self.mapToggled = True
        if state == QtCore.Qt.Checked:
            self.config.configs["map"] = "google"

    def _kartograph(self, state):
        """
        Toggles kartograph maps(exclusive with osm and google).

        Keyword arguments:
        state -- the state of the checkbox
        """
        self.toggled = True
        self.mapToggled = True
        if state == QtCore.Qt.Checked:
            self.config.configs["map"] = "kartograph"

    def _osm(self, state):
        """
        Toggles osm maps(exclusive with kartograph and google).

        Keyword arguments:
        state -- the state of the checkbox
        """
        self.toggled = True
        self.mapToggled = True
        if state == QtCore.Qt.Checked:
            self.config.configs["map"] = "osm"

    def _twitterAPI(self, state):
        """
        Toggles the Twitter API. Invoked when the Twitter
        checkbox is clicked.

        Keyword arguments:
        state -- the state of the checkbox
        """
        self.toggled = True
        if state == QtCore.Qt.Checked:
            if "Twitter" not in self.config.configs["apis"]:
                self.apiToggled = True
                self.config.configs["apis"].append("Twitter")
        else:
            if "Twitter" in self.config.configs["apis"]:
                self.config.configs["apis"].remove("Twitter")

    def _saveSettings(self):
        """Saves the current state of the settings."""
        self.config.save()

    def closeEvent(self, event):
        """
        Hands the execution over to the internal function _doClose.
        Is invoked when the user presses the close button(x)

        Keyword arguments:
        event -- the event that invoked the method
        """
        self._doClose()

    #prompts whether the user is sure to close. Invoked when the user exits the window
    def _doClose(self):
        """
        Prompts whether the user wants to save the state of the settings.
        Is invoked when the user exits with Ctrl-Q
        """
        if self.toggled:
            reply = QtWidgets.QMessageBox.question(self,
                                              'Message',
                                              'New Settings are unsaved.' +
                                              '\nDo you want to apply them before exiting?',
                                              QtWidgets.QMessageBox.Yes |
                                              QtWidgets.QMessageBox.No,
                                              QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                if self.apiToggled:
                    self.config.configs["toggled"] = True
                self._saveSettings()
                self.close()
            else:
                self.close()
        else:
            self.close()


#Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
