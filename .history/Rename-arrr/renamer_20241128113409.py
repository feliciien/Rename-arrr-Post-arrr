import os
import re

def extract_title_year(filename):
    """
    Extracts the title and year from a filename.
    Assumes the filename is in the format 'Title (Year).ext'
    """
    pattern = r'^(?P<title>.+?)\s*\((?P<year>\d{4})\)'
    match = re.match(pattern, os.path.splitext(filename)[0])
    if match:
        title = match.group('title').strip()
        year = match.group('year').strip()
        return title, year
    else:
        # If pattern does not match, return the original filename without extension and a default year
        title = os.path.splitext(filename)[0]
        year = 'Unknown'
        return title, year

def rename_files(folder_path, filename, title, year):
    """
    Renames a file based on the extracted title and year.
    For example, 'Old Name (2020).ext' -> 'Title (Year).ext'
    """
    extension = os.path.splitext(filename)[1]
    new_filename = f"{title} ({year}){extension}"
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)

    # Check if the new filename already exists to avoid overwriting
    if os.path.exists(new_path):
        raise FileExistsError(f"Cannot rename '{filename}' to '{new_filename}': File already exists.")

    os.rename(old_path, new_path)
    return new_filename