# Rename-arrr 🏴‍☠️

A powerful media file renaming tool with metadata fetching and organization features. Rename-arrr helps you organize your media library by automatically fetching metadata from various sources and renaming files according to your preferences.

## Features

### Core Features
- Rename movies, TV shows, anime files, and music files using metadata from multiple sources
- Create NFO files compatible with Emby, Plex, and Kodi
- Download posters and artwork
- Support for both GUI and CLI interfaces
- Individual file and batch processing
- Undo/history functionality

### Metadata Sources
- **Anime**: AniDB (direct scraping)
- **TV Shows**: TheTVDB (API and direct scraping)
- **Artwork**: ThePosterDB (direct scraping)
- **Music**: File metadata and online databases

### File Organization
- Intelligent title, artist, and year extraction
- Configurable naming patterns
- Handles duplicates automatically
- Creates proper folder structures
- Supports various media formats

### Supported Formats
- **Video**: MP4, MKV, AVI, MOV, WMV, FLV
- **Audio**: MP3, WAV, FLAC, M4A, AAC, OGG

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- PyQt5 (for GUI)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/feliciien/Rename-arrr-Post-arrr.git
cd Rename-arrr-Post-arrr
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Usage

### Graphical Interface (GUI)

Run the GUI version:
```bash
python -m rename_arrr.gui.main_window
```

The GUI provides:
- Individual file selection
- Multi-file selection support
- File list view with clear option
- Progress tracking per file
- Real-time feedback
- Media type selection (Auto/Movies/TV Shows/Music)
- Options for NFO generation and poster downloads

### Command Line Interface (CLI)

Basic usage:
```bash
rename-arrr --files file1.mp4 file2.mp3
```

Advanced options:
```bash
rename-arrr --files video.mkv --type anime --no-nfo --no-posters
```

Available options:
- `--files`: Space-separated list of files to process
- `--type`, `-t`: Media type (auto/anime/series/movie/music)
- `--no-nfo`: Skip NFO file generation
- `--no-posters`: Skip poster downloads

## Configuration

The application supports various configuration options:

### Media Types
- Auto-detect (default)
- Anime
- TV Series
- Movies
- Music

### NFO Files
- Creates compatible NFO files for:
  - Emby
  - Plex
  - Kodi (XBMC)

### Naming Patterns
- Movies: Title (Year)
- TV Shows: Title - SXXEXX
- Music: [Track#] Artist - Title

## Development

### Project Structure
```
Rename-arrr/
├── core/
│   ├── renamer.py
│   └── nfo_generator.py
├── scrapers/
│   ├── anidb_scraper.py
│   ├── tvdb_scraper.py
│   └── posterdb_scraper.py
├── gui/
│   └── main_window.py
├── cli.py
└── __main__.py
```

### Running Tests
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by FileBot and MetaX
- Uses various open-source libraries and APIs
- Thanks to all contributors
