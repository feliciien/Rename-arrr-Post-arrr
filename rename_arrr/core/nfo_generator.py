"""
NFO file generator for various media servers (Emby, Plex, Kodi)
"""
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class NFOGenerator:
    def __init__(self):
        self.supported_servers = ['emby', 'plex', 'kodi']
        
    def create_nfo(self, metadata: Dict, target_path: str, server_type: str = 'kodi') -> bool:
        """Create NFO file based on media type"""
        if not metadata or server_type not in self.supported_servers:
            return False
            
        try:
            media_type = metadata.get('type', 'movie')
            if media_type == 'movie':
                return self.create_movie_nfo(metadata, target_path, server_type)
            elif media_type in ['series', 'anime']:
                if metadata.get('episode'):
                    return self.create_episode_nfo(metadata, target_path, server_type)
                else:
                    return self.create_tvshow_nfo(metadata, target_path, server_type)
            return False
            
        except Exception as e:
            logger.error(f"Error creating NFO file: {str(e)}")
            return False
            
    def create_movie_nfo(self, metadata: Dict, target_path: str, server_type: str = 'kodi') -> bool:
        """Create movie NFO file"""
        root = ET.Element('movie')
        
        # Add basic metadata
        self._add_basic_metadata(root, metadata)
        
        # Add movie-specific metadata
        runtime = ET.SubElement(root, 'runtime')
        runtime.text = str(metadata.get('runtime', ''))
        
        tagline = ET.SubElement(root, 'tagline')
        tagline.text = metadata.get('tagline', '')
        
        # Add external IDs
        uniqueid = ET.SubElement(root, 'uniqueid')
        if metadata.get('imdb_id'):
            uniqueid.set('type', 'imdb')
            uniqueid.text = metadata['imdb_id']
        elif metadata.get('tmdb_id'):
            uniqueid.set('type', 'tmdb')
            uniqueid.text = str(metadata['tmdb_id'])
            
        return self._write_nfo(root, target_path)
        
    def create_tvshow_nfo(self, metadata: Dict, target_path: str, server_type: str = 'kodi') -> bool:
        """Create TV show NFO file"""
        root = ET.Element('tvshow')
        
        # Add basic metadata
        self._add_basic_metadata(root, metadata)
        
        # Add TV show specific metadata
        status = ET.SubElement(root, 'status')
        status.text = metadata.get('status', '')
        
        aired = ET.SubElement(root, 'aired')
        aired.text = metadata.get('first_aired', '')
        
        studio = ET.SubElement(root, 'studio')
        studio.text = metadata.get('network', '')
        
        # Add season details if available
        if metadata.get('seasons'):
            for season in metadata['seasons']:
                season_elem = ET.SubElement(root, 'season')
                season_elem.text = str(season.get('number', ''))
                
        # Add external IDs
        uniqueid = ET.SubElement(root, 'uniqueid')
        if metadata.get('tvdb_id'):
            uniqueid.set('type', 'tvdb')
            uniqueid.text = str(metadata['tvdb_id'])
            
        return self._write_nfo(root, target_path)
        
    def create_episode_nfo(self, metadata: Dict, target_path: str, server_type: str = 'kodi') -> bool:
        """Create episode NFO file"""
        root = ET.Element('episodedetails')
        
        # Add basic metadata
        self._add_basic_metadata(root, metadata)
        
        # Add episode-specific metadata
        season = ET.SubElement(root, 'season')
        season.text = str(metadata.get('season', '1'))
        
        episode = ET.SubElement(root, 'episode')
        episode.text = str(metadata.get('episode', '1'))
        
        aired = ET.SubElement(root, 'aired')
        aired.text = metadata.get('air_date', '')
        
        # Add show information
        showtitle = ET.SubElement(root, 'showtitle')
        showtitle.text = metadata.get('series_name', metadata.get('title', ''))
        
        return self._write_nfo(root, target_path)
        
    def _add_basic_metadata(self, root: ET.Element, metadata: Dict) -> None:
        """Add basic metadata common to all types"""
        # Title
        title = ET.SubElement(root, 'title')
        title.text = metadata.get('title', '')
        
        # Original title if different
        if metadata.get('original_title') and metadata['original_title'] != metadata.get('title'):
            originaltitle = ET.SubElement(root, 'originaltitle')
            originaltitle.text = metadata['original_title']
            
        # Year
        year = ET.SubElement(root, 'year')
        year.text = str(metadata.get('year', ''))
        
        # Plot/Overview
        plot = ET.SubElement(root, 'plot')
        plot.text = metadata.get('overview', '')
        
        # Rating
        if metadata.get('rating'):
            rating = ET.SubElement(root, 'rating')
            rating.text = str(metadata['rating'])
            
        # Genres
        if metadata.get('genres'):
            for genre in metadata['genres']:
                genre_elem = ET.SubElement(root, 'genre')
                genre_elem.text = genre
                
        # Cast
        if metadata.get('cast'):
            for actor in metadata['cast']:
                actor_elem = ET.SubElement(root, 'actor')
                name = ET.SubElement(actor_elem, 'name')
                name.text = actor.get('name', '')
                if actor.get('role'):
                    role = ET.SubElement(actor_elem, 'role')
                    role.text = actor['role']
                if actor.get('thumb'):
                    thumb = ET.SubElement(actor_elem, 'thumb')
                    thumb.text = actor['thumb']
                    
        # Add poster and fanart paths if available
        if metadata.get('poster_path'):
            poster = ET.SubElement(root, 'thumb')
            poster.text = metadata['poster_path']
            
        if metadata.get('fanart_path'):
            fanart = ET.SubElement(root, 'fanart')
            thumb = ET.SubElement(fanart, 'thumb')
            thumb.text = metadata['fanart_path']
            
    def _write_nfo(self, root: ET.Element, target_path: str) -> bool:
        """Write NFO file to disk"""
        try:
            tree = ET.ElementTree(root)
            nfo_path = os.path.splitext(target_path)[0] + '.nfo'
            tree.write(nfo_path, encoding='utf-8', xml_declaration=True)
            logger.info(f"Created NFO file: {nfo_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing NFO file: {str(e)}")
            return False
