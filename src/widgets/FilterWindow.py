#!/usr/bin/env python3

import re
import sre_constants

from PyQt5 import QtCore, QtGui, QtWidgets

#Python 3 Hack; QString is not compatible with Py3 :(
try:
    from PyQt5.QtCore import QString
except ImportError:
    #it's not defined :(
    QString = type("")

class FilterWindow(QtWidgets.QDialog):
    """
    Creates a dialog that poses as the window where you can
    tweak on your filter. As such, it is also an interface
    between the WebView, the GUI and the API
    """
    appliedSignal = QtCore.pyqtSignal(list)
    dateSignal = QtCore.pyqtSignal(tuple)
    def __init__(self, path, name, filt):
        """
        initializes the class

        Keyword arguments:
        path -- the path to the applications base dir
        name -- the name of the api
        filt -- the filters that are available for the api
        """
        super(QtWidgets.QDialog, self).__init__()
        self.name = name
        self.filters = filt
        self.path = path
        self._makeGUI()

    def _makeGUI(self):
        """Defines the GUI for the filter window."""
        self.setWindowTitle('Entanglement - Please specify filters for ' + self.name)
        self.setGeometry(QtCore.QRect(200, 100, 500, 500))
        self.setFixedSize(500, 500)
        self.setWindowIcon(QtGui.QIcon(
                            QString(
                                self.path + '/images/icon.png')))
        self.exitAction = QtWidgets.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)
        self.layout = QtWidgets.QVBoxLayout()
        timelabel = QtWidgets.QLabel(self)
        timelabel.setText("Set Time Boundaries:")
        timelayout = QtWidgets.QVBoxLayout()
        timelayout.addWidget(timelabel)
        self.layout.addLayout(timelayout)
        self.layout.addLayout(self._makeTime())
        optionslabel = QtWidgets.QLabel(self)
        optionslabel.setText("Choose filters:")
        optionslayout = QtWidgets.QVBoxLayout()
        optionslayout.addWidget(optionslabel)
        self.layout.addLayout(optionslayout)
        searchBox = QtWidgets.QLineEdit()
        searchBox.setPlaceholderText("Enter filter here")
        searchBox.textChanged.connect(self.updateFilters)
        filterlayout = QtWidgets.QVBoxLayout()
        filterlayout.addWidget(searchBox)
        self.layout.addLayout(filterlayout)
        self.layout.addLayout(self._makeOptions())
        cancelbut = QtWidgets.QPushButton("Cancel", self)
        cancelbut.move(400, 470)
        cancelbut.clicked.connect(self.close)
        applybut = QtWidgets.QPushButton("Apply", self)
        applybut.move(400, 420)
        applybut.clicked.connect(self._applyAction)
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(cancelbut)
        buttons.addWidget(applybut)
        self.layout.addLayout(buttons)
        self.setLayout(self.layout)

    def _makeTime(self):
        """Creates two windows for a timeline."""
        layout = QtWidgets.QHBoxLayout()
        self.beginTime = QtWidgets.QDateEdit()
        self.beginTime.setDisplayFormat("yyyy")
        self.beginTime.setDate(QtCore.QDate(2000, 1, 1))
        self.endTime = QtWidgets.QDateEdit()
        self.endTime.setDisplayFormat("yyyy")
        self.endTime.setDate(QtCore.QDate(2012, 1, 1))
        layout.addWidget(self.beginTime)
        layout.addWidget(self.endTime)
        return layout


    def _makeOptions(self):
        """Creates the content for the Window(buttons and so on)."""
        layout = QtWidgets.QHBoxLayout()
        self.filterview = ChoiceList()
        self.filterview.setSortingEnabled(True)
        self.filterview.itemClicked.connect(self.addItem)
        for filt in self.filters:
            x = QtWidgets.QListWidgetItem()
            x.setText(filt)
            self.filterview.addItem(x)
        self.chosenview = ChoiceList()
        self.chosenview.setSortingEnabled(True)
        self.chosenview.itemClicked.connect(self.removeItem)
        layout.addWidget(self.filterview)
        layout.addWidget(self.chosenview)
        return layout

    def updateFilters(self, search):
        self.filterview.clear()
        for filt in self.filters:
            try:
                if re.search(search, filt):
                    x = QtWidgets.QListWidgetItem()
                    x.setText(filt)
                    self.filterview.addItem(x)
            except sre_constants.error:
                if search in filt:
                    x = QtWidgets.QListWidgetItem()
                    x.setText(filt)
                    self.filterview.addItem(x)

    def addItem(self, item):
        index = self.filters.index(item.text())
        self.filterview.takeItem(self.chosenview.row(item))
        self.chosenview.addItem(item)

    def removeItem(self, item):
        index = self.filters.index(item.text())
        self.chosenview.takeItem(self.chosenview.row(item))
        self.filterview.addItem(item)

    def _applyAction(self):
        filters = []
        for i in range(self.chosenview.count()):
            filters.append(self.chosenview.item(i).text())
        self.dateSignal.emit((self.beginTime.date().year(),
            self.endTime.date().year()))
        self.appliedSignal.emit(filters)
        self.close()

class ChoiceList(QtWidgets.QListWidget):
    def __init__(self):
        super(QtWidgets.QListWidget, self).__init__()
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            super(ChoiceList, self).dragEnterEvent(e)

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
        else:
            super(ChoiceList, self).dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            links = []
            for url in e.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            e.setDropAction(QtCore.Qt.MoveAction)
            super(ChoiceList, self).dropEvent(e)


#Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
