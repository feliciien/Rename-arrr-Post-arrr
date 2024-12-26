# Rename-arrr/cli.py

import argparse
from renamer import rename_files
from utils import setup_logger

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description='Rename-arrr CLI Tool')
    parser.add_argument('folder', type=str, help='Path to the folder containing media files')
    args = parser.parse_args()

    folder_path = args.folder
    try:
        renamed_files = rename_files(folder_path)
        print(f'Renamed {len(renamed_files)} files successfully.')
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f'Error: {e}')

if __name__ == '__main__':
    main()