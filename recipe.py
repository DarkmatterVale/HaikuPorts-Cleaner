class Recipe():
    """
    Parses an individual recipe and fixes it.
    """

    def __init__(self, baseDir, name):
        # Set up the ordering for recipe files
        self.component_ordering = [
            "SUMMARY",
            "DESCRIPTION",
            "HOMEPAGE"
        ]

        self.baseDir = baseDir
        self.name = name

    def clean(self):
        """
        Fix the given recipe
        """
        # Read the file

        # Apply cleaning. This entails fixing:
        # - Ordering

        # Fix ordering

        # Save new data to file
