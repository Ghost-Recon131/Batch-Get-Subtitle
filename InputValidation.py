import pathlib
import os


# This function gets a string user user_input & validates it is not blank
def get_and_validate_string_input(text_prompt):
    user_in = None
    continue_loop = True

    # Characters banned by OS
    banned_ascii_characters = ["<", ">", ":", '"', "/", r"\"", "|", "?", "*"]

    # Keep asking for input until user enters a value
    while continue_loop:
        user_in = input(text_prompt)
        input_not_empty = user_in is not None and user_in != ""

        invalid_characters_detected = False
        for character in banned_ascii_characters:
            if character in user_in:
                invalid_characters_detected = True

        if input_not_empty and not invalid_characters_detected:
            continue_loop = False
        if not input_not_empty:
            print("Your input cannot be empty! \n")
        if invalid_characters_detected:
            print("Your input has invalid characters! \n")

    return user_in


# Validate entered file name
def validate_file_name(source_directory):
    continue_loop = True
    entered_file_name = None
    # Keep asking for input until input is correct
    while continue_loop:
        entered_file_name = get_and_validate_string_input("Enter name to search for (File extension needed) "
                                                          "WARNING: CASE SENSITIVE ie track5_eng.ass \n")
        extension = pathlib.Path(entered_file_name).suffix

        if extension is None or extension == "":
            print("Invalid file name is entered, make sure the file extension entered as well")

        # Only exit loop once both conditions are met
        if extension is not None and extension != "" and check_file_exists(source_directory, entered_file_name):
            continue_loop = False

    return entered_file_name


# Checks that a given file exists
def check_file_exists(source_directory, entered_file_name):
    file_exists = False
    # Check the file exists
    for root, subdirs, files in os.walk(source_directory):
        for file in files:
            if file.startswith(entered_file_name):
                file_exists = True
                break
    if not file_exists:
        print("File with given file name does not exist")

    return file_exists


#  Check if source directory exists
def check_source_directory(source_directory):
    if os.path.isdir(source_directory + '\\'):
        ret_value = True
    else:
        print("Source directory does not exist")
        ret_value = False
    return ret_value


# Validate output directory
def check_output_directory(source_directory, output_directory):
    # Check source & output directory is not the same
    directory_not_same = False
    if source_directory == output_directory:
        print("Output directory cannot be the same as source directory")
    else:
        directory_not_same = True

    # Check the output directory exists & can be accessed
    directory_accessible = True
    if os.path.isdir(output_directory + '\\') is False:
        try:
            os.mkdir(output_directory)
        except:
            directory_accessible = False
            print("Failed to create directory, possible permission error!")

    # Check the output directory is empty
    directory_empty = False
    if not os.listdir(output_directory):
        directory_empty = True

    return directory_not_same and directory_accessible and directory_empty


# Get an integer input from user, will continue asking for input until input is correct
def get_user_input_int(prompt):
    user_in = None
    continue_loop = True

    while continue_loop:
        try:
            user_in = int(input(prompt))
            continue_loop = False
        except:
            print("You did not enter a valid integer! \n")
    return user_in
