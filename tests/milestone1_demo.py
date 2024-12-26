"""
Milestone 1 Demo Script
This script demonstrates all features implemented for Milestone 1:
- Media scraping from multiple sources
- NFO file generation
- Image/poster downloads
- Complete metadata handling for all media types
"""

import os
import asyncio
import shutil
from pathlib import Path
from rename_arrr.core.renamer import MediaRenamer

async def setup_test_files():
    """Create test directory with sample files"""
    test_dir = Path("demo_files")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()
    
    # Sample files for each media type
    test_files = {
        # Anime files
        "anime": [
            "[HorribleSubs] My Hero Academia - 01 [720p].mkv",
            "[Erai-raws] Attack on Titan - 01 [1080p].mkv",
            "[SubsPlease] Demon Slayer S02E01 [720p].mkv"
        ],
        # TV Show files
        "tv": [
            "The Last of Us S01E01 720p WEB-DL.mp4",
            "Breaking.Bad.S01E01.720p.BluRay.x264.mkv",
            "Game.of.Thrones.S01E01.1080p.mkv"
        ],
        # Movie files
        "movies": [
            "Inception.2010.1080p.BluRay.x264.mkv",
            "The Matrix 1999 720p BRRip.mkv",
            "Interstellar (2014) 1080p.mkv"
        ],
        # Music files
        "music": [
            "01 - The Beatles - Hey Jude.mp3",
            "Pink Floyd - Dark Side of the Moon - 01 - Speak to Me.flac",
            "Queen - Bohemian Rhapsody.mp3",
            "01. Metallica - Enter Sandman.mp3"
        ]
    }
    
    # Create directories and files
    for media_type, files in test_files.items():
        media_dir = test_dir / media_type
        media_dir.mkdir()
        for file in files:
            (media_dir / file).touch()
    
    return test_dir

async def test_media_type(renamer: MediaRenamer, test_dir: Path, media_type: str):
    """Test renaming for a specific media type"""
    print(f"\n=== Testing {media_type.upper()} files ===")
    media_dir = test_dir / media_type
    
    for file in media_dir.iterdir():
        if file.is_file():
            print(f"\nProcessing: {file.name}")
            
            # Fetch metadata
            metadata = await renamer.fetch_metadata(str(file))
            if metadata:
                print("Metadata fetched:")
                for key, value in metadata.items():
                    if key != 'tracks':  # Skip printing full track list for brevity
                        print(f"  {key}: {value}")
                
                # Rename file
                new_path = await renamer.rename_file(str(file), metadata)
                if new_path:
                    print(f"Successfully renamed to: {Path(new_path).name}")
                    
                    # Check for NFO and artwork
                    nfo_file = Path(new_path).with_suffix('.nfo')
                    if nfo_file.exists():
                        print("✓ NFO file created")
                    
                    artwork_files = ['poster.jpg', 'folder.jpg']
                    for art in artwork_files:
                        art_file = Path(new_path).parent / art
                        if art_file.exists():
                            print(f"✓ {art} downloaded")
            else:
                print("❌ No metadata found")

async def main():
    """Run the demo"""
    print("=== Rename-arrr Milestone 1 Demo ===")
    print("Demonstrating all implemented features:")
    print("1. Media scraping from multiple sources")
    print("2. NFO file generation")
    print("3. Image/poster downloads")
    print("4. Complete metadata handling")
    
    # Setup test environment
    test_dir = await setup_test_files()
    print(f"\nCreated test environment in: {test_dir}")
    
    # Initialize renamer
    renamer = MediaRenamer()
    
    try:
        # Test each media type
        media_types = ['anime', 'tv', 'movies', 'music']
        for media_type in media_types:
            await test_media_type(renamer, test_dir, media_type)
    
    finally:
        # Cleanup
        await renamer.close()
        print("\nDemo completed!")
        print("\nNote: Test files are kept in the 'demo_files' directory for inspection.")
        print("You can find the following in each media type directory:")
        print("- Original and renamed media files")
        print("- Generated NFO files")
        print("- Downloaded artwork")

if __name__ == "__main__":
    asyncio.run(main())
