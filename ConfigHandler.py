import configparser
import os
import logging

# Global vars
CONF_FILE_NAME = "Batch-Get-Tool_config.ini"
logger = logging.getLogger(__name__)


# Load current configs
def load_subtitle_config():
    config_values = None
    load_success = False

    # Start loading details from config file
    if os.path.isfile(CONF_FILE_NAME):
        try:
            config = configparser.ConfigParser()
            config.read(CONF_FILE_NAME)
            subtitle_file_directory = config["Subtitles"]["subtitle_file_directory"]
            subtitle_output_directory = config["Subtitles"]["subtitle_output_directory"]
            attachment_output_directory = config["Subtitles"]["attachment_output_directory"]
            subtitle_file_name = config["Subtitles"]["subtitle_file_name"]
            subtitle_output_name = config["Subtitles"]["subtitle_output_name"]
            subtitle_structure = config["Subtitles"]["subtitle_structure"]
            subtitle_episode_value = config["Subtitles"]["subtitle_episode_value"]

            if evaluate_variables(subtitle_file_directory, subtitle_output_directory, attachment_output_directory,
                                  subtitle_file_name, subtitle_output_name, subtitle_structure,
                                  subtitle_episode_value) and check_chapter_episode_value(subtitle_episode_value):
                config_values = (subtitle_file_directory, subtitle_output_directory, attachment_output_directory,
                                 subtitle_file_name, subtitle_output_name, subtitle_structure, subtitle_episode_value)
                load_success = True
            else:
                logger.info("Missing or incomplete subtitle configs")
        except Exception as e:
            logger.exception(f"Failed to load config file: {e}")
    else:
        logger.info("Config file does not exist or is invalid. ")
        create_config_file()

    # Return either config values or false
    if load_success:
        load_success = config_values
    return load_success


# Get config for chapters
def load_chapter_config():
    config_values = ()
    load_success = False

    # Start loading details from config file
    if os.path.isfile(CONF_FILE_NAME):
        try:
            config = configparser.ConfigParser()
            config.read(CONF_FILE_NAME)
            chapter_file_directory = config["Chapters"]["chapter_file_directory"]
            chapter_output_directory = config["Chapters"]["chapter_output_directory"]
            chapter_file_name = config["Chapters"]["chapter_file_name"]
            chapter_output_name = config["Chapters"]["chapter_output_name"]
            chapter_structure = config["Chapters"]["chapter_structure"]
            chapter_episode_value = config["Chapters"]["chapter_episode_value"]

            if evaluate_variables(chapter_file_directory, chapter_output_directory, chapter_file_name,
                                  chapter_output_name, chapter_structure, chapter_episode_value) \
                    and check_chapter_episode_value(chapter_episode_value):
                config_values = (chapter_file_directory, chapter_output_directory, chapter_file_name,
                                 chapter_output_name, chapter_structure, chapter_episode_value)
                load_success = True
            else:
                logger.info("Missing or incomplete chapter configs")
        except Exception as e:
            logger.exception(f"Failed to load config file: {e}")
    else:
        logger.info("Config file does not exist or is invalid. ")
        create_config_file()

    # Return either config values or false
    if load_success:
        load_success = config_values
    return load_success


# Check if loaded value is blank
def evaluate_variables(*args):
    arg_not_blank = True
    for value in args:
        if not value or value.isspace():
            arg_not_blank = False

    # Check for banned characters
    invalid_characters_detected = False
    banned_ascii_characters = ["<", ">", ":", '"', "/", r"\"", "|", "?", "*"]
    for character in banned_ascii_characters:
        if character in args:
            invalid_characters_detected = True
    return_value = arg_not_blank and (invalid_characters_detected is False)
    return return_value


# Check chapter_episode_value is a valid int
def check_chapter_episode_value(chapter_episode_value):
    result = True
    try:
        tmp = int(chapter_episode_value)
    except Exception as e:
        result = False
        logger.exception(f"Invalid chapter episode value provided: {chapter_episode_value}, error: {e}")
    return result


# Create config file if it doesn't exist
def create_config_file():
    try:
        config = configparser.ConfigParser()
        # Define settings
        config["Subtitles"] = {
            "subtitle_file_directory": "",
            "subtitle_output_directory": "",
            "attachment_output_directory": "",
            "subtitle_file_name": "",
            "subtitle_output_name": "",
            "subtitle_structure": "",
            "subtitle_episode_value": ""
        }
        config["Chapters"] = {
            "chapter_file_directory": "",
            "chapter_output_directory": "",
            "chapter_file_name": "",
            "chapter_output_name": "",
            "chapter_structure": "",
            "chapter_episode_value": ""
        }
        # Write settings to file
        with open("Batch-Get-Tool_config.ini", "w") as config_file:
            config.write(config_file)
    except Exception as e:
        logger.exception(f"Failed to create config file: {e}")
