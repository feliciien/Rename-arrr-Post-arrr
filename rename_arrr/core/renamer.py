"""
Core media renaming functionality
"""
import os
import re
import logging
import asyncio
from pathlib import Path
from typing import Dict, Optional, List, Tuple

from rename_arrr.scrapers.tvdb import TVDBScraper
from rename_arrr.scrapers.anidb import AniDBScraper
from rename_arrr.scrapers.posterdb import PosterDBScraper
from rename_arrr.core.nfo import NFOGenerator
from rename_arrr.scrapers.musicbrainz import MusicBrainzScraper

logger = logging.getLogger(__name__)

class MediaRenamer:
    """Handle media file renaming operations"""
    
    def __init__(self):
        self.tvdb = TVDBScraper()
        self.anidb = AniDBScraper()
        self.posterdb = PosterDBScraper()
        self.musicbrainz = MusicBrainzScraper()
        self.nfo_gen = NFOGenerator()
        
    async def rename_file(self, file_path: str, metadata: Dict) -> Optional[str]:
        """Rename a single file based on metadata"""
        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"File not found: {file_path}")
                return None
                
            # Get new filename
            new_name = self._generate_filename(path, metadata)
            if not new_name:
                return None
                
            # Create new path
            new_path = path.parent / new_name
            
            # Handle duplicates
            counter = 1
            while new_path.exists():
                base = new_path.stem
                ext = new_path.suffix
                new_path = path.parent / f"{base} [{counter}]{ext}"
                counter += 1
            
            # Create NFO file
            if metadata.get('type') == 'movie':
                nfo_path = new_path.with_suffix('.nfo')
                self.nfo_gen.create_movie_nfo(metadata, nfo_path)
            elif metadata.get('type') == 'series':
                show_nfo = path.parent / 'tvshow.nfo'
                if not show_nfo.exists():
                    self.nfo_gen.create_tvshow_nfo(metadata, show_nfo)
                episode_nfo = new_path.with_suffix('.nfo')
                self.nfo_gen.create_episode_nfo(metadata, episode_nfo)
            elif metadata.get('type') == 'anime':
                show_nfo = path.parent / 'tvshow.nfo'
                if not show_nfo.exists():
                    self.nfo_gen.create_tvshow_nfo(metadata, show_nfo)
                episode_nfo = new_path.with_suffix('.nfo')
                self.nfo_gen.create_episode_nfo(metadata, episode_nfo)
            elif metadata.get('type') == 'music':
                if 'album' in metadata:
                    album_nfo = path.parent / 'album.nfo'
                    if not album_nfo.exists():
                        self.nfo_gen.create_album_nfo(metadata, album_nfo)
                song_nfo = new_path.with_suffix('.nfo')
                self.nfo_gen.create_song_nfo(metadata, song_nfo)
            
            # Download artwork if available
            if metadata.get('cover_url'):
                if metadata.get('type') == 'music':
                    art_path = path.parent / 'folder.jpg'
                else:
                    art_path = path.parent / 'poster.jpg'
                    
                if metadata['source'] == 'posterdb':
                    await self.posterdb.download_image(metadata['cover_url'], art_path)
                elif metadata['source'] == 'tvdb':
                    await self.tvdb.download_image(metadata['cover_url'], art_path)
                elif metadata['source'] == 'anidb':
                    await self.anidb.download_image(metadata['cover_url'], art_path)
                elif metadata['source'] == 'musicbrainz':
                    await self.musicbrainz.download_image(metadata['cover_url'], art_path)
            
            # Rename file
            path.rename(new_path)
            logger.info(f"Renamed: {path.name} -> {new_path.name}")
            
            return str(new_path)
            
        except Exception as e:
            logger.error(f"Error renaming file: {str(e)}")
            return None
    
    def _generate_filename(self, path: Path, metadata: Dict) -> Optional[str]:
        """Generate new filename based on metadata"""
        try:
            # Handle known show name capitalizations
            known_capitalizations = {
                'swat': 'S.W.A.T.',
                'shield': 'S.H.I.E.L.D.',
                'ncis': 'NCIS',
                'csi': 'CSI'
            }

            if metadata.get('type') == 'movie':
                # Movie format: Title (Year).ext
                title = metadata.get('title', path.stem)
                year = metadata.get('year', '')
                return f"{title} ({year}){path.suffix}"
                
            elif metadata.get('type') in ('series', 'anime'):
                # TV format: Title - SXXEYY.ext
                title = metadata.get('title', path.stem)
                # Check for known capitalizations
                title_lower = title.lower()
                if title_lower in known_capitalizations:
                    title = known_capitalizations[title_lower]
                season = metadata.get('season', '1')
                episode = metadata.get('episode', '1')
                return f"{title} - S{int(season):02d}E{int(episode):02d}{path.suffix}"
                
            elif metadata.get('type') == 'music':
                # Music format: [Track#] Artist - Title.ext
                track = metadata.get('track', '')
                artist = metadata.get('artist', '')
                title = metadata.get('title', path.stem)
                
                if track:
                    if 'album' in metadata:
                        # Album track format: XX - Title.ext
                        return f"{int(track):02d} - {title}{path.suffix}"
                    else:
                        # Single track format: Artist - Title.ext
                        return f"{artist} - {title}{path.suffix}"
                else:
                    return f"{artist} - {title}{path.suffix}"
                
            else:
                logger.warning(f"Unknown media type for: {path}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating filename: {str(e)}")
            return None
    
    async def fetch_metadata(self, file_path: str) -> Optional[Dict]:
        """Fetch metadata for a file"""
        try:
            info = self._extract_info_from_filename(os.path.basename(file_path))
            if not info:
                return None
            
            # Try different scrapers based on type
            if info['type'] == 'music':
                if 'album' in info:
                    # Search for album first
                    results = await self.musicbrainz.search_release(info['album'], info['artist'])
                    if results:
                        metadata = await self.musicbrainz.get_release_metadata(results[0]['id'])
                        if metadata:
                            # Find the specific track
                            for track in metadata.get('tracks', []):
                                if track['number'] == info['track'] or track['title'].lower() == info['title'].lower():
                                    metadata.update({
                                        'track': track['number'],
                                        'title': track['title'],
                                        'length': track['length']
                                    })
                                    break
                            # Get cover art
                            cover_url = await self.musicbrainz.get_cover_art(results[0]['id'])
                            if cover_url:
                                metadata['cover_url'] = cover_url
                            return metadata
                else:
                    # Search for artist first
                    artist_results = await self.musicbrainz.search_artist(info['artist'])
                    if artist_results:
                        # Then search for tracks by this artist
                        release_results = await self.musicbrainz.search_release(info['title'], artist_results[0]['name'])
                        if release_results:
                            metadata = await self.musicbrainz.get_release_metadata(release_results[0]['id'])
                            if metadata:
                                # Get cover art
                                cover_url = await self.musicbrainz.get_cover_art(release_results[0]['id'])
                                if cover_url:
                                    metadata['cover_url'] = cover_url
                                return metadata
            
            elif info['type'] == 'anime':
                results = await self.anidb.search(info['title'])
                if results:
                    metadata = await self.anidb.get_metadata(results[0]['url'])
                    if metadata:
                        metadata['type'] = 'anime'
                        metadata['season'] = info.get('season')
                        metadata['episode'] = info.get('episode')
                        return metadata
            
            elif info['type'] == 'series':
                results = await self.tvdb.search(info['title'])
                if results:
                    metadata = await self.tvdb.get_metadata(results[0]['url'])
                    if metadata:
                        metadata['type'] = 'series'
                        metadata['season'] = info.get('season')
                        metadata['episode'] = info.get('episode')
                        return metadata
            
            # Fallback to basic info
            return info
            
        except Exception as e:
            logger.error(f"Error fetching metadata: {str(e)}")
            return None
    
    def _extract_info_from_filename(self, filename: str) -> Optional[Dict]:
        """Extract title, year, season, and episode info from filename"""
        # Remove extension and replace dots/underscores with spaces
        name = os.path.splitext(filename)[0]
        original_name = name  # Keep original for year extraction
        name = name.replace('.', ' ').replace('_', ' ').replace('-', ' ')
        
        # Check for common music file patterns
        music_patterns = [
            # Pattern: 01 - Artist - Title
            r'^(\d+)\s*-\s*(.+?)\s*-\s*(.+?)$',
            # Pattern: Artist - Title
            r'^(.+?)\s*-\s*(.+?)$',
            # Pattern: Artist - Album - 01 - Title
            r'^(.+?)\s*-\s*(.+?)\s*-\s*(\d+)\s*-\s*(.+?)$'
        ]
        
        for pattern in music_patterns:
            match = re.match(pattern, name)
            if match:
                groups = match.groups()
                if len(groups) == 3:  # 01 - Artist - Title
                    return {
                        'track': groups[0].strip(),
                        'artist': groups[1].strip(),
                        'title': groups[2].strip(),
                        'type': 'music'
                    }
                elif len(groups) == 2:  # Artist - Title
                    return {
                        'artist': groups[0].strip(),
                        'title': groups[1].strip(),
                        'type': 'music'
                    }
                elif len(groups) == 4:  # Artist - Album - 01 - Title
                    return {
                        'artist': groups[0].strip(),
                        'album': groups[1].strip(),
                        'track': groups[2].strip(),
                        'title': groups[3].strip(),
                        'type': 'music'
                    }
        
        # Check for common anime release group tags
        anime_groups = ['HorribleSubs', 'Erai-raws', 'SubsPlease', 'Commie', 'UTW', 'Underwater']
        is_anime = any(group.lower() in original_name.lower() for group in anime_groups)
        
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
            r'\bdd51\b',  # Added
            r'\bded\b',   # Added
            r'\bdl\b',    # Added
            r'\b7p\b',    # Added
            r'\bazhd\b',  # Added
            r'\btvs\b',   # Added
            r'\[.*?\]',   # Anything in square brackets
            r'\(.*?\)',   # Anything in parentheses except years
        ]
        
        clean_name = name
        for pattern in patterns_to_remove:
            clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and strip
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        
        # Try to extract year first from original name
        year_match = re.search(r'\b(19|20)\d{2}\b', original_name)
        year = year_match.group(0) if year_match else None
        
        # Try to match TV show patterns
        tv_patterns = [
            r'(.+?)[-\s]+[Ss](\d{1,2})[Ee](\d{1,2})',  # S01E01 format
            r'(.+?)[-\s]+(\d)(\d{2})',                  # 101 format (1 digit season)
            r'(.+?)[-\s]+(\d{2})(\d{2})',               # 1001 format (2 digit season)
        ]
        
        for pattern in tv_patterns:
            tv_match = re.search(pattern, clean_name)
            if tv_match:
                title = tv_match.group(1).strip()
                return {
                    'title': title,
                    'year': year,
                    'type': 'anime' if is_anime else 'series',
                    'season': tv_match.group(2),
                    'episode': tv_match.group(3)
                }
        
        # Try to match standalone episode number (like "101")
        episode_match = re.search(r'(\d{2,3})(?:\s|$)', clean_name)
        if episode_match:
            episode_num = episode_match.group(1)
            if len(episode_num) == 3:
                season = episode_num[0]
                episode = episode_num[1:]
            else:
                season = '1'
                episode = episode_num
                
            # Get title by removing the episode number
            title = clean_name[:episode_match.start()].strip()
            return {
                'title': title,
                'year': year,
                'type': 'anime' if is_anime else 'series',
                'season': season,
                'episode': episode
            }
        
        # If no TV/anime pattern, treat as movie
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

    async def close(self):
        """Close all scrapers"""
        await self.tvdb.close()
        await self.anidb.close()
        await self.posterdb.close()
        await self.musicbrainz.close()
