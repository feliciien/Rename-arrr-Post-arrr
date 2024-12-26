import os
import re
from metadata_fetcher import fetch_movie_metadata as fetch_metadata

def extract_title_year(filename):
    """
    Extract title and year from the filename as a fallback mechanism.
    """
    patterns = [
        r'^(?P<title>.+?)\s*\((?P<year>\d{4})\)',
        r'^(?P<title>.+?)\.(?P<year>\d{4})',
        r'^(?P<title>.+?)\s*-\s*(?P<year>\d{4})',
        r'^(?P<title>.+?)_(?P<year>\d{4})'
    ]
    base_name = os.path.splitext(filename)[0]
    for pattern in patterns:
        match = re.match(pattern, base_name)
        if match:
            title = match.group('title').strip()
            year = match.group('year').strip()
            return sanitize_title(title), year
    return sanitize_title(base_name), 'Unknown'

def sanitize_title(title):
    """
    Sanitize title by removing invalid characters for filenames.
    """
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '', title).strip()

def rename_files(folder_path, filename, title, year):
    """
    Rename a file based on metadata fetched from TMDb or extracted from filename.
    """
    try:
        # Attempt to fetch metadata using the API
        fetched_metadata = fetch_metadata(title, year)
        final_title = fetched_metadata.get('title', title)
        final_year = fetched_metadata.get('year', year)
    except (ValueError, ConnectionError):
        # Fallback to extracted metadata if API fails
        final_title, final_year = title, year

    extension = os.path.splitext(filename)[1]
    new_filename = f"{final_title} ({final_year}){extension}"

    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)

    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{final_title} ({final_year}) [{counter}]{extension}"
        new_path = os.path.join(folder_path, new_filename)
        counter += 1

    os.rename(old_path, new_path)
    return new_filename