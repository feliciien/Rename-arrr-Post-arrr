import os
import re

def extract_title_year(filename):
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
    invalid_chars = r'[<>:"/\\|?*]'
    return re.sub(invalid_chars, '', title).strip()

def rename_files(folder_path, filename, title, year):
    extension = os.path.splitext(filename)[1]
    sanitized_title = sanitize_title(title)
    new_filename = f"{sanitized_title} ({year}){extension}"

    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)

    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{sanitized_title} ({year}) [{counter}]{extension}"
        new_path = os.path.join(folder_path, new_filename)
        counter += 1

    os.rename(old_path, new_path)
    return new_filename