import os
import shutil
from natsort import natsorted
import pathlib

# Global variables
file_extension = None


#  Moves files to new location + creates list of file objects
def move_files(source_directory, output_directory, file_name):
    for root, subdirs, files in os.walk(source_directory):
        for file in files:
            # Gets the file extension
            global file_extension
            file_extension = pathlib.Path(file_name).suffix
            try:
                # Finds the file with the given file name & extension
                if file.startswith(file_name) and file.endswith(file_extension):
                    count = 1
                    destination_file = os.path.join(output_directory, file)
                    # Get original file & give it a temporary name
                    while os.path.exists(destination_file):
                        destination_file = os.path.join(output_directory, f"{file}_{count}")
                        count += 1
                    # Move the file to new directory
                    shutil.move(os.path.join(root, file), destination_file)
            except Exception as e:
                print("Failed to move file, possible permission error", e, end="\n")


#  Rename files after they are copied
def rename_files(output_directory, new_file_name, season_episode, episode_numbering):
    os.chdir(output_directory)
    for (i, filename) in enumerate(natsorted(os.listdir(output_directory))):
        try:
            global file_extension
            os.rename(src=filename, dst='{}{}{}{}'.format(new_file_name, season_episode,
                                                          episode_numbering, file_extension))
            episode_numbering += 1
        except Exception as e:
            print("Failed to rename file, possible permission error", e, end="\n")
    print('Completed')


# List all renamed files
def list_processed_files(output_directory):
    # array to store files found
    files_found = []

    for path in os.listdir(output_directory):
        # Only add files to array, ignores directories
        if os.path.isfile(os.path.join(output_directory, path)):
            files_found.append(path)

    for files in files_found:
        print(files, end='\n')


# Start the moving & rename process
def start(source_directory, output_directory, file_name, new_file_name, season_episode, episode_numbering):
    move_files(source_directory, output_directory, file_name)
    rename_files(output_directory, new_file_name, season_episode, episode_numbering)
