import argparse
import os
from renamer import rename_files, extract_title_year
from utils import setup_logger

logger = setup_logger()

def rename_files_cli(folder_path):
    """
    CLI function to rename all files in the specified folder.
    """
    allowed_extensions = {'.mp4', '.mkv', '.avi', '.mov'}
    files_to_rename = [
        file for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file)) and os.path.splitext(file)[1].lower() in allowed_extensions
    ]

    if not files_to_rename:
        logger.info(f"No valid files found in the folder: {folder_path}")
        print(f"No valid files found in the folder: {folder_path}")
        return

    logger.info(f"Found {len(files_to_rename)} files to rename in folder: {folder_path}")
    print(f"Found {len(files_to_rename)} files to rename in folder: {folder_path}")

    for filename in files_to_rename:
        try:
            # Extract title and year from filename
            extracted_title, extracted_year = extract_title_year(filename)

            # Rename file with extracted or fetched metadata
            new_filename = rename_files(folder_path, filename, extracted_title, extracted_year)
            logger.info(f"Renamed '{filename}' to '{new_filename}'")
            print(f"Renamed '{filename}' to '{new_filename}'")
        except Exception as e:
            logger.error(f"Error renaming '{filename}': {e}")
            print(f"Error renaming '{filename}': {e}")

    logger.info("Renaming process completed.")
    print("Renaming process completed.")

def main():
    parser = argparse.ArgumentParser(description="CLI for Rename...arrr")
    parser.add_argument("--folder", "-f", required=True, help="Path to the folder containing files to rename")
    args = parser.parse_args()

    folder_path = args.folder

    if not os.path.exists(folder_path):
        logger.error(f"Folder does not exist: {folder_path}")
        print(f"Error: Folder does not exist: {folder_path}")
        return

    rename_files_cli(folder_path)

if __name__ == "__main__":
    main()