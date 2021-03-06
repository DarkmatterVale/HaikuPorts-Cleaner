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
            "CHECKSUM_MD5",
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

        self.remove_components = [
            "STATUS_HAIKU",
            "CHECKSUM_MD5",
            "DEPEND"
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
            },
            "STATUS_HAIKU" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "STATUS_HAIKU",
                "join" : "=",
                "pre_requests" : []
            },
            "DEPEND" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "DEPEND",
                "join" : "=",
                "pre_requests" : []
            },
            "CHECKSUM_MD5" : {
                "begin_id" : '"',
                "end_id" : '"',
                "name" : "CHECKSUM_MD5",
                "join" : "=",
                "pre_requests" : []
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

        # Adding log data
        self.logData += ("*" * 70) + "\n"
        self.logData += re.sub(".recipe", "", self.name) + "\n"
        self.logData += ("*" * 70) + "\n"

        # Read the recipe file
        with open(os.path.join(self.baseDir, self.name), 'r') as content_file:
            self.content = content_file.read()
            content_file.close()

        # Updating corrected_content
        self.corrected_content = self.content

        # Determine whether the recipe is of the old format
        if self.should_update_format(self.content):
            # Apply updating
            self.corrected_content = self.convert_old_format(self.content)
            self.content = self.corrected_content
            self.corrected_content = self.correct_ordering()
        # Determine whether clean the recipe
        elif self.should_clean_recipe(self.content):
            # Apply cleaning
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

        # For each component, go through the recipe, find it, and correctly
        #   place it into the new recipe
        for component in self.order:
            start_, end_ = self.extract_component(original_content, component)

            if start_ != -1 and end_ != -1:
                extracted_component_list[component] = {
                    "text" : str(self.content)[start_:end_] + "\n",
                    "clean_text" : re.sub(component + self.component_ordering[component]["join"], "", str(self.content)[start_:end_] + "\n")[1:-2]
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
                self.logData += "WARNING: Adding dummy SUMMARY component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy SUMMARY component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

            # Correcting DESCRIPTION related issues
            if component == "DESCRIPTION" and "DESCRIPTION" in extracted_component_list:
                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(extracted_component_list[component]["text"], [self.component_ordering[component]["end_id"]], 1)
                if end_character_index != -1:
                    extracted_component_list[component]["text"] = extracted_component_list[component]["text"][:(end_character_index + 1)] + self.component_ordering[component]["end_id"] + "\n"
            elif component == "DESCRIPTION" and "DESCRIPTION" not in extracted_component_list:
                print("\033[91mERROR: \033[00m{}".format("Cannot find DESCRIPTION in recipe"))
                self.logData += "ERROR: Cannot find DESCRIPTION in recipe\n"
                self.logData += "WARNING: Adding dummy DESCRIPTION component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy DESCRIPTION component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

            # Correcting HOMPAGE related issues
            if component == "HOMEPAGE" and "HOMEPAGE" in extracted_component_list:
                # If it is multi-line, make sure it is correctly formatted
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    # Getting the individual items within provides
                    num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                    # Generating the correct homepage component
                    generated_text = component + self.component_ordering[component]["join"] + "\"" + re.sub("\t", "", instances_[0]) + "\n"

                    # Since the first COPYRIGHT is not supposed to be on a newline, ignore it
                    num_ -= 1
                    instances_ = instances_[1:]

                    for instance in instances_:
                        cleaned_instance = ""
                        for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                            if non_spaced != "":
                                cleaned_instance += " " + non_spaced
                        cleaned_instance = cleaned_instance[1:]

                        if "#" in instance:
                            generated_text += instance + "\n"
                        else:
                            generated_text += "\t" + cleaned_instance + "\n"

                    # Cleaning ending of component (fixing tabs, etc)
                    end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                    if end_character_index != -1:
                        generated_text = generated_text[:(end_character_index + 1)] + self.component_ordering[component]["end_id"] + "\n"

                    extracted_component_list[component]["text"] = generated_text
            elif component == "HOMEPAGE" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

            # Correcting COPYRIGHT related issues
            if component == "COPYRIGHT" and "COPYRIGHT" in extracted_component_list:
                # If it is multi-line, make sure it is correctly formatted
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    # Getting the individual items within provides
                    num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                    # Cleaning all extra commas
                    for instance_index in range(0, num_):
                        for character_index in range(1, len(instances_[instance_index]) - 3):
                            try:
                                if instances_[instance_index][character_index] == ",":
                                    if re.sub("[0-9]", "", instances_[instance_index][character_index - 1]) == "" and instances_[instance_index][character_index + 1] == " " and re.sub("[0-9]", "", instances_[instance_index][character_index + 2]) != "":
                                        instances_[instance_index] = instances_[instance_index][:character_index] + instances_[instance_index][character_index + 1:]
                            except:
                                pass

                    # Generating the correct copyright component
                    if instances_[0][0] == "\t":
                        generated_text = component + self.component_ordering[component]["join"] + "\"" + instances_[0][1:] + "\n"
                    else:
                        generated_text = component + self.component_ordering[component]["join"] + "\"" + instances_[0] + "\n"

                    for instance_index in range(1, len(instances_)):
                        cleaned_instance = ""
                        for non_spaced in self.remove_characters(instances_[instance_index], ["\t"]).split(" "):
                            if non_spaced != "":
                                cleaned_instance += " " + non_spaced
                        cleaned_instance = cleaned_instance[1:]

                        if "#" in instances_[instance_index]:
                            generated_text += instances_[instance_index] + "\n"
                        elif instance_index > 0:
                                if "\\" in instances_[instance_index - 1]:
                                    generated_text += cleaned_instance + "\n"
                                    continue

                        generated_text += "\t" + cleaned_instance + "\n"

                    # Cleaning ending of component (fixing tabs, etc)
                    end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                    if end_character_index != -1:
                        generated_text = generated_text[:(end_character_index + 1)] + self.component_ordering[component]["end_id"] + "\n"

                    extracted_component_list[component]["text"] = generated_text
            elif component == "COPYRIGHT" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

            # Correcting LICENSE related issues
            if component == "LICENSE" and "LICENSE" in extracted_component_list:
                # If it is multi-line, make sure it is correctly formatted
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    # Getting the individual items within provides
                    num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                    # Generating the correct license component
                    generated_text = component + self.component_ordering[component]["join"] + "\"" + re.sub("\t", "", instances_[0]) + "\n"

                    # Since the first COPYRIGHT is not supposed to be on a newline, ignore it
                    num_ -= 1
                    instances_ = instances_[1:]

                    for instance in instances_:
                        cleaned_instance = ""
                        for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                            if non_spaced != "":
                                cleaned_instance += " " + non_spaced
                        cleaned_instance = cleaned_instance[1:]

                        if "#" in instance:
                            generated_text += instance + "\n"
                        else:
                            generated_text += "\t" + cleaned_instance + "\n"

                    # Cleaning ending of component (fixing tabs, etc)
                    end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                    if end_character_index != -1:
                        generated_text = generated_text[:(end_character_index + 1)] + self.component_ordering[component]["end_id"] + "\n"

                    extracted_component_list[component]["text"] = generated_text
            elif component == "LICENSE" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

            # Correcting REVISION related issues
            if component == "REVISION" and "REVISION" in extracted_component_list:
                # Make sure it is only one line long
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    extracted_component_list[component]["text"] = re.sub(r"\n", "", extracted_component_list[component]["text"]) + "\n"
                    self.logData += "WARNING: Removing extra newline characters in REVISION\n"
            elif component == "REVISION" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    "text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"1\"\n",
                    "clean_text" : ""
                }

            # Correcting SOURCE_URI related issues
            if component == "SOURCE_URI" and "SOURCE_URI" in extracted_component_list:
                # Make sure it is only one line long
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    extracted_component_list[component]["text"] = re.sub(r"\n", "", extracted_component_list[component]["text"]) + "\n"
                    self.logData += "WARNING: Removing extra newline characters in SOURCE_URI\n"
            elif component == "SOURCE_URI" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

            # Correcting CHECKSUM_SHA256 related issues
            if component == "CHECKSUM_SHA256" and "CHECKSUM_SHA256" in extracted_component_list:
                # Make sure it is only one line long
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    extracted_component_list[component]["text"] = re.sub(r"\n", "", extracted_component_list[component]["text"]) + "\n"
                    self.logData += "WARNING: Removing extra newline characters in CHECKSUM_SHA256\n"
            elif component == "CHECKSUM_SHA256" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

            # Correcting SOURCE_DIR related issues
            if component == "SOURCE_DIR" and "SOURCE_DIR" in extracted_component_list:
                # Make sure it is only one line long
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    extracted_component_list[component]["text"] = re.sub(r"\n", "", extracted_component_list[component]["text"]) + "\n"
                    self.logData += "WARNING: Removing extra newline characters in SOURCE_DIR\n"

            # Correcting PATCHES related issues
            if component == "PATCHES" and "PATCHES" in extracted_component_list:
                # If it is multi-line, make sure it is correctly formatted
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    # Getting the individual items within provides
                    num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                    # Generating the correct patches component
                    generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                    for instance in instances_:
                        cleaned_instance = ""
                        for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                            if non_spaced != "":
                                cleaned_instance += " " + non_spaced
                        cleaned_instance = cleaned_instance[1:]

                        if "#" in instance:
                            generated_text += instance + "\n"
                        else:
                            generated_text += "\t" + cleaned_instance + "\n"

                    # Cleaning ending of component (fixing tabs, etc)
                    end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                    if end_character_index != -1:
                        generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                    extracted_component_list[component]["text"] = generated_text

            # Correcting ADDITIONAL_FILES related issues
            if component == "ADDITIONAL_FILES" and "ADDITIONAL_FILES" in extracted_component_list:
                # If it is multi-line, make sure it is correctly formatted
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    # Getting the individual items within provides
                    num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                    # Generating the correct additional_files component
                    generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                    for instance in instances_:
                        cleaned_instance = ""
                        for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                            if non_spaced != "":
                                cleaned_instance += " " + non_spaced
                        cleaned_instance = cleaned_instance[1:]

                        if "#" in instance:
                            generated_text += instance + "\n"
                        else:
                            generated_text += "\t" + cleaned_instance + "\n"

                    # Cleaning ending of component (fixing tabs, etc)
                    end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                    if end_character_index != -1:
                        generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                    extracted_component_list[component]["text"] = generated_text

            # Correcting ARCHITECTURES related issues
            if component == "ARCHITECTURES" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    "text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"?x86 ?x86_gcc2\"\n",
                    "clean_text" : ""
                }

            # Correcting SECONDARY_ARCHITECTURES related issues
            if component == "SECONDARY_ARCHITECTURES" and "SECONDARY_ARCHITECTURES" in extracted_component_list:
                # Make sure it is only one line long
                if len(extracted_component_list[component]["text"].split("\n")) > 2:
                    extracted_component_list[component]["text"] = re.sub(r"\n", "", extracted_component_list[component]["text"]) + "\n"
                    self.logData += "WARNING: Removing extra newline characters in SECONDARY_ARCHITECTURES\n"

            # Correcting PROVIDES related issues
            if component == "PROVIDES" and "PROVIDES" in extracted_component_list:
                # Getting the individual items within provides
                num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                # Generating the correct provides component
                generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                for instance in instances_:
                    cleaned_instance = ""
                    for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                        if non_spaced != "":
                            cleaned_instance += " " + non_spaced
                    cleaned_instance = cleaned_instance[1:]

                    if "#" in instance:
                        generated_text += instance + "\n"
                    else:
                        generated_text += "\t" + cleaned_instance + "\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                if end_character_index != -1:
                    generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                extracted_component_list[component]["text"] = generated_text
            elif component == "PROVIDES" and "PROVIDES" not in extracted_component_list:
                extracted_component_list["PROVIDES"] = {
                    "text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + "PROVIDES=\"\n\t" + re.sub("-.*", "", self.name) + " = $portVersion\n\t\"\n",
                    "clean_text" : re.sub("-.*", "", self.name) + " = $portVersion"
                }
                self.logData += "WARNING: Adding dummy missing PROVIDES in recipe"

            # Correcting REQUIRES related issues
            if component == "REQUIRES" and "REQUIRES" in extracted_component_list:
                # Making sure that a "haiku" is in the REQUIRES component
                if "SECONDARY_ARCHITECTURES" in extracted_component_list:
                    if "haiku$secondaryArchSuffix\n" not in extracted_component_list[component]["text"] and "haiku${secondaryArchSuffix}" not in extracted_component_list[component]["text"]:
                        extracted_component_list[component]["text"] = component + self.component_ordering[component]["join"] + "\"\n\thaiku$secondaryArchSuffix\n\t" + extracted_component_list[component]["clean_text"]
                        extracted_component_list[component]["clean_text"] = "\"\n\thaiku$secondaryArchSuffix\n\t" + extracted_component_list[component]["clean_text"]
                else:
                    if "haiku\n" not in extracted_component_list[component]["text"] and "haiku$secondaryArchSuffix" not in extracted_component_list[component]["text"] and "haiku${secondaryArchSuffix}" not in extracted_component_list[component]["text"]:
                        extracted_component_list[component]["text"] = component + self.component_ordering[component]["join"] + "\"\n\thaiku\n\t" + extracted_component_list[component]["clean_text"]
                        extracted_component_list[component]["clean_text"] = "\"\n\thaiku\n\t" + extracted_component_list[component]["clean_text"]

                # Getting the individual items within provides
                num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                # Generating the correct requires component
                generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                for instance in instances_:
                    cleaned_instance = ""
                    for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                        if non_spaced != "":
                            cleaned_instance += " " + non_spaced
                    cleaned_instance = cleaned_instance[1:]

                    if "#" in instance:
                        generated_text += instance + "\n"
                    else:
                        generated_text += "\t" + cleaned_instance + "\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                if end_character_index != -1:
                    generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                extracted_component_list[component]["text"] = generated_text
            elif component == "REQUIRES" and "REQUIRES" not in extracted_component_list:
                extracted_component_list["REQUIRES"] = {
                    "text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + "REQUIRES=\"\n\thaiku\n\t\"\n",
                    "clean_text" : "haiku"
                }
                self.logData += "WARNING: Adding dummy missing REQUIRES in recipe"

            # Correcting PROVIDES_devel related issues
            if component == "PROVIDES_devel" and "PROVIDES_devel" in extracted_component_list:
                # Getting the individual items within provides
                num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                # Generating the correct provides_devel component
                generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                for instance in instances_:
                    cleaned_instance = ""
                    for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                        if non_spaced != "":
                            cleaned_instance += " " + non_spaced
                    cleaned_instance = cleaned_instance[1:]

                    if "#" in instance:
                        generated_text += instance + "\n"
                    else:
                        generated_text += "\t" + cleaned_instance + "\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                if end_character_index != -1:
                    generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                extracted_component_list[component]["text"] = generated_text

                # Make sure there is a REQUIRES_devel component in the recipe
                if "REQUIRES_devel" not in extracted_component_list:
                    if "SECONDARY_ARCHITECTURES" in extracted_component_list:
                        extracted_component_list["REQUIRES_devel"] = {
                            "text" : "REQUIRES_devel=\"\n\thaiku$\{secondaryArchSuffix\}_devel\n\t\"\n",
                            "clean_text" : "haiku$\{secondaryArchSuffix\}_devel"
                        }
                        self.logData += "WARNING: Adding missing REQUIRES_devel component\n"
                    else:
                        extracted_component_list["REQUIRES_devel"] = {
                            "text" : "REQUIRES_devel=\"\n\thaiku_devel\n\t\"\n",
                            "clean_text" : "haiku_devel"
                        }
                        self.logData += "WARNING: Adding missing REQUIRES_devel component\n"

            # Correcting REQUIRES_devel related issues
            if component == "REQUIRES_devel" and "REQUIRES_devel" in extracted_component_list:
                # Getting the individual items within provides
                num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                # Generating the correct requires_devel component
                generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                for instance in instances_:
                    cleaned_instance = ""
                    for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                        if non_spaced != "":
                            cleaned_instance += " " + non_spaced
                    cleaned_instance = cleaned_instance[1:]

                    if "#" in instance:
                        generated_text += instance + "\n"
                    else:
                        generated_text += "\t" + cleaned_instance + "\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                if end_character_index != -1:
                    generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                extracted_component_list[component]["text"] = generated_text

                # Make sure there is a PROVIDES_devel component in the recipe
                if "PROVIDES_devel" not in extracted_component_list:
                    if "SECONDARY_ARCHITECTURES" in extracted_component_list:
                        extracted_component_list["PROVIDES_devel"] = {
                            "text" : "PROVIDES_devel=\"\n\t" + re.sub("-.*", "", self.name) + "$\{secondaryArchSuffix\}_devel = $portVersion\n\t\"\n",
                            "clean_text" : re.sub("-.*", "", self.name) + "$\{secondaryArchSuffix\}_devel = $portVersion"
                        }
                        self.logData += "WARNING: Adding missing PROVIDES_devel component\n"
                    else:
                        extracted_component_list["PROVIDES_devel"] = {
                            "text" : "PROVIDES_devel=\"\n\t" + re.sub("-.*", "", self.name) + "_devel = $portVersion\n\t\"\n",
                            "clean_text" : re.sub("-.*", "", self.name) + "_devel = $portVersion"
                        }
                        self.logData += "WARNING: Adding missing PROVIDES_devel component\n"

            # Correcting REQUIRES_devel related issues
            if component == "BUILD_REQUIRES" and "BUILD_REQUIRES" in extracted_component_list:
                # Getting the individual items within provides
                num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                # Generating the correct build_requires component
                generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                for instance in instances_:
                    cleaned_instance = ""
                    for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                        if non_spaced != "":
                            cleaned_instance += " " + non_spaced
                    cleaned_instance = cleaned_instance[1:]

                    if "#" in instance:
                        generated_text += instance + "\n"
                    else:
                        generated_text += "\t" + cleaned_instance + "\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                if end_character_index != -1:
                    generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                if extracted_component_list[component]["clean_text"] != "":
                    extracted_component_list[component]["text"] = generated_text
            elif component == "BUILD_REQUIRES" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    "text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\n\thaiku_devel\n\t\"\n",
                    "clean_text" : ""
                }

            # Correcting REQUIRES_devel related issues
            if component == "BUILD_PREREQUIRES" and "BUILD_PREREQUIRES" in extracted_component_list:
                # Getting the individual items within provides
                num_, instances_ = self.number_of_instances(extracted_component_list[component]["clean_text"], "*", ["\n"])

                # Generating the correct build_prerequires component
                generated_text = component + self.component_ordering[component]["join"] + "\"\n"
                for instance in instances_:
                    cleaned_instance = ""
                    for non_spaced in self.remove_characters(instance, ["\t"]).split(" "):
                        if non_spaced != "":
                            cleaned_instance += " " + non_spaced
                    cleaned_instance = cleaned_instance[1:]

                    if "#" in instance:
                        generated_text += instance + "\n"
                    else:
                        generated_text += "\t" + cleaned_instance + "\n"

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(generated_text, [], 0)
                if end_character_index != -1:
                    generated_text = generated_text[:(end_character_index + 1)] + "\n\t" + self.component_ordering[component]["end_id"] + "\n"

                extracted_component_list[component]["text"] = generated_text
            elif component == "BUILD_PREREQUIRES" and component not in extracted_component_list:
                self.logData += "WARNING: Adding dummy " + component + " component in recipe\n"

                extracted_component_list[component] = {
                    #"text" : "# WARNING: Adding dummy " + component + " component in recipe\n" + component + self.component_ordering[component]["join"] + "\"\n\t\"\n",
                    "text" : "# WARNING: " + component + " must be added to recipe here\n",
                    "clean_text" : ""
                }

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

    def should_update_format(self, content):
        """
        If the parser detects that the recipe is of the old format, update the
        recipe.
        """
        for old_component in self.remove_components:
            if old_component in content:
                return True

        return False

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

    def number_of_instances(self, text, char_to_find, skip_chars):
        """
        Returns the number of times "char_to_find" is found in "text", split
        by "skip_chars"
        """
        number = 0
        instances = []

        for skip_char in skip_chars:
            text_components = text.split()
            if skip_char != "":
                text_components = text.split(skip_char)

            for individual_component in text_components:
                if char_to_find == "*":
                    if individual_component != "":
                        number += 1
                        instances.append(individual_component)
                else:
                    if individual_component == char_to_find:
                        number += 1
                        instances.append(individual_component)

        return number, instances

    def remove_characters(self, text, chars_to_remove):
        """
        Returns the text minus all of the instances of "chars_to_remove"
        """
        for char in chars_to_remove:
            text = re.sub(char, "", text)

        return text

    def convert_old_format(self, text):
        """
        Convert recipes from the old format to the new format.
        """
        warning_text = "# WARNING: THIS RECIPE WAS AUTO-CONVERTED...SEE GIT LOG FOR MORE INFORMATION\n\n"
        extracted_component_list = {}

        # For each component, go through the recipe, find it, and correctly
        #   place it into the new recipe
        for component in self.order:
            start_, end_ = self.extract_component(text, component)

            if start_ != -1 and end_ != -1:
                extracted_component_list[component] = {
                    "text" : str(self.content)[start_:end_] + "\n",
                    "clean_text" : re.sub(component + self.component_ordering[component]["join"], "", str(self.content)[start_:end_] + "\n")[1:-2]
                }

        for component in self.remove_components:
            start_, end_ = self.extract_component(text, component)

            if start_ != -1 and end_ != -1:
                extracted_component_list[component] = {
                    "text" : str(self.content)[start_:end_] + "\n",
                    "clean_text" : re.sub(component + self.component_ordering[component]["join"], "", str(self.content)[start_:end_] + "\n")[1:-2]
                }

        # Cleaning all old components & generating appropriate current
        #   components
        for component in self.remove_components:
            # Converting DEPEND into other parts of the recipe
            if component == "DEPEND" and component in extracted_component_list:
                depend_components = self.extract_depend_components(extracted_component_list[component]["clean_text"])

                if "REQUIRES" not in extracted_component_list:
                    extracted_component_list["REQUIRES"] = {
                        "text" : "REQUIRES=\"\n\thaiku\n\t\"\n",
                        "clean_text" : "haiku"
                    }

                text = extracted_component_list["REQUIRES"]["text"]

                # Cleaning ending of component (fixing tabs, etc)
                end_character_index = self.find_previous_non_whitespace_character(text, [], 0)
                if end_character_index != -1:
                    text = text[:end_character_index - 1]

                if text[-1] == "\t":
                    text = text[:-2]

                for depend_component in depend_components:
                    text += "\t" + depend_component[0] + " " + depend_component[1] + " " + depend_component[2] + "\n"
                text += "\t\""

                extracted_component_list["REQUIRES"]["text"] = text + "\n"
                extracted_component_list["REQUIRES"]["clean_text"] = re.sub("REQUIRES" + self.component_ordering["REQUIRES"]["join"], "", text + "\n")[1:-2]

            # Converting STATUS_HAIKU
            if component == "STATUS_HAIKU" and component in extracted_component_list:
                if extracted_component_list[component]["clean_text"].lower() == "stable":
                    extracted_component_list["ARCHITECTURES"] = {
                        "text" : "ARCHITECTURES" + self.component_ordering["ARCHITECTURES"]["join"] + "\"x86_gcc2\"\n",
                        "clean_text" : "x86_gcc2"
                    }
                elif extracted_component_list[component]["clean_text"].lower() == "broken":
                    extracted_component_list["ARCHITECTURES"] = {
                        "text" : "ARCHITECTURES" + self.component_ordering["ARCHITECTURES"]["join"] + "\"!x86_gcc2\"\n",
                        "clean_text" : "!x86_gcc2"
                    }
                else:
                    extracted_component_list["ARCHITECTURES"] = {
                        "text" : "ARCHITECTURES" + self.component_ordering["ARCHITECTURES"]["join"] + "\"?x86_gcc2\"\n",
                        "clean_text" : "?x86_gcc2"
                    }

        # Assembling final information
        ordered_content = warning_text
        for component in self.order:
            if component in extracted_component_list:
                for component_part in self.component_ordering[component]["pre_requests"]:
                    ordered_content += component_part
                ordered_content += extracted_component_list[component]["text"]

        return ordered_content

    def extract_depend_components(self, clean_depend_component):
        """
        Extracts each dependency. It then determines the version(s) required
        and returns a list containing the [ordered] data for each dependency.
        """
        depend_components = []

        for component in clean_depend_component.split("\n"):
            if self.remove_whitespace(component) != "":
                indiv_dependency_components = component.split(" ")

                name = ""
                ver_operator = ""
                version = ""

                for indiv_comp_index in range(0, len(indiv_dependency_components)):
                    if self.remove_whitespace(indiv_dependency_components[indiv_comp_index]) != "":
                        try:
                            name = re.sub(".*/", "", indiv_dependency_components[indiv_comp_index])
                            ver_operator = indiv_dependency_components[indiv_comp_index + 1]
                            version = indiv_dependency_components[indiv_comp_index + 2]
                            break
                        except:
                            pass

                depend_components.append([name, ver_operator, version])

        # Returning the dependencies found in the DEPEND component
        return depend_components
