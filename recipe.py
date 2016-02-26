import os
import re


class RecipeFixer():
    """
    Parses an individual recipe and fixes it.
    """

    def __init__(self, baseDir, name, log):
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

        # Setting up logging information
        self.logFile = log

        # Setting general variables
        self.baseDir = baseDir
        self.name = name

    def clean(self):
        """
        Fix the given recipe
        """
        # Reset variables
        self.content = ""
        self.corrected_content = ""
        self.logData = ""

        # Read the recipe file
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

        # Save new data to the recipe file
        with open(os.path.join(self.baseDir, self.name), 'w') as content_file:
            content_file.seek(0)
            content_file.write(self.corrected_content)
            content_file.close()

        # Save the log data
        with open(os.path.join(os.getcwd(), self.logFile), 'a') as log_file:
            log_file.write(self.logData)
            log_file.close()

    def correct_ordering(self):
        """
        Corrects the ordering of the content within recipes
        """
        original_content = self.content
        ordered_content = ""
        extracted_component_list = {}

        # Adding log data
        self.logData += ("*" * 70) + "\n"
        self.logData += re.sub(".recipe", "", self.name) + "\n"
        self.logData += ("*" * 70) + "\n"

        # For each component, go through the recipe, find it, and correctly
        #   place it into the new recipe
        extraction_text = str(original_content)
        for component in self.order:
            start_, end_ = self.extract_component(str(self.content), component)
            start_text, end_test = self.extract_component(extraction_text, component)

            if start_text != -1 and end_test != -1:
                if len(self.remove_whitespace(extraction_text[:start_text])) == 0:
                    extraction_text = extraction_text[:start_text] + extraction_text[end_test + 1:]

                    extracted_component_list[component] = {
                        "text" : str(self.content)[start_:end_] + "\n"
                    }

        # Correcting mistakes in each component
        for component in self.order:
            # Correcting SUMMARY related issues
            if component == "SUMMARY" and "SUMMARY" in extracted_component_list:
                # Make sure it is only one line long
                if len(extracted_component_list[component]["text"]) > 70:
                    print("\033[91mERROR: \033[00m{}".format("SUMMARY must be less than 80 characters long"))
                    self.logData += "WARNING: SUMMARY must be less than 70 characters long\n"
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    extracted_component_list[component]["text"] = re.sub(r"\n", "", extracted_component_list[component]["text"]) + "\n"
                    self.logData += "WARNING: Removing extra newline characters in SUMMARY\n"

                # Make sure it does not end in a period
                end_character_index = self.find_previous_non_whitespace_character(extracted_component_list[component]["text"], [self.component_ordering[component]["end_id"]], 1)
                if end_character_index != -1:
                    if "." == extracted_component_list[component]["text"][end_character_index]:
                        extracted_component_list[component]["text"] = extracted_component_list[component]["text"][:end_character_index] + extracted_component_list[component]["text"][(end_character_index + 1):]
                        self.logData += "WARNING: Removing extra period at the end of SUMMARY\n"
            elif component == "SUMMARY" and "SUMMARY" not in extracted_component_list:
                print("\033[91mERROR: \033[00m{}".format("Cannot find SUMMARY in recipe"))
                self.logData += "ERROR: Cannot find SUMMARY in recipe\n"

            # Correcting DESCRIPTION related issues
            if component == "DESCRIPTION" and "DESCRIPTION" in extracted_component_list:
                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(extracted_component_list[component]["text"], [self.component_ordering[component]["end_id"]], 1)
                if end_character_index != -1:
                    extracted_component_list[component]["text"] = extracted_component_list[component]["text"][:(end_character_index + 1)] + self.component_ordering[component]["end_id"] + "\n"
            elif component == "DESCRIPTION" and "DESCRIPTION" not in extracted_component_list:
                print("\033[91mERROR: \033[00m{}".format("Cannot find DESCRIPTION in recipe"))
                self.logData += "ERROR: Cannot find DESCRIPTION in recipe\n"

            # Correcting PROVIDES related issues
            if component == "PROVIDES" and "PROVIDES" in extracted_component_list:
                # Removing extra new line characters
                lines = extracted_component_list[component]["text"].split("\n")
                for line_index in range(0, len(lines)):
                    if self.remove_whitespace(lines[line_index]) == "":
                        lines[line_index] = ""
                    else:
                        lines[line_index] += "\n"
                extracted_component_list[component]["text"] = "".join(lines)

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(extracted_component_list[component]["text"], [self.component_ordering[component]["end_id"]], 1)
                if end_character_index != -1:
                    extracted_component_list[component]["text"] = extracted_component_list[component]["text"][:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"
            elif component == "PROVIDES" and "PROVIDES" not in extracted_component_list:
                extracted_component_list["PROVIDES"] = {
                    "text" : "PROVIDES=\"\n\t" + re.sub("-.*", "", self.name) + " = $portVersion\n\t\"\n"
                }
                self.logData += "WARNING: Adding dummy missing PROVIDES in recipe"

            # Correcting REQUIRES related issues
            if component == "REQUIRES" and "REQUIRES" in extracted_component_list:
                # Removing extra new line characters
                lines = extracted_component_list[component]["text"].split("\n")
                for line_index in range(0, len(lines)):
                    if self.remove_whitespace(lines[line_index]) == "":
                        lines[line_index] = ""
                    else:
                        lines[line_index] += "\n"
                extracted_component_list[component]["text"] = "".join(lines)

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(extracted_component_list[component]["text"], [self.component_ordering[component]["end_id"]], 1)
                if end_character_index != -1:
                    extracted_component_list[component]["text"] = extracted_component_list[component]["text"][:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"
            elif component == "REQUIRES" and "REQUIRES" not in extracted_component_list:
                extracted_component_list["REQUIRES"] = {
                    "text" : "REQUIRES=\"\n\thaiku\n\t\"\n"
                }
                self.logData += "WARNING: Adding dummy missing REQUIRES in recipe"

            # Correcting PROVIDES_devel related issues
            if component == "PROVIDES_devel" and "PROVIDES_devel" in extracted_component_list:
                # Removing extra new line characters
                lines = extracted_component_list[component]["text"].split("\n")
                for line_index in range(0, len(lines)):
                    if self.remove_whitespace(lines[line_index]) == "":
                        lines[line_index] = ""
                    else:
                        lines[line_index] += "\n"
                extracted_component_list[component]["text"] = "".join(lines)

                # Make sure there is a REQUIRES_devel component in the recipe
                if "REQUIRES_devel" not in extracted_component_list:
                    if "SECONDARY_ARCHITECTURES" in extracted_component_list:
                        extracted_component_list["REQUIRES_devel"] = {
                            "text" : "REQUIRES_devel=\"\n\thaiku$\{secondaryArchSuffix\}_devel\n\t\"\n"
                        }
                        self.logData += "WARNING: Adding missing REQUIRES_devel component\n"
                    else:
                        extracted_component_list["REQUIRES_devel"] = {
                            "text" : "REQUIRES_devel=\"\n\thaiku_devel\n\t\"\n"
                        }
                        self.logData += "WARNING: Adding missing REQUIRES_devel component\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(extracted_component_list[component]["text"], [self.component_ordering[component]["end_id"]], 1)
                if end_character_index != -1:
                    extracted_component_list[component]["text"] = extracted_component_list[component]["text"][:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

            # Correcting REQUIRES_devel related issues
            if component == "REQUIRES_devel" and "REQUIRES_devel" in extracted_component_list:
                # Removing extra new line characters
                lines = extracted_component_list[component]["text"].split("\n")
                for line_index in range(0, len(lines)):
                    if self.remove_whitespace(lines[line_index]) == "":
                        lines[line_index] = ""
                    else:
                        lines[line_index] += "\n"
                extracted_component_list[component]["text"] = "".join(lines)

                # Make sure there is a PROVIDES_devel component in the recipe
                if "PROVIDES_devel" not in extracted_component_list:
                    if "SECONDARY_ARCHITECTURES" in extracted_component_list:
                        extracted_component_list["PROVIDES_devel"] = {
                            "text" : "PROVIDES_devel=\"\n\t" + re.sub("-.*", "", self.name) + "$\{secondaryArchSuffix\}_devel = $portVersion\n\t\"\n"
                        }
                        self.logData += "WARNING: Adding missing PROVIDES_devel component\n"
                    else:
                        extracted_component_list["PROVIDES_devel"] = {
                            "text" : "PROVIDES_devel=\"\n\t" + re.sub("-.*", "", self.name) + "_devel = $portVersion\n\t\"\n"
                        }
                        self.logData += "WARNING: Adding missing PROVIDES_devel component\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(extracted_component_list[component]["text"], [self.component_ordering[component]["end_id"]], 1)
                if end_character_index != -1:
                    extracted_component_list[component]["text"] = extracted_component_list[component]["text"][:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

        # Assembling final information
        for component in self.order:
            if component in extracted_component_list:
                for component_part in self.component_ordering[component]["pre_requests"]:
                    ordered_content += component_part
                ordered_content += extracted_component_list[component]["text"]

        # Cleaning up log file
        self.logData += "\n"

        # Return the final components
        return ordered_content


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

                component_end_index = component_start_index + end_index

        return component_start_index, component_end_index

    def should_clean_recipe(self, content):
        """
        If the recipe detects something that should not be placed inside of
        it, the cleaner should skip the recipe.
        """
        content_copy = str(content)

        # For each component, go through the recipe, find it, and remove
        #   it from the cleaner
        for component in self.order:
            start_index, end_index = self.extract_component(content_copy, component)
            if start_index != -1 and end_index != -1:
                if len(self.remove_whitespace(content_copy[:start_index])) == 0:
                    content_copy = content_copy[:start_index] + content_copy[end_index + 1:]

        if self.remove_whitespace(content_copy) != "":
            self.logData += "ERROR: Cannot parse recipe file with unknown content"
            return False

        return True

    def remove_whitespace(self, text):
        """
        Removes all whitespace in the text and returns whatever is remaining.
        """

        return "".join(text.split())

    def find_previous_non_whitespace_character(self, text, skip_character_list, max_num_chars_to_skip):
        """
        Returns the index of the last non-whitespace character, excluding
        the skip characters.
        """
        # Setting up variables
        character_index = -1
        find_index = len(text) - 1
        num_chars_skipped = 0

        while find_index >= 0:
            current_character = text[find_index]

            if current_character.strip() == "":
                find_index -= 1
                continue

            skip_test = False
            if num_chars_skipped < max_num_chars_to_skip:
                for skip_character in skip_character_list:
                    if current_character == skip_character:
                        skip_test = True
                        num_chars_skipped += 1
                        break
            if skip_test:
                find_index -= 1
                continue

            character_index = find_index
            break

        return character_index

    def find_previous_character(self, text, character):
        """
        Returns the index of the closest to the end of the text character
        that is "character".
        """
        # Setting up variables
        character_index = -1
        find_index = len(text) - 1

        # Finding previous character
        while find_index >= 0:
            current_character = text[find_index]

            if current_character == character:
                character_index = find_index
                break

            find_index -= 1

        # Returning index of found character
        return character_index

    def find_next_non_whitespace_character(self, text, skip_character_list, max_num_chars_to_skip):
        """
        Returns the index of the next non-whitespace character, excluding the
        skip characters.
        """
        # Setting up variables
        character_index = -1
        find_index = 0
        num_chars_skipped = 0

        while find_index < len(text):
            current_character = text[find_index]

            if current_character.strip() == "":
                find_index += 1
                continue

            skip_test = False
            if num_chars_skipped < max_num_chars_to_skip:
                for skip_character in skip_character_list:
                    if current_character == skip_character:
                        skip_test = True
                        num_chars_skipped += 1
                        break
            if skip_test:
                find_index += 1
                continue

            character_index = find_index
            break

        return character_index
