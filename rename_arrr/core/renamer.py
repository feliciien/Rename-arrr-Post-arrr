"""
Media file renamer that handles movies, TV shows, and anime.
"""
import os
import re
import logging
import asyncio
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from rename_arrr.core.nfo_generator import NFOGenerator
from rename_arrr.scrapers.base import BaseScraper
from rename_arrr.scrapers.anidb import AniDBScraper
from rename_arrr.scrapers.tvdb import TVDBScraper
from rename_arrr.scrapers.posterdb import PosterDBScraper

logger = logging.getLogger(__name__)

class MediaRenamer:
    def __init__(self):
        self.nfo_generator = NFOGenerator()
        self.scrapers = {
            'anidb': AniDBScraper(),
            'tvdb': TVDBScraper(),
            'posterdb': PosterDBScraper()
        }
        
    async def process_directory(self, directory_path: str) -> List[Dict]:
        """Process all media files in a directory"""
        results = []
        directory = Path(directory_path)
        
        if not directory.exists() or not directory.is_dir():
            logger.error(f"Directory does not exist: {directory_path}")
            return results
            
        for file_path in directory.glob('**/*'):
            if file_path.is_file() and self._is_media_file(file_path):
                info = self._extract_info_from_filename(file_path.name)
                if info:
                    # For testing, use the extracted info as metadata
                    metadata = {
                        'title': info['title'],
                        'year': info.get('year'),
                        'type': info['type'],
                        'season': info.get('season'),
                        'episode': info.get('episode'),
                        'artist': info.get('artist'),
                        'track': info.get('track')
                    }
                    new_path = await self.rename_file(str(file_path), metadata)
                    if new_path:
                        results.append({
                            'original': str(file_path),
                            'new': new_path,
                            'metadata': metadata
                        })
                            
        return results
        
    async def rename_file(self, file_path: str, metadata: Dict) -> Optional[str]:
        """Rename a media file based on metadata"""
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            return None
            
        try:
            directory = os.path.dirname(file_path)
            extension = os.path.splitext(file_path)[1]
            
            # Generate new filename based on metadata
            if metadata.get('type') == 'movie':
                new_name = f"{metadata['title']} ({metadata['year']}){extension}"
            elif metadata.get('type') in ['series', 'anime']:
                season = metadata.get('season', '1')
                episode = metadata.get('episode', '1')
                new_name = f"{metadata['title']} - S{int(season):02d}E{int(episode):02d}{extension}"
            elif metadata.get('type') == 'music':
                track = metadata.get('track', '')
                if track:
                    track = f"{track} - "
                new_name = f"{track}{metadata['artist']} - {metadata['title']}{extension}"
            else:
                logger.warning(f"Unknown media type for: {file_path}")
                return None
                
            # Handle duplicates
            new_path = os.path.join(directory, new_name)
            counter = 1
            while os.path.exists(new_path):
                base, ext = os.path.splitext(new_name)
                new_path = os.path.join(directory, f"{base} [{counter}]{ext}")
                counter += 1
                
            # Rename the file
            os.rename(file_path, new_path)
            
            # Generate NFO file
            self.nfo_generator.create_nfo(metadata, new_path)
            
            logger.info(f"Renamed: {file_path} -> {new_path}")
            return new_path
            
        except Exception as e:
            logger.error(f"Error renaming file {file_path}: {str(e)}")
            return None
            
    def _extract_info_from_filename(self, filename: str) -> Optional[Dict]:
        """Extract title, year, season, and episode info from filename"""
        # Remove extension and replace dots/underscores with spaces
        name = os.path.splitext(filename)[0]
        original_name = name  # Keep original for year extraction
        name = name.replace('.', ' ').replace('_', ' ')

        # Check if it's a music file pattern (XX Artist - Title)
        music_match = re.match(r'^(\d+\s+)?(.+?)\s*-\s*(.+?)$', name)
        if music_match:
            track_num = music_match.group(1)
            artist = music_match.group(2).strip()
            title = music_match.group(3).strip()
            return {
                'title': title,
                'artist': artist,
                'track': track_num.strip() if track_num else None,
                'type': 'music'
            }

        # Try to extract year first from original name
        year_match = re.search(r'\b(19|20)\d{2}\b', original_name)
        year = year_match.group(0) if year_match else None
        
        # Remove quality tags and other common patterns
        patterns_to_remove = [
            r'\b\d{3,4}p\b',  # Resolution (720p, 1080p, etc.)
            r'\bBluRay\b',
            r'\bBRRip\b',
            r'\bWEB-?DL\b',
            r'\bHDRip\b',
            r'\bDVDRip\b',
            r'\bHDTV\b',
            r'\bx264\b',
            r'\bAAC\b',
            r'\bAC3\b',
            r'\b10bit\b',
            r'\bHEVC\b',
            r'\bH\.?264\b',
            r'\bBT2020\b',
            r'\bDTS\b',
            r'\bDD5\.1\b',
            r'\[.*?\]',  # Anything in square brackets
            r'\(.*?\)',  # Anything in parentheses except years
        ]
        
        clean_name = name
        for pattern in patterns_to_remove:
            clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)
            
        # Clean up multiple spaces and strip
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        
        # Try to extract season/episode
        episode_match = re.search(r'[Ss](\d{1,2})[Ee](\d{1,2})', clean_name)
        if episode_match:
            season = int(episode_match.group(1))
            episode = int(episode_match.group(2))
            # Remove season/episode from title
            title = clean_name[:episode_match.start()].strip()
            return {
                'title': title,
                'year': year,
                'type': 'series',
                'season': season,
                'episode': episode
            }
            
        # If no season/episode, treat as movie
        # Try to find the year in the clean name if not found in original
        if not year:
            year_match = re.search(r'\b(19|20)\d{2}\b', clean_name)
            year = year_match.group(0) if year_match else None
            
        if year:
            # Find the year in the clean name to get the title
            year_match = re.search(re.escape(year), clean_name)
            if year_match:
                title = clean_name[:year_match.start()].strip()
            else:
                title = clean_name.strip()
        else:
            title = clean_name.strip()
            
        return {
            'title': title,
            'year': year,
            'type': 'movie'
        }
        
    async def _fetch_metadata(self, info: Dict) -> Optional[Dict]:
        """Fetch metadata from available scrapers"""
        try:
            # Start with basic info from filename
            metadata = {
                'title': info['title'],
                'year': info['year'],
                'type': info['type']
            }
            
            # Add season/episode info if present
            if 'season' in info:
                metadata['season'] = info['season']
            if 'episode' in info:
                metadata['episode'] = info['episode']
                
            # Try to fetch additional metadata from scrapers
            for scraper in self.scrapers.values():
                try:
                    additional_metadata = await scraper.fetch_metadata(info)
                    if additional_metadata:
                        metadata.update(additional_metadata)
                        break
                except Exception as e:
                    logger.warning(f"Error fetching metadata from {scraper.__class__.__name__}: {str(e)}")
                    
            return metadata
            
        except Exception as e:
            logger.error(f"Error fetching metadata: {str(e)}")
            return None
            
    def _is_media_file(self, file_path: Path) -> bool:
        """Check if file is a supported media file"""
        media_extensions = {
            # Video files
            '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv',
            # Audio files
            '.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'
        }
        return file_path.suffix.lower() in media_extensions
