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
            ['{', '}', "BUILD()", "\n", "\n"],
            ['{', '}', "INSTALL()", "\n", "\n"]
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

        # Apply cleaning. This entails fixing:
        # - Ordering

        # Fix ordering
        self.corrected_content = self.correct_ordering()

        # Save new data to file
        with open(os.path.join("/Users/vtolpegin/Desktop", self.name), 'w') as content_file:
            content_file.write(self.corrected_content)

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

                    left_quote_index = component_text.find(component[0])
                    right_quote_index = component_text[left_quote_index + 1:].find(component[1])

                    while str(component_text[(left_quote_index + right_quote_index):(left_quote_index + right_quote_index + 1)]) == "\\":
                        right_quote_index += component_text[left_quote_index + right_quote_index + 2:].find(component[1]) + 1

                    #print(component[2] + component[3] + component_text[left_quote_index:(left_quote_index + right_quote_index + 2)])
                    for component_part in component[4:]:
                        ordered_content += component_part
                    ordered_content += component[2] + component[3] + component_text[left_quote_index:(left_quote_index + right_quote_index + 2)] + "\n"
                else:
                    left_index = 0
                    right_index = 0

                    component_text = original_content_copy[original_content_copy.index(component[2]):]

                    left_quote_index = component_text.find(component[0])
                    right_quote_index = component_text[left_quote_index + 1:].find(component[1])
                    left_index += 1
                    right_index += 1

                    inner_left_quote_index = left_quote_index
                    break_while = False
                    while not break_while:
                        inner_left_index = len(re.findall(component[0], component_text[inner_left_quote_index + 1:inner_left_quote_index + right_quote_index + 2]))

                        if inner_left_index > 0:
                            left_index += inner_left_index

                            temp_inner_left_quote_index = right_quote_index + 2
                            temp_right_quote_index = component_text[inner_left_quote_index + right_quote_index + 2:].find(component[1])
                            if temp_right_quote_index != -1:
                                right_index += 1
                                right_quote_index += temp_right_quote_index + 1
                            inner_left_quote_index = temp_inner_left_quote_index
                        else:
                            while left_index > right_index:
                                right_quote_index += component_text[left_quote_index + right_quote_index + 2:].find(component[1]) + 1
                                right_index += 1

                            break_while = True

                    #print(component[2] + component[3] + component_text[left_quote_index:(left_quote_index + right_quote_index + 2)])
                    for component_part in component[4:]:
                        ordered_content += component_part
                    ordered_content += component[2] + component[3] + component_text[left_quote_index:(left_quote_index + right_quote_index + 2)] + "\n"

        # Return the final components
        return ordered_content
