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

        # Setting up log file
        self.logFile = "log"
        with open(os.path.join(os.getcwd(), self.logFile), 'w') as log_file:
            log_file.write("")
            log_file.close()

        # Cleaning all files within the base directory
        self.clean_directory(self.directory)

        # Creating a timer for the end of the program
        stop = timeit.default_timer()

        # Printing the total time it took to run the program
        print("Total time to clean " + self.directory + " : " + str(stop - start) + " seconds")

    def clean_directory(self, directory_to_clean):
        """
        Cleans the main haikuports directory & all its subfolders
        """
        total_recipes = self.tally_recipes(directory_to_clean)
        recipe_index = 0
        for root, dirs, files in os.walk(directory_to_clean):
            path = root.split('/')
            print (len(path) - 1) *'---' , os.path.basename(root)
            for test_file in files:
                if test_file.endswith(".recipe"):
                    recipe_index += 1
                    print len(path)*'---', test_file, ' ', recipe_index, '/', total_recipes
                    current_recipe_fixer = RecipeFixer(root, test_file, self.logFile)
                    current_recipe_fixer.clean()

        # Printing out the total recipe count
        print("Cleaned " + str(recipe_index) + " recipes")

    def tally_recipes(self, base_directory):
        """
        Returns the total number of recipes located within the directory
        base_directory
        """
        total_recipes = 0
        for root, dirs, files in os.walk(base_directory):
            for test_file in files:
                if test_file.endswith(".recipe"):
                    total_recipes += 1

        return total_recipes
