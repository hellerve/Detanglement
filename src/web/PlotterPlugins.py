#!/usr/bin/env python3

from PyQt5 import QtCore, QtWebKit


# WARNING: STUB CLASS!
class PlotterInterfaces(QtCore.QObject):
    """
        This provides an interface between Javascript and Python.
        The methods in this class are all referenced by JS code -
        except for __init__ which is called in a Qt context.
        WARNING!
        THIS MODULE IS A STUB
    """
    def __init__(self, web_view):
        """
        Initializes the class

        Keyword arguments:
        web_view -- a QtWebKit object
        """
        QtCore.QObject.__init__(self, web_view)
        self.web_view = web_view


# Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
