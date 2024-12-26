"""
Test script for media renaming functionality
"""
import os
import asyncio
from pathlib import Path
from rename_arrr.core.renamer import MediaRenamer

async def test_anime_renaming():
    """Test anime renaming functionality"""
    renamer = MediaRenamer()
    
    # Test anime file
    test_file = "test_files/[HorribleSubs] My Hero Academia - 01 [720p].mkv"
    
    # Create test directory and file
    os.makedirs("test_files", exist_ok=True)
    Path(test_file).touch()
    
    try:
        # Fetch metadata and rename
        metadata = await renamer.fetch_metadata(test_file)
        if metadata:
            print(f"Fetched metadata: {metadata}")
            new_path = await renamer.rename_file(test_file, metadata)
            if new_path:
                print(f"Successfully renamed to: {new_path}")
    finally:
        await renamer.close()

async def test_tv_show_renaming():
    """Test TV show renaming functionality"""
    renamer = MediaRenamer()
    
    # Test TV show file
    test_file = "test_files/The.Last.of.Us.S01E01.720p.WEB-DL.mp4"
    
    # Create test directory and file
    os.makedirs("test_files", exist_ok=True)
    Path(test_file).touch()
    
    try:
        # Fetch metadata and rename
        metadata = await renamer.fetch_metadata(test_file)
        if metadata:
            print(f"Fetched metadata: {metadata}")
            new_path = await renamer.rename_file(test_file, metadata)
            if new_path:
                print(f"Successfully renamed to: {new_path}")
    finally:
        await renamer.close()

async def test_movie_renaming():
    """Test movie renaming functionality"""
    renamer = MediaRenamer()
    
    # Test movie file
    test_file = "test_files/Inception.2010.1080p.BluRay.x264.mkv"
    
    # Create test directory and file
    os.makedirs("test_files", exist_ok=True)
    Path(test_file).touch()
    
    try:
        # Fetch metadata and rename
        metadata = await renamer.fetch_metadata(test_file)
        if metadata:
            print(f"Fetched metadata: {metadata}")
            new_path = await renamer.rename_file(test_file, metadata)
            if new_path:
                print(f"Successfully renamed to: {new_path}")
    finally:
        await renamer.close()

async def test_music_renaming():
    """Test music renaming functionality"""
    renamer = MediaRenamer()
    
    # Test music files
    test_files = [
        "test_files/01 - The Beatles - Hey Jude.mp3",
        "test_files/Pink Floyd - Dark Side of the Moon - 01 - Speak to Me.flac",
        "test_files/Queen - Bohemian Rhapsody.mp3"
    ]
    
    # Create test directory and files
    os.makedirs("test_files", exist_ok=True)
    for file in test_files:
        Path(file).touch()
    
    try:
        for test_file in test_files:
            # Fetch metadata and rename
            metadata = await renamer.fetch_metadata(test_file)
            if metadata:
                print(f"Fetched metadata: {metadata}")
                new_path = await renamer.rename_file(test_file, metadata)
                if new_path:
                    print(f"Successfully renamed to: {new_path}")
    finally:
        await renamer.close()

async def main():
    """Run all tests"""
    print("Testing anime renaming...")
    await test_anime_renaming()
    
    print("\nTesting TV show renaming...")
    await test_tv_show_renaming()
    
    print("\nTesting movie renaming...")
    await test_movie_renaming()
    
    print("\nTesting music renaming...")
    await test_music_renaming()

if __name__ == "__main__":
    asyncio.run(main())
