#!/usr/bin/env python3

import os
import sys
import subprocess

def check():
    print("##### System Information #####\n")
    print("Platform:", sys.platform)
    print("Operating System:", os.name)
    print("Python:", sys.version.replace("\n", "")+ "\n")

    print("\n\n##### System Status #####")
    print("\n## Tangle Requirements ##")

    core_err = []
    core_info = []

    try:
        import pygeoip
        print("PyGeoIp:", pygeoip.__version__)
    except:
        print("PyGeoIp:", "missing")
        core_err.append("Please install pygeoip to use Tangle.")


    try:
        import geopy
        print("geopy:", "up and working")
    except:
        print("geopy:", "missing")
        core_err.append("Please install geopy to use Tangle.")

    try:
        import TwitterAPI
        print("TwitterAPI:", TwitterAPI.__version__)
    except:
        print("TwitterAPI:", "missing")
        core_err.append("Please install TwitterAPI to use Tangle.")

    try:
        from PyQt5 import QtCore
        print("pyqt:", QtCore.PYQT_VERSION_STR)
    except:
        print("pyqt:", "missing")
        core_err.append("Please install PyQt4 to use Tangle.")

    try:
        import kartograph
        print("kartograph:", "up and working")
    except:
        print("kartograph:", "missing")
        core_info.append("You might want to install Kartograph if " +
                         "you want to use SVG-based maps.")

    if sys.version_info < (3, 0):
        core_err.append("Your python version is too old, Please use " +
                        "at least Python 3.0")

    if core_info:
        print("\n\033[93mPossible improvements for Tangle:\n")
        for line in core_info:
            print(line)

    if core_err:
        print("\n\033[91mThe system check has detected some errors:\n")
        for err in core_err:
            print(err)
        choice = input("\nShould the dependencies be installed " +
                        "automatically?[y/n]\033[0m")
        if choice in ["y", "Y", "YES", "Yes", "yes"]:
            if __name__ == "__main__":
                okay = subprocess.call(["sh", "dependencies.sh"])
            else:
                okay = subprocess.call(["sh", "utils/dependencies.sh"])
            if okay == 0:
                core_err = False

    if not core_err:
        print("\n\033[92mNo real Problems detected, Tangle should work.\n")
        choice = input("\nShould it be installed automatically?[y/n]\033[0m")
        if choice in ["y", "Y", "YES", "Yes", "yes"]:
            if __name__ == "__main__":
                subprocess.call(["sh", "install.sh"])
            else:
                subprocess.call(["sh", "utils/install.sh"])

    print("\033[0m")


if __name__ == "__main__":
    check()
