from Options import getOption
from Recipe import RecipeFixer

import os
import timeit


class Cleaner():
    """
    Main class for the ports cleaner. This class handles the management of
    each individual "clean" task/process
    """

    def __init__(self, options, args):
        """
        Clean the haikuports tree
        """
        # Creating a timer for the start of the program
        start = timeit.default_timer()

        # Setting build-dependent variables
        self.directory = getOption("directory")

        # Cleaning all files within the base directory
        self.clean_directory(self.directory)

        # Creating a timer for the end of the program
        stop = timeit.default_timer()

        # Alerting the user that the process is done
        print("All recipes have been corrected...")

        # Printing the total time it took to run the program
        print("Total time to clean " + self.directory + " : " + str(stop - start))

    def clean_directory(self, directory_to_clean):
        """
        Cleans the main haikuports directory & all its subfolders
        """
        recipe_index = 0
        for root, dirs, files in os.walk(directory_to_clean):
            path = root.split('/')
            print (len(path) - 1) *'---' , os.path.basename(root)
            for test_file in files:
                if test_file.endswith(".recipe"):
                    print len(path)*'---', test_file
                    current_recipe_fixer = RecipeFixer(root, test_file)
                    current_recipe_fixer.clean()
                    recipe_index += 1

        # Printing out the total recipe count
        print("Cleaned " + str(recipe_index) " recipes")
