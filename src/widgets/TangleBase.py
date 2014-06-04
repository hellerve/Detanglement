#!/usr/bin/env python3

from PyQt5 import QtCore, QtGui, QtWidgets

#Python 3 Hack; QString is not compatible with Py3 :(
try:
    from PyQt5.QtCore import QString
except ImportError:
    #it's not defined :(
    QString = type("")

class TangleBase(QtWidgets.QDialog):
    """
    Creates a dialog that poses as the window where you can
    add APIs to Entanglement. As such, it is also an interface
    between the database and the application.
    """
    def __init__(self, path):
        """
        initializes the class

        Keyword arguments:
        path -- path to the parent directory of the project
        """
        super(QtWidgets.QDialog, self).__init__()
        self.path = path
        self._makeGUI()
        self._makeInterface()

    def _makeGUI(self):
        """Defines the GUI for the settings window."""
        self.setWindowTitle('Entanglement - Add APIs to the Database')
        self.setGeometry(QtCore.QRect(200, 100, 400, 500))
        self.setFixedSize(400, 500)
        self.setWindowIcon(QtGui.QIcon(
                            QString(
                                self.path + '/images/icon.png')))
        self.exitAction = QtWidgets.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)

    def _makeInterface(self):
        """Creates the content for the Window(buttons and so on)."""
        dblabel = QtWidgets.QLabel(self)
        dblabel.setGeometry(5, 10, 250, 20)
        dblabel.setText("Enter API name")
        dblabellayout = QtWidgets.QHBoxLayout()
        dblabellayout.addWidget(dblabel)
        self.dbnamebox = QtWidgets.QLineEdit()
        self.dbnamebox.setPlaceholderText("Wow")
        nameboxlayout = QtWidgets.QHBoxLayout()
        nameboxlayout.addWidget(self.dbnamebox)
        credentialslabel = QtWidgets.QLabel(self)
        credentialslabel.setGeometry(5, 50, 250, 20)
        credentialslabel.setText("Your API keys")
        credlabellayout = QtWidgets.QHBoxLayout()
        credlabellayout.addWidget(credentialslabel)
        credentials = QtWidgets.QCheckBox("This API has credentials (API keys)", self)
        credentials.move(10, 70)
        credentials.stateChanged.connect(self._credentials)
        credbutlayout = QtWidgets.QHBoxLayout()
        credbutlayout.addWidget(credentials)
        self.keylist = []
        keybox = QtWidgets.QLineEdit()
        keybox.setEnabled(False)
        keybox.textChanged.connect(self._keysProvided)
        keyboxlayout = QtWidgets.QHBoxLayout()
        keyboxlayout.addWidget(keybox)
        self.keylist.append(keybox)
        applybut = QtWidgets.QPushButton("Apply", self)
        applybut.move(400, 470)
        applybut.clicked.connect(self._applyAction)
        cancelbut = QtWidgets.QPushButton("Cancel", self)
        cancelbut.move(400, 420)
        cancelbut.clicked.connect(self.close)
        cancelapplylayout = QtWidgets.QHBoxLayout()
        cancelapplylayout.addWidget(applybut)
        cancelapplylayout.addWidget(cancelbut)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(dblabellayout)
        self.layout.addLayout(nameboxlayout)
        self.layout.addLayout(credlabellayout)
        self.layout.addLayout(credbutlayout)
        self.layout.addLayout(keyboxlayout)

    def _credentials(self, state):
        """
        Toggles credentials. Invoked when the credentials checkbox is clicked.

        Keyword arguments:
        state -- the state of the checkbox
        """
        for keybox in self.keylist:
            keybox.setEnabled(not keybox.isEnabled())

    def _keysProvided(self):
        """
        Adds another QLineEdit if possible.
        Invoked when the last credentials lineedit is edited.

        Keyword arguments:
        state -- the state of the checkbox
        """
        sender = self.keylist[-1]
        sender.textChanged.disconnect(self._keysProvided)
        x, y, xend, yend = sender.geometry().getCoords()
        if yend < 450:
            newkeybox = QtWidgets.QLineEdit()
            newkeybox.setGeometry(x, yend+20, xend-x, yend-y)
            newkeybox.textChanged.connect(self._keysProvided())
            self.layout.addWidget(newkeybox)

    def _applyAction(self):
        """Adds the API to the Database."""
        self.close()


#Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
