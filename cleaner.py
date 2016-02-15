from Options import getOption

import os


class Cleaner():
    """
    Main class for the ports cleaner. This class handles the management of
    each individual "clean" task/process
    """

    def __init__(self, options, args):
        """
        Clean the haikuports tree
        """
        print(getOption("directory"))

        # Setting build-dependent variables
        self.directory = getOption("directory")

        # Cleaning all files within the base directory
        self.clean_directory(self.directory)

        # Alerting the user that the process is done
        print("All recipes have been corrected...")
