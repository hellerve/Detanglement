#!/usr/bin/env python3

from PyQt5 import QtWidgets, QtCore, QtGui

#Python 3 Hack; QString is not compatible with Py3 :(
try:
    from PyQt5.QtCore import QString
except ImportError:
    #it's not defined :(
    QString = type("")


class ProgressBar(QtWidgets.QWidget, QtCore.QThread):
    """
    Class that creates a progress bar used while the data points are
    placed on the map.
    """
    def __init__(self, names, ranged, path):
        """
        Initialize the class

        Keyword arguments:
        names -- api names
        ranged -- range of the api
        path -- path to the parent directory of the project
        """
        super(QtWidgets.QWidget, self).__init__()
        self.ranged = ranged
        self.names = names
        self.names.reverse()
        self.canceled = False
        self._initUI(path)
        self.show()

    def _initUI(self, path):
        """
        Initialize the window and the progress bar

        Keyword arguments:
        path -- path to the parent directory of the project
        """
        self.setGeometry(600, 400, 270, 120)
        self.setFixedSize(270, 150)
        self.setWindowTitle("Setup Progress")
        self.setWindowIcon(QtGui.QIcon(
                              QString(
                                path + '/images/icon.png')))
        self.value = 0
        self.proglabel = QtWidgets.QLabel(self)
        self.proglabel.setGeometry(70, 20, 150, 20)
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setGeometry(30, 50, 200, 25)
        self.pbar.setRange(0, self.ranged)
        self.pbar.setValue(0)
        cancelbut = QtWidgets.QPushButton("Cancel", self)
        cancelbut.move(170, 80)
        cancelbut.clicked.connect(self._buttonClicked)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.proglabel)
        layout.addWidget(self.pbar)
        layout.addWidget(cancelbut)

    def run(self):
        QtWidgets.QApplication.processEvents()

    def increment(self):
        """
        Increments the value of the progress bar. As far as I can tell,
        that is a pretty odd implementation of a progress bar,
        but it is minimalistic and works fine for me
        """
        self.value += 1
        self.pbar.setValue(self.value)

    def updateApi(self):
        """Updates the API loading display"""
        self.proglabel.setText("Loading " + self.names.pop())

    def _buttonClicked(self):
        """
        Gets called when the cancel button is pressed. Closes the window
        and breaks out of the load loop
        """
        self.canceled = True
        self.pbar.setValue(self.ranged)

    def keyPressEvent(self, e):
        """
        Reacts to a pressed key. Invokes the same routine as a click on
        cancel

        Keyword arguments:
        e -- event that happened
        """
        if e.key() == QtCore.Qt.Key_Escape:
            self.buttonClicked()

    def updateName(self):
        """Updates the api name"""
        self.proglabel.setText("Loading " + self.names.pop())


#Not a main module.
if __name__ == "__main__":
    raise ImportError("This should not be used as main module.")
