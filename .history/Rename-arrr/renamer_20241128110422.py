import os
from utils import setup_logger

logger = setup_logger()

def rename_files(folder_path, filename, title, year):
    _, ext = os.path.splitext(filename)
    new_filename = f"{title} ({year}){ext}"
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)

    if os.path.exists(new_path):
        raise FileExistsError(f"A file named '{new_filename}' already exists.")

    os.rename(old_path, new_path)
    logger.info(f"Renamed '{filename}' to '{new_filename}'")
    return new_filename

def extract_title_year(filename):
    name, _ = os.path.splitext(filename)
    tokens = name.replace('.', ' ').replace('_', ' ').split()
    year = next(token for token in tokens if token.isdigit() and len(token) == 4)
    title = ' '.join(tokens[:tokens.index(year)])
    return title, year