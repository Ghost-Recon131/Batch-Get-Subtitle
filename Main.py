import logging
import ConfigHandler
import FileOperation


# Config logger
logging.basicConfig(level=logging.NOTSET, format='%(module)s %(asctime)s %(levelname)s: %(message)s',
                    handlers=[logging.StreamHandler()])


# Main function
def main():
    subtitle_config_values = ConfigHandler.load_subtitle_config()
    chapter_config_values = ConfigHandler.load_chapter_config()

    if subtitle_config_values is not False and FileOperation.check_directories(subtitle_config_values):
        result = FileOperation.find_and_copy_file(subtitle_config_values)
        logging.info(f"Copy subtitle result: {result}")
    if chapter_config_values is not False and FileOperation.check_directories(chapter_config_values):
        result = FileOperation.find_and_copy_file(chapter_config_values)
        logging.info(f"Copy chapter result: {result}")


# Initiate script
if __name__ == '__main__':
    print("Script starting, please wait...")
    main()
    print("Script finished.")