#!/usr/bin/env python3.4

import os
import sys
import webbrowser

from argparse import ArgumentParser

path = ""
# Version information ########################################################
# Inspired by the Makehuman Project ##########################################
__version__ = [0, 1, 2]             # Major, minor and patch version number
__release__ = False                 # False for nightly
__versionSub__ = "Alpha/Test"       # Short version description
##############################################################################


def getVersionDigitsStr():
    """
    String representation of the version number only (no additional info)
    Inspired by the Makehuman Project
    """
    return ".".join([str(v) for v in __version__])


def _versionStr():
    """
    Inspired by the Makehuman Project
    """
    if __versionSub__:
        return getVersionDigitsStr() + " " + __versionSub__
    else:
        return getVersionDigitsStr()


def isRelease():
    """
    True when release version, False for nightly (dev) build
    Inspired by the Makehuman Project
    """
    return __release__


def isBuild():
    """
    Determine whether the app is frozen using pyinstaller/py2app.
    Returns True when this is a release or nightly build (eg. it is build as a
    distributable package), returns False if it is a source checkout.
    Inspired by the Makehuman Project
    """
    return getattr(sys, 'frozen', False)


def getVersion():
    """
    Comparable version as list of ints
    Inspired by the Makehuman Project
    """
    return __version__


def getVersionStr(verbose=True):
    """
    Verbose version as string, for displaying and information
    Inspired by the Makehuman Project
    """
    if isRelease():
        return _versionStr()
    else:
        try:
            result = _versionStr() + " (r%s %s)" % (os.environ['HGREVISION'],
                                                    os.environ['HGNODEID'])
            if verbose:
                result += (" [%s]" % os.environ['HGREVISION_SOURCE'])
            return result
        except KeyError:
            print("HG lib does not seem to be installed.")


def getShortVersion():
    """
    Useful for tagging assets
    Inspired by the Makehuman Project
    """
    if __versionSub__:
        return __versionSub__.replace(' ', '_').lower()
    else:
        return "v" + getVersionDigitsStr()


# Gets the folder where Tangle.py is located
def _getCwd():
    """
    Retrieve the folder where Tangle.py is located.
    This is not necessarily the CWD.
    Inspired by the Makehuman Project
    """
    if isBuild():
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.realpath(__file__))


# Hacky, but hey, at least I don't have to make my own GUI then.
def _openHelp():
    """
    Internal function that displays the help
    whenever an error is encountered or the graphical
    help option is specified.
    """
    webbrowser.open(path + "/html/helpfiles/help.htm", 1)


# The handling of the command line arguments. I just love argparse.
def _parseArguments():
    """
    Internal function that parses the command line arguments.

    Returns:
    A list of apis to be used in this session
    """
    parser = ArgumentParser()
    parser.add_argument("-g", "--graphicalhelp",
                        help="displays a graphical help page", dest="helpme",
                        action="store_true")
    parser.add_argument("-a", "--api", help="provide a list of APIs to use" +
                        " for the data data is shown. Available per " +
                        "default:\n\tTwitter",
                        dest="apis")
    parser.add_argument("--version", help="displays the version number and" +
                        " exits.", dest="v", action="store_true")
    parser.add_argument("-d", "--devel", help="displays developer infos" +
                        " and exits.", dest="d", action="store_true")
    parser.add_argument("-f", help="creates a config file with default " +
                        "values.", dest="conf", action="store_true")
    parser.add_argument("-l", help="stores error log in a file.",
                        dest="l", action="store_true")
    parser.add_argument("--log", help="stores error log in a specifically " +
                        "named file. Overrides the '-l' option.",
                        dest="log")
    parser.add_argument("--syscheck", help="checks whether the " +
                        "dependencies are met and installs them if wanted.",
                        dest="s", action="store_true")
    options, unknown = parser.parse_known_args()

    # if unknown:
    #     print("The following arguments are unknown: ", unknown, "\n")
    #     parser.print_help()
    #     sys.exit(1)

    if options.helpme:
        _openHelp()
        sys.exit(0)

    if options.v:
        print("Tangle Version:", _versionStr())
        sys.exit(0)

    if options.d:
        _showDevel()
        sys.exit(0)

    if options.conf:
        _makeConfFile()
        sys.exit(0)

    if options.log:
        _logToFile(options.log)
    elif options.l:
        _logToFile()

    if options.s:
        _sysCheck()
        sys.exit(0)

    if not options.apis:
        from util.ConfigObject import ConfigObject
        config = ConfigObject(path + "/src/config.json")
        apis = config.configs.value("apis", "WorldBank")
        return apis if type(apis) is list else [apis]
    else:
        return options.apis.split(',')


def _makeApiObjects(apis):
    """
    Creates instances of API objects for every specified object if possible.

    Keyword arguments:
    apis -- a list of apis for which objects should be created
    """
    import sqlite3
    from plugins.APIInterface import APIInterface
    objects = []
    plugindir = os.listdir(path + "/src/plugins")
    db = sqlite3.connect(path + "/rc/creds.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS credentials(api_name " +
                   "TEXT PRIMARY KEY, authentication TEXT)")
    db_content = cursor.execute("SELECT api_name FROM credentials")
    for api in apis:
        if api == "Twitter":
            continue
        if api + ".py" in plugindir and api in db_content:
            credentials = cursor.execute("SELECT authentication FROM " +
                                         "credentials WHERE api_name=" +
                                         api)
            if credentials:
                impobj = getattr(__import__("plugins", fromlist=[api]), api)
                objects.append(APIInterface(api, impobj, credentials))
            else:
                print("Api", api, "could not be imported: No credentials.")
        elif api + ".py" in plugindir:
            impobj = getattr(getattr(__import__("plugins", fromlist=[api]),
                                     api), api)
            objects.append(APIInterface(api, impobj, []))
    return objects


def _showDevel():
    """
    Prints developer informations to stdout.
    """
    print("\033[92m####   General Information   ####\033[0m")
    print("Tangle Version:", _versionStr())
    print("Build:", isBuild())
    print("\n\033[91m####   KNOWN BUGS   ####\033[0m")
    with open(path + "/rc/KNOWN_BUGS", "r") as f:
        print(f.read())
    print("\n\033[93m####   PLANNED FEATURES   ####\033[0m")
    with open(path + "/rc/PLANNED_FEATURES", "r") as f:
        print(f.read())


def _logToFile(logfile=None):
    """
    Redirects stdout and stderr to file.
    """
    if not logfile:
        import datetime
        logfile = "Log" + str(datetime.datetime.now()) + ".log"
    with open(path + "/logging/" + logfile, "a") as f:
        sys.stderr = f
        sys.stdout = f


def _makeConfFile():
    """
    Creates a Configuration File with default values.
    """
    gname = input("Which account name would you like to use " +
                  "for authentication at geonames?")
    from PyQt5.QtCore import QSettings
    settings = QSettings("FKI", "Detanglement")
    settings.setValue("apis", ["WorldBank"])
    settings.setValue("geo_location", False)
    settings.setValue("gnames", gname)
    settings.setValue("map", "google")
    # try:
    #     open(path + "/src/config.json", "r")
    #     choice = input("File already exists. Should it be overridden with " +
    #                    "default values?")
    #     if choice in ["y", "yes", "YES", "Yes"]:
    #         raise FileNotFoundError
    # except FileNotFoundError:
    #     import json
    #     with open(path + "/src/config.json", "w+") as f:
    #         gname = input("Which account name would you like to use " +
    #                       "for authentication at geonames?")
    #         f.write(json.dumps({"apis": ["Twitter"],
    #                             "geo_location": False,
    #                             "gnames": gname,
    #                             "map": "google"}))
    #         f.close()


def _sysCheck():
    """
    It is checked whether the dependencies for the application are met.
    """
    from util import SystemCheck
    SystemCheck.check()


def main():
    """
    The main function. The arguments are parsed and the GUI is launched.
    Not much to it, really.
    """
    global path
    path += _getCwd()[:-4]

    apis = _parseArguments()
    api_objects = _makeApiObjects(apis)

    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    from widgets.TangleUI import TangleUI
    menu = TangleUI(api_objects, app, path, "/src/config.json")
    sys.exit(app.exec_())

# Yay, a main module!
if __name__ == "__main__":
    main()
