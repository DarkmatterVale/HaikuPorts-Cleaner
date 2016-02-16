from Options import getOption
from Recipe import RecipeFixer

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

        # Setting build-dependent variables
        self.directory = getOption("directory")

        # Cleaning all files within the base directory
        self.clean_directory(self.directory)

        # Alerting the user that the process is done
        print("All recipes have been corrected...")

    def clean_directory(self, directory_to_clean):
        """
        Cleans the main haikuports directory & all its subfolders
        """
        for root, dirs, files in os.walk(directory_to_clean):
            path = root.split('/')
            print (len(path) - 1) *'---' , os.path.basename(root)
            for test_file in files:
                if test_file.endswith(".recipe"):
                    print len(path)*'---', test_file
                    current_recipe_fixer = RecipeFixer(root, test_file)
                    current_recipe_fixer.clean()
                    exit(0)
