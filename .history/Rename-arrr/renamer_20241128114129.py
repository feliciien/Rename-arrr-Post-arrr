import os
import re

def extract_title_year(filename):
    """
    Extracts the title and year from a filename.
    Supports naming conventions like:
      - Title (Year).ext
      - Title.Year.ext
      - Title - Year.ext
      - Title_Year_Resolution.ext
    Returns:
      - Title (str): Extracted or cleaned title.
      - Year (str): Extracted year or 'Unknown' if not found.
    """
    # Patterns for common file naming conventions
    patterns = [
        r'^(?P<title>.+?)\s*\((?P<year>\d{4})\)',  # Title (Year).ext
        r'^(?P<title>.+?)\.(?P<year>\d{4})',       # Title.Year.ext
        r'^(?P<title>.+?)\s*-\s*(?P<year>\d{4})',  # Title - Year.ext
        r'^(?P<title>.+?)_(?P<year>\d{4})'         # Title_Year.ext
    ]

    base_name = os.path.splitext(filename)[0]  # Remove file extension
    for pattern in patterns:
        match = re.match(pattern, base_name)
        if match:
            title = match.group('title').strip()
            year = match.group('year').strip()
            return sanitize_title(title), year

    # If no pattern matches, fallback to the original filename and 'Unknown'
    return sanitize_title(base_name), 'Unknown'

def sanitize_title(title):
    """
    Removes invalid characters from the title for safe file naming.
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

def rename_all_files_in_folder(folder_path):
    """
    Iterates over all files in a folder and renames them.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")

    renamed_files = []
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            try:
                title, year = extract_title_year(filename)
                new_filename = rename_files(folder_path, filename, title, year)
                renamed_files.append((filename, new_filename))
            except Exception as e:
                print(f"Failed to rename {filename}: {e}")
    return renamed_files