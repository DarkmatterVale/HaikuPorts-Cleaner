import os
import re


class RecipeFixer():
    """
    Parses an individual recipe and fixes it.
    """

    def __init__(self, baseDir, name):
        # Set up the ordering for recipe files
        self.component_ordering = [
            ['"', '"', "SUMMARY", "="],
            ['"', '"', "DESCRIPTION", "="],
            ['"', '"', "HOMEPAGE", "="],
            ['"', '"', "COPYRIGHT", "="],
            ['"', '"', "LICENSE", "="],
            ['"', '"', "REVISION", "="],
            ['"', '"', "SOURCE_URI", "="],
            ['"', '"', "CHECKSUM_SHA256", "="],
            ['"', '"', "SOURCE_DIR", "="],
            ['"', '"', "PATCHES", "="],
            ['"', '"', "ADDITIONAL_FILES", "="],
            ['"', '"', "ARCHITECTURES", "=", "\n"],
            ['"', '"', "SECONDARY_ARCHITECTURES", "="],
            ['"', '"', "PROVIDES", "=", "\n"],
            ['"', '"', "REQUIRES", "="],
            ['"', '"', "PROVIDES_devel", "=", "\n"],
            ['"', '"', "REQUIRES_devel", "="],
            ['"', '"', "BUILD_REQUIRES", "=", "\n"],
            ['"', '"', "BUILD_PREREQUIRES", "="],
            ['{', '}', "PATCH()", "\n", "\n"],
            ['{', '}', "BUILD()", "\n", "\n"],
            ['{', '}', "INSTALL()", "\n", "\n"],
            ['{', '}', "TEST()", "\n", "\n"]
        ]

        # Set up the current removal conditions for recipes.
        #   This should not be in the final version. For now, we just want
        #   to fix ordering so we do not need to worry about this.
        self.cancel_conditions = [
            "DEPEND",
            "\nif"
        ]

        # Setting variables
        self.baseDir = baseDir
        self.name = name

    def clean(self):
        """
        Fix the given recipe
        """
        # Reset variables
        self.content = ""
        self.corrected_content = ""

        # Read the file
        with open(os.path.join(self.baseDir, self.name), 'r') as content_file:
            self.content = content_file.read()
            content_file.close()

        # Determine whether to cancel the cleaning or not
        if not self.clean_recipe(self.content):
            return

        # Apply cleaning. This entails fixing:
        # - Ordering

        # Fix ordering
        self.corrected_content = self.correct_ordering()

        # Save new data to file
        with open(os.path.join(self.baseDir, self.name), 'w') as content_file:
            content_file.seek(0)
            content_file.write(self.corrected_content)
            content_file.close()

    def correct_ordering(self):
        """
        Corrects the ordering of the content within recipes
        """
        original_content = self.content
        ordered_content = ""

        # For each component, go through the recipe, find it, and correctly
        #   place it into the new recipe
        for component in self.component_ordering:
            original_content_copy = str(self.content)
            if component[2] in original_content_copy:
                if component[0] == component[1]:
                    component_text = original_content_copy[original_content_copy.index(component[2]):]

                    start_index = component_text.find(component[0])
                    end_index = component_text[start_index + 1:].find(component[1])

                    while str(component_text[(start_index + end_index):(start_index + end_index + 1)]) == "\\":
                        end_index += component_text[start_index + end_index + 2:].find(component[1]) + 1

                    #print(component[2] + component[3] + component_text[start_index:(start_index + end_index + 2)])
                    for component_part in component[4:]:
                        ordered_content += component_part
                    ordered_content += component[2] + component[3] + component_text[start_index:(start_index + end_index + 2)] + "\n"
                else:
                    nesting_index = 0

                    component_text = original_content_copy[original_content_copy.index(component[2]):]

                    start_index = component_text.find(component[0])
                    end_index = start_index + 1
                    nesting_index += 1

                    while nesting_index > 0:
                        if component[0] in component_text[end_index:end_index + 1]:
                            nesting_index += 1

                        elif component[1] in component_text[end_index:end_index + 1]:
                            nesting_index -= 1
                        end_index += 1

                    #print(component[2] + component[3] + component_text[start_index:end_index])
                    for component_part in component[4:]:
                        ordered_content += component_part
                    ordered_content += component[2] + component[3] + component_text[start_index:end_index] + "\n"

        # Return the final components
        return ordered_content

    def clean_recipe(self, content):
        """
        If the recipe detects something that should not be placed inside of
        it, the cleaner should skip the recipe.
        """
        content_copy = str(content)

        # For each component, go through the recipe, find it, and correctly
        #   place it into the new recipe
        for component in self.component_ordering:
            if component[2] in content_copy:
                if component[0] == component[1]:
                    find_index = content_copy.index(component[2])
                    component_text = content_copy[find_index:]

                    start_index = component_text.find(component[0])
                    end_index = component_text[start_index + 1:].find(component[1])

                    while str(component_text[(start_index + end_index):(start_index + end_index + 1)]) == "\\":
                        end_index += component_text[start_index + end_index + 2:].find(component[1]) + 1

                    #print(component[2] + component[3] + component_text[start_index:(start_index + end_index + 2)])
                    ordered_content = component[2] + component[3]#+ component_text[start_index:end_index] + "\n"
                    content_copy = content_copy[:find_index] + component_text[:(start_index - len(ordered_content))] + component_text[(start_index + end_index + 2):]
                else:
                    nesting_index = 0
                    find_index = content_copy.index(component[2])
                    component_text = content_copy[content_copy.index(component[2]):]

                    start_index = component_text.find(component[0])
                    end_index = start_index + 1
                    nesting_index += 1

                    while nesting_index > 0:
                        if component[0] in component_text[end_index:end_index + 1]:
                            nesting_index += 1

                        elif component[1] in component_text[end_index:end_index + 1]:
                            nesting_index -= 1
                        end_index += 1

                    #print(component[2] + component[3] + component_text[start_index:end_index])
                    ordered_content = component[2] + component[3]#+ component_text[start_index:end_index] + "\n"
                    content_copy = content_copy[:find_index] + component_text[:(start_index - len(ordered_content))] + component_text[(end_index + 1):]

        if self.remove_whitespace(content_copy) != "":
            return False

        return True

    def remove_whitespace(self, text):
        """
        Removes all whitespace in the text and returns whatever is remaining.
        """

        return "".join(text.split())
