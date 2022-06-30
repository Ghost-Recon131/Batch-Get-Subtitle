import argparse
import InputValidation
import MoveAndRename


# argparse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action=argparse.BooleanOptionalAction, help='Verbose Output', default=False)
parser.add_argument('-l', '--list', action=argparse.BooleanOptionalAction, help='List renamed files', default=False)
args = parser.parse_args()


# Global variables
file_extension = None
source_directory = None
output_directory = None
file_name = None
new_file_name = None
season_episode = None
episode_numbering = None


# Check all inputs
def validate_inputs():
    all_input_valid = False
    global source_directory, output_directory, file_name, new_file_name, season_episode, episode_numbering

    # Get necessary inputs
    source_directory = input("Enter location of source files. WARNING: CASE SENSITIVE \n")

    # Only continue asking for input if source directory is valid
    if InputValidation.check_source_directory(source_directory):
        output_directory = input("Enter location to output files. WARNING: CASE SENSITIVE \n")
        if InputValidation.check_output_directory(source_directory, output_directory):
            file_name = InputValidation.validate_file_name(source_directory)

            new_file_name = InputValidation.get_and_validate_string_input("New name for files (File extension not "
                                                                          "needed) \n")

            structure = InputValidation.get_and_validate_string_input("Structure for name and season ie S1E \n")
            season_episode = ' ' + structure

            episode_numbering = InputValidation.get_user_input_int("Enter the starting episode number as integer: ")

            all_input_valid = True
        else:
            print("Exiting due to invalid output directory")
    else:
        print("Exiting due to invalid source directory")
    return all_input_valid


# Print inputs if verbose option is enabled
def verbose_output():
    global source_directory, output_directory, file_name, new_file_name, season_episode, episode_numbering
    if args.verbose:
        format_output = """
Entered Source directory: {}
Entered Output directory: {}
Entered file name to search for: {}
Entered new file name: {}
Entered naming structure: {}
Entered starting episode number: {}
        \n""".format(source_directory, output_directory, file_name, new_file_name, season_episode, episode_numbering)
        print(format_output)


# Print list of processed files if list option is enabled
def list_processed_files():
    global output_directory
    if args.list:
        MoveAndRename.list_processed_files(output_directory)


# Main program logic
def main():
    global source_directory, output_directory, file_name, new_file_name, season_episode, episode_numbering

    if validate_inputs():
        # Start processing files
        MoveAndRename.start(source_directory, output_directory, file_name, new_file_name, season_episode,
                            episode_numbering)

        # argparse options
        list_processed_files()
    verbose_output()


# Run main program
main()
