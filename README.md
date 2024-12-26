# Rename-arrr 🏴‍☠️

A powerful media file renaming tool with metadata fetching and organization features. Rename-arrr helps you organize your media library by automatically fetching metadata from various sources and renaming files according to your preferences.

## ✨ Features

### 🎯 Core Features (Milestone 1 Completed)
- Rename movies, TV shows, anime files, and music files using metadata from multiple sources
- Create NFO files compatible with Emby, Plex, and Kodi
- Download posters and artwork automatically
- Modern GUI with real-time progress tracking
- Powerful CLI for automation and scripting
- Individual file and batch processing
- Smart media type detection

### 🔍 Metadata Sources
- **Anime**: AniDB (direct scraping)
  - Series information
  - Episode details
  - Artwork and posters
- **TV Shows**: TheTVDB (API and direct scraping)
  - Series metadata
  - Episode information
  - Cast and crew details
- **Artwork**: ThePosterDB (direct scraping)
  - High-quality posters
  - Season artwork
  - Series banners
- **Music**: MusicBrainz
  - Artist information
  - Album details
  - Track metadata

### 📁 File Organization
- Intelligent title, artist, and year extraction
- Configurable naming patterns
- Handles duplicates automatically
- Creates proper folder structures
- Supports various media formats

### 📺 Supported Formats
- **Video**: MP4, MKV, AVI, MOV, WMV, FLV
- **Audio**: MP3, WAV, FLAC, M4A, AAC, OGG

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- PyQt5 (for GUI)

### Installation

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

## 💻 Usage

### GUI Interface

Launch the GUI:
```bash
python run_gui.py
```

Features:
- 🖱️ Drag-and-drop file selection
- 📋 File list management
- 📊 Real-time progress tracking
- 🎭 Media type auto-detection
- 🎨 Poster preview and download
- 📝 NFO file generation options

### CLI Interface

Basic usage:
```bash
python -m rename_arrr.cli.main --files "path/to/files/*"
```

Advanced options:
```bash
python -m rename_arrr.cli.main --files video.mkv --type anime --scraper anidb --no-nfo --no-posters
```

Available arguments:
- `--files`: Files or glob patterns to process
- `--type`: Media type (auto/anime/series/movie/music)
- `--scraper`: Metadata source (anidb/tvdb/posterdb/musicbrainz)
- `--no-nfo`: Skip NFO file generation
- `--no-posters`: Skip poster downloads
- `--dry-run`: Show changes without applying them

## ⚙️ Configuration

### Media Types
- 🎬 Movies
  - Title and year extraction
  - Cast and crew metadata
  - Movie posters
- 📺 TV Shows
  - Series and episode detection
  - Season organization
  - Episode metadata
- 🎌 Anime
  - Episode numbering
  - Series information
  - Alternative titles
- 🎵 Music
  - Artist and album detection
  - Track numbering
  - Album artwork

### Naming Patterns
Default patterns (customizable):
- Movies: `{title} ({year})`
- TV Shows: `{series} - S{season:02d}E{episode:02d} - {title}`
- Anime: `{series} - {episode:03d} - {title}`
- Music: `{artist} - {album} - {track:02d} - {title}`

## 🧪 Testing

1. Run the included demo script:
```bash
python tests/milestone1_demo.py
```

2. Use the test media files in `test_media/`:
- Movies: `The.Matrix.1999.mp4`
- TV Shows: `Breaking.Bad.S01E01.mp4`
- Anime: `Naruto.Episode.001.mp4`
- Music: `Pink.Floyd.-.Dark.Side.of.the.Moon.01.-.Speak.to.Me.mp3`

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AniDB for anime metadata
- TheTVDB for TV show information
- ThePosterDB for artwork
- MusicBrainz for music metadata
