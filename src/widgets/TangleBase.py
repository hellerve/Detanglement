#!/usr/bin/env python3

from Crypto.Cipher import AES
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql

# Python 3 Hack; QString is not compatible with Py3 :(
try:
    from PyQt5.QtCore import QString
except ImportError:
    # it's not defined :(
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
        self.setWindowIcon(QtGui.QIcon(QString(self.path +
                                               '/images/icon.png')))
        self.exitAction = QtWidgets.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)

    def _makeInterface(self):
        """Creates the content for the Window(buttons and so on)."""
        dblabel = QtWidgets.QLabel(self)
        dblabel.setGeometry(5, 15, 250, 20)
        dblabel.setText("Enter API name")
        dblabellayout = QtWidgets.QHBoxLayout()
        dblabellayout.addWidget(dblabel)
        self.dbnamebox = QtWidgets.QLineEdit(self)
        self.dbnamebox.move(20, 40)
        self.dbnamebox.setPlaceholderText("Your API Name")
        nameboxlayout = QtWidgets.QHBoxLayout()
        nameboxlayout.addWidget(self.dbnamebox)
        credentialslabel = QtWidgets.QLabel(self)
        credentialslabel.setGeometry(5, 70, 250, 20)
        credentialslabel.setText("Your API keys")
        credlabellayout = QtWidgets.QHBoxLayout()
        credlabellayout.addWidget(credentialslabel)
        creds = QtWidgets.QCheckBox("This API has credentials (API keys)",
                                    self)
        creds.move(20, 95)
        creds.stateChanged.connect(self._credentials)
        credbutlayout = QtWidgets.QHBoxLayout()
        credbutlayout.addWidget(creds)
        self.keylist = []
        keybox = QtWidgets.QLineEdit(self)
        keybox.move(40, 120)
        keybox.setEnabled(False)
        keybox.textChanged.connect(self._keysProvided)
        keyboxlayout = QtWidgets.QHBoxLayout()
        keyboxlayout.addWidget(keybox)
        self.keylist.append(keybox)
        applybut = QtWidgets.QPushButton("Apply", self)
        applybut.move(100, 460)
        applybut.clicked.connect(self._applyAction)
        applyexitbut = QtWidgets.QPushButton("Apply and Exit", self)
        applyexitbut.move(180, 460)
        applyexitbut.clicked.connect(self._applyAndClose)
        cancelbut = QtWidgets.QPushButton("Cancel", self)
        cancelbut.move(310, 460)
        cancelbut.clicked.connect(self.close)
        cancelapplylayout = QtWidgets.QHBoxLayout()
        cancelapplylayout.addWidget(applybut)
        cancelapplylayout.addWidget(applyexitbut)
        cancelapplylayout.addWidget(cancelbut)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(dblabellayout)
        self.layout.addLayout(nameboxlayout)
        self.layout.addLayout(credlabellayout)
        self.layout.addLayout(credbutlayout)
        self.layout.addLayout(keyboxlayout)
        self.layout.addLayout(cancelapplylayout)

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
        if yend < 430:
            newkeybox = QtWidgets.QLineEdit(self)
            newkeybox.move(x, y+25)
            newkeybox.textChanged.connect(self._keysProvided)
            keyboxlayout = QtWidgets.QHBoxLayout()
            keyboxlayout.addWidget(newkeybox)
            self.layout.addLayout(keyboxlayout)
            self.keylist.append(newkeybox)
            newkeybox.show()

    def _applyAction(self):
        """Adds the API to the Database."""
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setHostName("localhost")
        db.setDatabaseName("../rc/creds")
        db.setUserName("root")
        db.setPassword("")
        passwd, ok = QtWidgets.QInputDialog.getText(self, "Password Dialog",
                                                    "Please enter your " +
                                                    "password:")
        if not ok:
            return
        ok = db.open()
        if not ok:
            message = QtWidgets.QErrorMessage(self)
            message.showMessage("Could not connect to Database.")
            message.exec()
            return
        query = QtSql.QSqlQuery()
        query.exec("create table if not exists apis(id int, api_name " +
                   "varchar(30) primary key)")
        query.exec("create table if not exists credentials(credential " +
                   "varchar(60), api_id int)")
        query.exec("select * from apis order by id desc limit 1")
        query.next()
        idn = query.value(0)
        if not idn:
            idn = 1
        query.exec("insert into apis values(" + str(idn) + ", " +
                   self.dbnamebox.text() + ")")
        for keybox in self.keylist:
            keybox.text()

    def _applyAndClose(self):
        """Applies the changes and closes the window."""
        self._applyAction()
        self.close()


# Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
