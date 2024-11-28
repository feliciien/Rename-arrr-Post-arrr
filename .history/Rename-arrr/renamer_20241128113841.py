import os
import re

def extract_title_year(filename):
    """
    Extracts the title and year from a filename.
    Supports common naming conventions like:
      - Title.Year.ext
      - Title (Year).ext
      - Title - Year.ext
    Returns:
      - Title (str): Extracted or cleaned title.
      - Year (str): Extracted year or 'Unknown' if not found.
    """
    # Patterns to match various file naming conventions
    patterns = [
        r'^(?P<title>.+?)\s*\((?P<year>\d{4})\)',  # e.g., "Title (2020)"
        r'^(?P<title>.+?)\s*-\s*(?P<year>\d{4})',  # e.g., "Title - 2020"
        r'^(?P<title>.+?)\.(?P<year>\d{4})'        # e.g., "Title.2020"
    ]

    base_name = os.path.splitext(filename)[0]  # Remove extension
    for pattern in patterns:
        match = re.match(pattern, base_name)
        if match:
            title = match.group('title').strip()
            year = match.group('year').strip()
            return sanitize_title(title), year

    # If no patterns match, return original filename as title and 'Unknown' for year
    return sanitize_title(base_name), 'Unknown'

def sanitize_title(title):
    """
    Cleans up the title by removing invalid characters for file systems.
    """
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '', title).strip()

def rename_files(folder_path, filename, title, year):
    """
    Renames a file based on the extracted title and year.
    Ensures no overwriting of existing files by appending a counter if necessary.
    """
    extension = os.path.splitext(filename)[1]  # File extension
    sanitized_title = sanitize_title(title)  # Clean the title
    new_filename = f"{sanitized_title} ({year}){extension}"

    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)

    # Ensure the old file exists
    if not os.path.exists(old_path):
        raise FileNotFoundError(f"Cannot find file: {old_path}")

    # Avoid overwriting by appending a counter if the file already exists
    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{sanitized_title} ({year}) [{counter}]{extension}"
        new_path = os.path.join(folder_path, new_filename)
        counter += 1

    os.rename(old_path, new_path)
    return new_filename