#!/usr/bin/env python3

import json
from PyQt5.QtCore import QSettings


class ConfigObject():
    """Class for parsing the json config file"""
    # initializes the class. A conf file name is needed
    def __init__(self, config_file):
        """
        Initializes the class

        Keyword Arguments:
        config_file -- string representation of the config file name
        """
        self.config_file = config_file
        self.configs = QSettings("FKI", "Detanglement")

    # internal function; parses the config.
    def _parseConfFile(self):
        """
        Internal function which parses the config
        file. It will fail miserably when the config
        file is faulty. This will hurt me very much.

        Returns:
        data -- data which was parsed
        """
        return {key: self.settings.value(key) for key
                in self.settings.allKeys()}

    def refresh(self):
        """
        Refreshes the configuration in case a different object changed
        something.
        """
        # self.configs = self._parseConfFile()
        pass

    def save(self):
        """Saves the momentary configurations into the json file"""
        pass
        # try:
        #     with open(self.config_file, "w") as f:
        #         f.write(json.dumps(self.configs))
        #         f.close()
        # except IOError as e:
        #     print("Config File could not be found. Please run Tangle " +
        #           "again with the -f option set.")
        #     raise e


# Not a main module
if __name__ == "__main__":
    raise ImportError("This is not supposed to be a main module.")
