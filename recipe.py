import os
import re


class RecipeFixer():
    """
    Parses an individual recipe and fixes it.
    """

    def __init__(self, baseDir, name):
        # Set up the ordering for recipe files
        self.order = [
            "SUMMARY",
            "DESCRIPTION",
            "HOMEPAGE",
            "COPYRIGHT",
            "LICENSE",
            "REVISION",
            "SOURCE_URI",
            "CHECKSUM_SHA256",
            "SOURCE_DIR",
            "PATCHES",
            "ADDITIONAL_FILES",
            "ARCHITECTURES",
            "SECONDARY_ARCHITECTURES",
            "PROVIDES",
            "REQUIRES",
            "PROVIDES_devel",
            "REQUIRES_devel",
            "BUILD_REQUIRES",
            "BUILD_PREREQUIRES",
            "PATCH()",
            "BUILD()",
            "INSTALL()",
            "TEST()",
        ]
        self.component_ordering = {
            "SUMMARY" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "SUMMARY",
                "join" : "=",
                "pre_requests" : []
            },
            "DESCRIPTION" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "DESCRIPTION",
                "join" : "=",
                "pre_requests" : []
            },
            "HOMEPAGE" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "HOMEPAGE",
                "join" : "=",
                "pre_requests" : []
            },
            "COPYRIGHT" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "COPYRIGHT",
                "join" : "=",
                "pre_requests" : []
            },
            "LICENSE" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "LICENSE",
                "join" : "=",
                "pre_requests" : []
            },
            "REVISION" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "REVISION",
                "join" : "=",
                "pre_requests" : []
            },
            "SOURCE_URI" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "SOURCE_URI",
                "join" : "=",
                "pre_requests" : []
            },
            "CHECKSUM_SHA256" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "CHECKSUM_SHA256",
                "join" : "=",
                "pre_requests" : []
            },
            "SOURCE_DIR" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "SOURCE_DIR",
                "join" : "=",
                "pre_requests" : []
            },
            "PATCHES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "PATCHES",
                "join" : "=",
                "pre_requests" : []
            },
            "ADDITIONAL_FILES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "ADDITIONAL_FILES",
                "join" : "=",
                "pre_requests" : []
            },
            "ARCHITECTURES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "ARCHITECTURES",
                "join" : "=",
                "pre_requests" : ["\n"]
            },
            "SECONDARY_ARCHITECTURES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "SECONDARY_ARCHITECTURES",
                "join" : "=",
                "pre_requests" : []
            },
            "PROVIDES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "PROVIDES",
                "join" : "=",
                "pre_requests" : ["\n"]
            },
            "REQUIRES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "REQUIRES",
                "join" : "=",
                "pre_requests" : []
            },
            "PROVIDES_devel" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "PROVIDES_devel",
                "join" : "=",
                "pre_requests" : ["\n"]
            },
            "REQUIRES_devel" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "REQUIRES_devel",
                "join" : "=",
                "pre_requests" : []
            },
            "BUILD_REQUIRES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "BUILD_REQUIRES",
                "join" : "=",
                "pre_requests" : ["\n"]
            },
            "BUILD_PREREQUIRES" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "BUILD_PREREQUIRES",
                "join" : "=",
                "pre_requests" : []
            },
            "PATCH()" : {
                "begin_id" : '{',
                "end_id" : '}',
                "name" : "PATCH()",
                "join" : "\n",
                "pre_requests" : ["\n"]
            },
            "BUILD()" : {
                "begin_id" : '{',
                "end_id" : '}',
                "name" : "BUILD()",
                "join" : "\n",
                "pre_requests" : ["\n"]
            },
            "INSTALL()" : {
                "begin_id" : '{',
                "end_id" : '}',
                "name" : "INSTALL()",
                "join" : "\n",
                "pre_requests" : ["\n"]
            },
            "TEST()" : {
                "begin_id" : '{',
                "end_id" : '}',
                "name" : "TEST()",
                "join" : "\n",
                "pre_requests" : ["\n"]
            }
        }

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
        if not self.should_clean_recipe(self.content):
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
        for component in self.order:
            original_content_copy = str(self.content)
            #self.extract_component(original_content_copy, component)
            if self.component_ordering[component]["name"] in original_content_copy:
                if self.component_ordering[component]["begin_id"] == self.component_ordering[component]["end_id"]:
                    find_index = original_content_copy.index(self.component_ordering[component]["name"])
                    component_text = original_content_copy[find_index:]

                    start_index = component_text.find(self.component_ordering[component]["begin_id"])
                    end_index = component_text[start_index + 1:].find(self.component_ordering[component]["end_id"])

                    while str(component_text[(start_index + end_index):(start_index + end_index + 1)]) == "\\":
                        end_index += component_text[start_index + end_index + 2:].find(self.component_ordering[component]["end_id"]) + 1

                    for component_part in self.component_ordering[component]["pre_requests"]:
                        ordered_content += component_part
                    ordered_content += self.component_ordering[component]["name"] +self. component_ordering[component]["join"] + component_text[start_index:(start_index + end_index + 2)] + "\n"
                else:
                    nesting_index = 0
                    find_index = original_content_copy.index(self.component_ordering[component]["name"])
                    component_text = original_content_copy[find_index:]

                    start_index = component_text.find(self.component_ordering[component]["begin_id"])
                    end_index = start_index + 1
                    nesting_index += 1

                    while nesting_index > 0:# and end_index < len(component_text):
                        if self.component_ordering[component]["begin_id"] in component_text[end_index:end_index + 1]:
                            nesting_index += 1
                        elif self.component_ordering[component]["end_id"] in component_text[end_index:end_index + 1]:
                            nesting_index -= 1
                        end_index += 1

                    for component_part in self.component_ordering[component]["pre_requests"]:
                        ordered_content += component_part
                    ordered_content += self.component_ordering[component]["name"] + self.component_ordering[component]["join"] + component_text[start_index:end_index] + "\n"

        # Return the final components
        return ordered_content

    def should_clean_recipe(self, content):
        """
        If the recipe detects something that should not be placed inside of
        it, the cleaner should skip the recipe.
        """
        content_copy = str(content)

        # For each component, go through the recipe, find it, and correctly
        #   place it into the new recipe
        for component in self.order:
            if self.component_ordering[component]["name"] in content_copy:
                if self.component_ordering[component]["begin_id"] == self.component_ordering[component]["end_id"]:
                    find_index = content_copy.index(self.component_ordering[component]["name"])
                    component_text = content_copy[find_index:]

                    start_index = component_text.find(self.component_ordering[component]["begin_id"])
                    end_index = component_text[start_index + 1:].find(self.component_ordering[component]["end_id"])

                    while str(component_text[(start_index + end_index):(start_index + end_index + 1)]) == "\\":
                        end_index += component_text[start_index + end_index + 2:].find(self.component_ordering[component]["end_id"]) + 1

                    ordered_content = self.component_ordering[component]["name"] + self.component_ordering[component]["join"]
                    content_copy = content_copy[:find_index] + component_text[:(start_index - len(ordered_content))] + component_text[(start_index + end_index + 2):]
                else:
                    nesting_index = 0
                    find_index = content_copy.index(self.component_ordering[component]["name"])
                    component_text = content_copy[content_copy.index(self.component_ordering[component]["name"]):]

                    start_index = component_text.find(self.component_ordering[component]["begin_id"])
                    end_index = start_index + 1
                    nesting_index += 1

                    while nesting_index > 0:# and end_index < len(component_text):
                        if self.component_ordering[component]["begin_id"] in component_text[end_index:end_index + 1]:
                            nesting_index += 1
                        elif self.component_ordering[component]["end_id"] in component_text[end_index:end_index + 1]:
                            nesting_index -= 1
                        end_index += 1

                    ordered_content = self.component_ordering[component]["name"] + self.component_ordering[component]["join"]
                    content_copy = content_copy[:find_index] + component_text[:(start_index - len(ordered_content))] + component_text[(end_index + 1):]

        if self.remove_whitespace(content_copy) != "":
            return False

        return True

    def extract_component(self, text, component_name):
        """
        Returns the start and end index for the component with the name
        component_name. It not only identifies the start and end index, but
        will also grab any additional data that is critical (or in the recipe)
        """
        # Setting up indexes
        component_start_index = -1
        component_end_index = -1
        component = component_name

        # Detecting previous component
        if self.component_ordering[component]["name"] in text:
            if self.component_ordering[component]["begin_id"] == self.component_ordering[component]["end_id"]:
                component_start_index = text.index(self.component_ordering[component]["name"])
                component_text = text[component_start_index:]

                start_index = component_text.find(self.component_ordering[component]["begin_id"])
                end_index = component_text[start_index + 1:].find(self.component_ordering[component]["end_id"])

                while str(component_text[(start_index + end_index):(start_index + end_index + 1)]) == "\\":
                    end_index += component_text[start_index + end_index + 2:].find(self.component_ordering[component]["end_id"]) + 1

                component_end_index = component_start_index + start_index + end_index + 2
            else:
                nesting_index = 0
                component_start_index = text.index(self.component_ordering[component]["name"])
                component_text = text[component_start_index:]

                start_index = component_text.find(self.component_ordering[component]["begin_id"])
                end_index = start_index + 1
                nesting_index += 1

                while nesting_index > 0:
                    if self.component_ordering[component]["begin_id"] in component_text[end_index:end_index + 1]:
                        nesting_index += 1
                    elif self.component_ordering[component]["end_id"] in component_text[end_index:end_index + 1]:
                        nesting_index -= 1
                    end_index += 1

                component_end_index = component_start_index + end_index + 2

        print("---" + component_name + "---")
        print(str(text[component_start_index:component_end_index]))
        print("---DONE---")

        return component_start_index, component_end_index

    def remove_whitespace(self, text):
        """
        Removes all whitespace in the text and returns whatever is remaining.
        """

        return "".join(text.split())
