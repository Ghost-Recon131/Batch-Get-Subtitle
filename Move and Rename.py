import os
import shutil
from natsort import natsorted
import pathlib

# Global variables
file_extension = None


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


# This function will validate entered file name
def validate_file_name():
    continue_loop = True
    # Keep asking for input until input is correct
    while continue_loop:
        file_name = get_and_validate_string_input("Name to search for (File extension needed) WARNING: CASE SENSITIVE ie track5_eng.ass \n")
        extension = pathlib.Path(file_name).suffix
        if extension is not None and extension != "":
            continue_loop = False
        else:
            print("Invalid file name is entered, make sure the file extension entered as well")
    return file_name


#  Check if source directory exists
def check_source_directory(source_directory):
    if os.path.isdir(source_directory + '\\'):
        ret_value = True
    else:
        print("Source directory does not exist")
        ret_value = False
    return ret_value


#  Check if the output location exists, if not, creates the folder
def check_output_directory(output_location):
    operation_status = True
    if os.path.isdir(output_location + '\\') is False:
        try:
            os.mkdir(output_location)
        except:
            print("Failed to create directory, possible permission error!")
            operation_status = False
    return operation_status


#  Moves files to new location
def move_files(source_directory, output_directory, file_name):
    for root, subdirs, files in os.walk(source_directory):
        for f in files:
            global file_extension
            file_extension = pathlib.Path(file_name).suffix
            try:
                if f.startswith(file_name) and f.endswith(file_extension):
                    count = 1
                    destination_file = os.path.join(output_directory, f)
                    while os.path.exists(destination_file):
                        destination_file = os.path.join(output_directory, f"{f}_{count}")
                        count += 1
                    shutil.move(os.path.join(root, f), destination_file)
            except:
                print("Failed to move file, possible permission error")


#  Rename files after they are copied
def rename_files(output_directory, new_file_name, season_episode):
    os.chdir(output_directory)
    for (i, filename) in enumerate(natsorted(os.listdir(output_directory))):
        i += 1
        try:
            global file_extension
            os.rename(src=filename, dst='{}{}{}{}'.format(new_file_name, season_episode, i, file_extension))
        except:
            print("Failed to rename file, possible permission error")
    print('Completed')


# Main Program
def main():

    # Get necessary inputs
    source_directory = input("Enter location of source files. WARNING: CASE SENSITIVE \n")
    # Only continue asking for input if source directory is valid
    if check_source_directory(source_directory):
        output_directory = input("Enter location to output files. WARNING: CASE SENSITIVE \n")
        file_name = validate_file_name()
        new_file_name = get_and_validate_string_input("New name for files (File extension not needed) \n")
        structure = get_and_validate_string_input("Structure for name and season ie S1E \n")
        season_episode = ' ' + structure

        # Only continue to move & rename files once source directory is valid
        if check_output_directory(output_directory):
            move_files(source_directory, output_directory, file_name)
            rename_files(output_directory, new_file_name, season_episode)
    else:
        print("Exiting program")


# Start main program
main()

