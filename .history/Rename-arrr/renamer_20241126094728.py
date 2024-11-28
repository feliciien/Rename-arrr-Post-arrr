import os
from utils import setup_logger

# Set up the logger
logger = setup_logger()

def rename_files(folder_path, filename, title, year):
    """
    Renames a single media file based on extracted title and year.

    Args:
        folder_path (str): The directory containing the file.
        filename (str): The current name of the file.
        title (str): The extracted title of the file.
        year (str): The extracted year of the file.

    Returns:
        str: The new filename after renaming.

    Raises:
        Exception: If an error occurs during the renaming process.
    """
    try:
        _, ext = os.path.splitext(filename)  # Extract file extension
        new_filename = f"{title} ({year}){ext}"  # Format the new filename
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)

        if os.path.exists(new_path):
            raise FileExistsError(f"A file named '{new_filename}' already exists in the directory.")

        os.rename(old_path, new_path)  # Rename the file
        logger.info(f"Renamed '{filename}' to '{new_filename}'")
        return new_filename
    except Exception as e:
        logger.error(f"Failed to rename file '{filename}': {e}")
        raise e

def extract_title_year(filename):
    """
    Extracts the title and year from a media file name.

    Args:
        filename (str): The current name of the file.

    Returns:
        tuple: A tuple containing the title (str) and year (str).

    Raises:
        ValueError: If the title or year cannot be extracted.
    """
    try:
        # Remove the file extension and split the filename into tokens
        name, _ = os.path.splitext(filename)
        tokens = name.replace('.', ' ').replace('_', ' ').split()

        # Extract the year (a 4-digit number)
        year = next(token for token in tokens if token.isdigit() and len(token) == 4)

        # Extract the title (all tokens before the year)
        title = ' '.join(tokens[:tokens.index(year)])
        return title, year
    except Exception:
        logger.error(f"Failed to extract title and year from filename: {filename}")
        raise ValueError(f"Could not extract title and year from '{filename}'")

def batch_rename(folder_path):
    """
    Renames all media files in the specified folder.

    Args:
        folder_path (str): The directory containing media files.

    Returns:
        list: A list of tuples containing old and new filenames.

    Raises:
        Exception: If an error occurs during the batch renaming process.
    """
    renamed_files = []
    supported_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv']
    try:
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)

            # Skip if not a file
            if not os.path.isfile(full_path):
                continue

            # Skip unsupported file types
            _, ext = os.path.splitext(filename)
            if ext.lower() not in supported_extensions:
                continue

            # Extract title and year, then rename
            try:
                title, year = extract_title_year(filename)
                new_filename = rename_files(folder_path, filename, title, year)
                renamed_files.append((filename, new_filename))
            except ValueError as ve:
                logger.warning(f"Skipping file '{filename}': {ve}")
            except Exception as e:
                logger.error(f"Failed to rename file '{filename}': {e}")

        logger.info(f"Batch rename completed. {len(renamed_files)} files renamed.")
        return renamed_files
    except Exception as e:
        logger.error(f"Batch rename failed: {e}")
        raise e