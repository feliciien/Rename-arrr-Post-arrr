#!/usr/bin/env python3
"""
Script to download and set up test files for Rename-arrr
"""
import os
import sys
import requests
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(url: str, dest_path: str) -> bool:
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        
        with open(dest_path, 'wb') as f, tqdm(
            desc=os.path.basename(dest_path),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(block_size):
                size = f.write(data)
                pbar.update(size)
                
        return True
    except Exception as e:
        logger.error(f"Error downloading {url}: {str(e)}")
        return False

def main():
    # Create test files directory
    test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_files')
    os.makedirs(test_dir, exist_ok=True)
    
    # Download test files from 1fichier
    url = "https://1fichier.com/dir/iIq4jGFB"
    logger.info(f"Downloading test files from {url}")
    
    # TODO: Add proper file downloading logic for 1fichier
    # For now, we'll create some dummy test files
    test_files = [
        "The Matrix (1999).mp4",
        "Inception.2010.1080p.BluRay.mp4",
        "Avatar_2009_HDRip.mkv",
        "Breaking.Bad.S01E01.720p.BluRay.x264.mkv",
        "Game.of.Thrones.S08E06.1080p.WEB-DL.mkv",
        "Steins;Gate - 01 [BD 1080p].mkv",
        "One Piece - 1084 [1080p].mkv"
    ]
    
    for filename in test_files:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(b'Dummy file for testing')
        logger.info(f"Created test file: {filename}")
    
    logger.info("Test files setup complete!")

if __name__ == '__main__':
    main()
