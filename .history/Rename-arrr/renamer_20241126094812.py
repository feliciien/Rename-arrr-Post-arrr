# renamer.py

import os
import re

def extract_title_year(filename):
    """
    Extracts the title and year from a filename.
    Assumes the filename contains the title followed by the year in parentheses.
    Example: "Movie Title (2024).mp4" -> ("Movie Title", "2024")
    """
    pattern = r'^(?P<title>.+?)\s*\((?P<year>\d{4})\)'
    match = re.match(pattern, os.path.splitext(filename)[0])
    if match:
        title = match.group('title').strip()
        year = match.group('year').strip()
        return title, year
    else:
        raise ValueError("Filename does not match the expected pattern 'Title (Year)'.")

def rename_files(folder_path, filename, title, year):
    """
    Renames the file to a new format, e.g., "Title (Year).ext"
    """
    extension = os.path.splitext(filename)[1]
    new_filename = f"{title} ({year}){extension}"
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_filename)

    if os.path.exists(new_file):
        raise FileExistsError(f"Cannot rename '{filename}' to '{new_filename}': Target file already exists.")

    os.rename(old_file, new_file)
    return new_filename