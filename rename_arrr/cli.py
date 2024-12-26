import argparse
import os
import asyncio
import logging
from core.renamer import MediaRenamer
from typing import Dict, List

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rename_arrr.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def rename_files_cli(folder_path: str, config: Dict = None) -> List[Dict]:
    """
    CLI function to rename all files in the specified folder.
    Returns a list of results containing original and new filenames with metadata.
    """
    if not os.path.exists(folder_path):
        logger.error(f"Folder does not exist: {folder_path}")
        return []

    try:
        renamer = MediaRenamer(config)
        results = await renamer.process_directory(folder_path)

        # Print results
        logger.info(f"\nProcessed {len(results)} files:")
        for result in results:
            if result['new']:
                logger.info(f"\nRenamed: {os.path.basename(result['original'])} -> {os.path.basename(result['new'])}")
                if result['metadata'].get('poster'):
                    logger.info(f"Downloaded poster: {os.path.basename(result['metadata']['poster'])}")
            else:
                logger.error(f"\nFailed to rename: {os.path.basename(result['original'])}")

        return results

    except Exception as e:
        logger.error(f"Error processing directory: {str(e)}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Rename-arrr: Media File Renaming Tool")
    parser.add_argument("--folder", "-f", required=True, help="Path to the folder containing files to rename")
    parser.add_argument("--type", "-t", choices=['auto', 'anime', 'series', 'movie'], default='auto',
                      help="Type of media files (default: auto)")
    parser.add_argument("--no-nfo", action="store_true", help="Skip NFO file generation")
    parser.add_argument("--no-posters", action="store_true", help="Skip poster downloads")
    args = parser.parse_args()

    # Prepare configuration
    config = {
        'media_type': args.type,
        'create_nfo': not args.no_nfo,
        'download_posters': not args.no_posters
    }

    # Run the async function
    loop = asyncio.get_event_loop()
    try:
        results = loop.run_until_complete(rename_files_cli(args.folder, config))
        if results:
            logger.info("Renaming process completed successfully.")
        else:
            logger.error("No files were processed.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        loop.close()

if __name__ == "__main__":
    main()