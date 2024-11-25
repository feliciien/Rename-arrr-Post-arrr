# Rename-arrr/renamer.py

import os
from metadata_fetcher import fetch_movie_metadata
from utils import setup_logging, log_info, log_error

# Initialize logging
setup_logging()

def rename_files(folder_path):
    renamed_files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            title, ext = os.path.splitext(filename)
            try:
                metadata = fetch_movie_metadata(title)
                new_name = f"{metadata['title']} ({metadata['release_date'][:4]}){ext}"
                new_path = os.path.join(folder_path, new_name)
                os.rename(file_path, new_path)
                renamed_files.append(new_name)
                log_info(f"Renamed '{filename}' to '{new_name}'")
            except Exception as e:
                error_message = f"Failed to rename '{filename}': {e}"
                print(error_message)
                log_error(error_message)
    return renamed_files