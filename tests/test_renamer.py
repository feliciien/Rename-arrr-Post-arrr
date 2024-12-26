"""
Tests for the MediaRenamer class
"""
import pytest
import os
import asyncio
from rename_arrr.core.renamer import MediaRenamer

@pytest.fixture
def renamer():
    return MediaRenamer()

@pytest.fixture
def test_files(tmp_path):
    """Create test files in a temporary directory"""
    # Create test files
    files = [
        "The Matrix (1999).mp4",
        "Inception.2010.1080p.BluRay.mp4",
        "Avatar_2009_HDRip.mkv",
        "Spirited.Away.2001.mkv"
    ]
    
    for file in files:
        path = tmp_path / file
        path.write_text("")
        
    return tmp_path

@pytest.mark.asyncio
async def test_extract_info_from_filename(renamer):
    """Test filename information extraction"""
    test_cases = [
        {
            "filename": "The Matrix (1999).mp4",
            "expected": {"title": "The Matrix", "year": "1999"}
        },
        {
            "filename": "Inception.2010.1080p.BluRay.mp4",
            "expected": {"title": "Inception", "year": "2010"}
        },
        {
            "filename": "Avatar_2009_HDRip.mkv",
            "expected": {"title": "Avatar", "year": "2009"}
        }
    ]
    
    for case in test_cases:
        result = renamer._extract_info_from_filename(case["filename"])
        assert result["title"] == case["expected"]["title"]
        assert result["year"] == case["expected"]["year"]

@pytest.mark.asyncio
async def test_rename_file(renamer, tmp_path):
    """Test file renaming"""
    # Create test file
    original = tmp_path / "The.Matrix.1999.mp4"
    original.write_text("")
    
    metadata = {
        "title": "The Matrix",
        "year": "1999",
        "type": "movie"
    }
    
    new_path = await renamer.rename_file(str(original), metadata)
    assert os.path.exists(new_path)
    assert os.path.basename(new_path) == "The Matrix (1999).mp4"

@pytest.mark.asyncio
async def test_process_directory(renamer, test_files):
    """Test directory processing"""
    results = await renamer.process_directory(str(test_files))
    
    assert len(results) == 4
    for result in results:
        assert result["original"]
        assert result["new"]
        assert result["metadata"]
        
        # Verify file exists
        assert os.path.exists(result["new"])
        
        # Check if NFO file was created
        nfo_path = os.path.splitext(result["new"])[0] + ".nfo"
        if result["metadata"].get("type") in ["movie", "series", "anime"]:
            assert os.path.exists(nfo_path)

@pytest.mark.asyncio
async def test_duplicate_handling(renamer, tmp_path):
    """Test handling of duplicate filenames"""
    # Create two files with same metadata
    file1 = tmp_path / "Matrix.1999.mp4"
    file2 = tmp_path / "The.Matrix.1999.HDRip.mp4"
    file1.write_text("")
    file2.write_text("")
    
    metadata = {
        "title": "The Matrix",
        "year": "1999",
        "type": "movie"
    }
    
    # Rename first file
    new_path1 = await renamer.rename_file(str(file1), metadata)
    assert os.path.basename(new_path1) == "The Matrix (1999).mp4"
    
    # Rename second file
    new_path2 = await renamer.rename_file(str(file2), metadata)
    assert os.path.basename(new_path2) == "The Matrix (1999) [1].mp4"

if __name__ == "__main__":
    pytest.main([__file__])
