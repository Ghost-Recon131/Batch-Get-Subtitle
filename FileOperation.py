import os
import pathlib
import logging
import shutil
import textwrap

# Global vars
logger = logging.getLogger(__name__)


# Check directories exists
def check_directories(subtitle_config_values):
    file_directory = subtitle_config_values[0]
    output_directory = subtitle_config_values[1]

    directory_exists = check_directory_exists(file_directory, output_directory)
    output_directory_empty = check_directory_empty(output_directory)
    directories_valid = directory_exists and output_directory_empty
    return directories_valid


# Check the given directories exists
def check_directory_exists(file_directory, output_directory):
    directories_exist = False
    if os.path.exists(file_directory) and os.path.exists(output_directory):
        directories_exist = True
    elif not os.path.exists(file_directory):
        logger.error("File directory does not exist: {0}".format(file_directory))
    elif not os.path.exists(output_directory):
        logger.error("Output directory does not exist: {0}".format(output_directory))
    return directories_exist


# Check that the output directory is empty
def check_directory_empty(output_directory):
    directories_empty = False
    if not os.listdir(output_directory):
        directories_empty = True
    else:
        logger.error("Output directory is not empty, please check it does not contain any files or subdirectories")
    return directories_empty


# Locates the files then copies them
def find_and_copy_file(subtitle_config_values):
    copy_success = True
    no_files_found = False

    if len(subtitle_config_values) == 7:
        (file_directory, output_directory, attachment_output_directory, search_name, output_name,
         structure, episode_value) = subtitle_config_values
    else:
        attachment_output_directory = None
        (file_directory, output_directory, search_name, output_name,
         structure, episode_value) = subtitle_config_values

    episode_value_counter = int(episode_value)
    search_name, search_name_extension = os.path.splitext(search_name)

    try:
        for root, dirs, files in os.walk(file_directory):
            for file in files:
                filename, extension = os.path.splitext(file)
                if filename == search_name:
                    file_path = os.path.join(root, file)

                    if attachment_output_directory is not None:
                        # Check for an "attachments" folder in the same directory
                        try:
                            attachments_folder = os.path.join(root, "attachments")
                            logging.debug(f"attachments_folder: {attachments_folder}")
                            if not os.path.exists(attachment_output_directory):
                                os.makedirs(attachment_output_directory)

                            # Copy each file from the attachments folder to the destination folder
                            for attachment_file in os.listdir(attachments_folder):
                                attachment_file_path = os.path.join(attachments_folder, attachment_file)
                                destination_file_path = os.path.join(attachment_output_directory, attachment_file)

                                # Skip if a file with the same name already exists
                                if not os.path.exists(destination_file_path):
                                    shutil.copy2(attachment_file_path, destination_file_path)
                        except Exception as e:
                            logger.warning(f"Failed to copy attachment files. Error: {e}")
                    else:
                        pass

                    # Continue for subtitle / chapter files
                    final_output_name = output_name + " " + structure + str(episode_value_counter) + str(
                        pathlib.Path(file_path).suffix)
                    output_path = os.path.join(output_directory, final_output_name)
                    shutil.copy2(file_path, output_path)
                    episode_value_counter += 1
                    successfully_copied = True if os.path.isfile(output_path) else False
                    no_files_found = True

                    # Generate debug information
                    original_file_size_mib = os.path.getsize(file_path) / (1024 * 1024)
                    copied_file_size_mib = os.path.getsize(output_path) / (1024 * 1024)
                    debug_info = textwrap.dedent(f"""
                    Original File Path: {file_path} | Original File Size: {original_file_size_mib}
                    Output Path: {output_path} | Copied File Size: {copied_file_size_mib}
                    Successfully Copied: {successfully_copied}
                    """)
                    # logger.debug(debug_info)
    except Exception as e:
        copy_success = False
        logger.exception(f"Failed to locate & copy file: {e}")

    return copy_success and no_files_found

