# Rename-arrr/renamer.py

import os
from metadata_fetcher import fetch_movie_metadata
from utils import setup_logger

logger = setup_logger()

def rename_files(folder_path, title, year):
    """
    Renames a single media file based on the provided title and year.

    :param folder_path: Path to the folder containing media files.
    :param title: Extracted title of the movie.
    :param year: Extracted release year of the movie.
    :return: Dictionary containing the new title and year.
    :raises Exception: If renaming fails.
    """
    # Construct the original filename with extension
    # This function assumes that the renaming logic is handled externally (e.g., by the GUI thread)
    # Since the GUI is handling individual files, this function renames a single file
    try:
        # Search for the file matching the title and year
        for filename in os.listdir(folder_path):
            if not os.path.isfile(os.path.join(folder_path, filename)):
                continue
            # Simple check to match title and year in filename
            if title.lower() in filename.lower() and year in filename:
                ext = os.path.splitext(filename)[1]
                new_filename = f"{title} ({year}){ext}"
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(old_file_path, new_file_path)
                logger.info(f"Renamed '{filename}' to '{new_filename}'")
                return {'title': title, 'year': year}
        raise FileNotFoundError(f"No matching file found for title '{title}' and year '{year}'.")
    except Exception as e:
        logger.error(f"Error renaming file: {e}")
        raise e

def extract_title_year(filename):
    """
    Extracts the movie title and year from the filename using simple parsing.

    :param filename: Original filename.
    :return: Tuple containing title and year.
    :raises ValueError: If extraction fails.
    """
    name, ext = os.path.splitext(filename)
    # Replace common separators with spaces
    name = name.replace('.', ' ').replace('_', ' ').replace('-', ' ')
    
    # Attempt to extract year
    tokens = name.split()
    year = None
    title_tokens = []
    
    for token in tokens:
        if token.isdigit() and len(token) == 4:
            year = token
            break
        title_tokens.append(token)
    
    if not year:
        raise ValueError("Year not found in filename.")
    
    title = ' '.join(title_tokens)
    return title, year