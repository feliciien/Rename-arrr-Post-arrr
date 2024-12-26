"""
NFO file generator for various media centers
"""
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class NFOGenerator:
    """Generate NFO files for various media centers"""
    
    @staticmethod
    def create_movie_nfo(metadata: Dict, save_path: Path) -> bool:
        """Create movie NFO file"""
        try:
            # Create root element
            root = ET.Element("movie")
            
            # Add basic metadata
            title = ET.SubElement(root, "title")
            title.text = metadata.get('title', '')
            
            year = ET.SubElement(root, "year")
            year.text = metadata.get('year', '')
            
            plot = ET.SubElement(root, "plot")
            plot.text = metadata.get('overview', '')
            
            rating = ET.SubElement(root, "rating")
            rating.text = metadata.get('rating', '')
            
            # Add genres
            for genre in metadata.get('genres', []):
                genre_elem = ET.SubElement(root, "genre")
                genre_elem.text = genre
            
            # Add poster if available
            if metadata.get('poster_url'):
                thumb = ET.SubElement(root, "thumb")
                thumb.text = metadata['poster_url']
            
            # Save file
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            save_path.write_text(xml_str, encoding='utf-8')
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating movie NFO: {str(e)}")
            return False
    
    @staticmethod
    def create_tvshow_nfo(metadata: Dict, save_path: Path) -> bool:
        """Create TV show NFO file"""
        try:
            # Create root element
            root = ET.Element("tvshow")
            
            # Add basic metadata
            title = ET.SubElement(root, "title")
            title.text = metadata.get('title', '')
            
            year = ET.SubElement(root, "year")
            year.text = metadata.get('year', '')
            
            plot = ET.SubElement(root, "plot")
            plot.text = metadata.get('overview', '')
            
            rating = ET.SubElement(root, "rating")
            rating.text = metadata.get('rating', '')
            
            # Add episode info if available
            if metadata.get('episodes'):
                episodes = ET.SubElement(root, "episodes")
                episodes.text = metadata['episodes']
            
            # Add genres
            for genre in metadata.get('genres', []):
                genre_elem = ET.SubElement(root, "genre")
                genre_elem.text = genre
            
            # Add poster if available
            if metadata.get('poster_url'):
                thumb = ET.SubElement(root, "thumb")
                thumb.text = metadata['poster_url']
            
            # Save file
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            save_path.write_text(xml_str, encoding='utf-8')
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating TV show NFO: {str(e)}")
            return False
    
    @staticmethod
    def create_episode_nfo(metadata: Dict, save_path: Path) -> bool:
        """Create episode NFO file"""
        try:
            # Create root element
            root = ET.Element("episodedetails")
            
            # Add basic metadata
            title = ET.SubElement(root, "title")
            title.text = metadata.get('title', '')
            
            season = ET.SubElement(root, "season")
            season.text = str(metadata.get('season', '1'))
            
            episode = ET.SubElement(root, "episode")
            episode.text = str(metadata.get('episode', '1'))
            
            plot = ET.SubElement(root, "plot")
            plot.text = metadata.get('overview', '')
            
            rating = ET.SubElement(root, "rating")
            rating.text = metadata.get('rating', '')
            
            # Add aired date if available
            if metadata.get('aired'):
                aired = ET.SubElement(root, "aired")
                aired.text = metadata['aired']
            
            # Add poster if available
            if metadata.get('poster_url'):
                thumb = ET.SubElement(root, "thumb")
                thumb.text = metadata['poster_url']
            
            # Save file
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            save_path.write_text(xml_str, encoding='utf-8')
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating episode NFO: {str(e)}")
            return False

    @staticmethod
    def create_album_nfo(metadata: Dict, save_path: Path) -> bool:
        """Create album NFO file"""
        try:
            # Create root element
            root = ET.Element("album")
            
            # Add basic metadata
            title = ET.SubElement(root, "title")
            title.text = metadata.get('title', '')
            
            artist = ET.SubElement(root, "artist")
            artist.text = metadata.get('artist', '')
            
            year = ET.SubElement(root, "year")
            year.text = metadata.get('date', '').split('-')[0] if metadata.get('date') else ''
            
            genre = ET.SubElement(root, "genre")
            genre.text = metadata.get('genre', '')
            
            type_elem = ET.SubElement(root, "type")
            type_elem.text = metadata.get('type', 'Album')
            
            # Add tracks
            tracks = ET.SubElement(root, "tracks")
            for track in metadata.get('tracks', []):
                track_elem = ET.SubElement(tracks, "track")
                
                number = ET.SubElement(track_elem, "position")
                number.text = track.get('number', '')
                
                track_title = ET.SubElement(track_elem, "title")
                track_title.text = track.get('title', '')
                
                duration = ET.SubElement(track_elem, "duration")
                duration.text = track.get('length', '')
            
            # Add cover art if available
            if metadata.get('cover_url'):
                thumb = ET.SubElement(root, "thumb")
                thumb.text = metadata['cover_url']
            
            # Save file
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            save_path.write_text(xml_str, encoding='utf-8')
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating album NFO: {str(e)}")
            return False
    
    @staticmethod
    def create_song_nfo(metadata: Dict, save_path: Path) -> bool:
        """Create song NFO file"""
        try:
            # Create root element
            root = ET.Element("song")
            
            # Add basic metadata
            title = ET.SubElement(root, "title")
            title.text = metadata.get('title', '')
            
            artist = ET.SubElement(root, "artist")
            artist.text = metadata.get('artist', '')
            
            album = ET.SubElement(root, "album")
            album.text = metadata.get('album', '')
            
            track = ET.SubElement(root, "track")
            track.text = metadata.get('track', '')
            
            year = ET.SubElement(root, "year")
            year.text = metadata.get('date', '').split('-')[0] if metadata.get('date') else ''
            
            genre = ET.SubElement(root, "genre")
            genre.text = metadata.get('genre', '')
            
            duration = ET.SubElement(root, "duration")
            duration.text = metadata.get('length', '')
            
            # Add cover art if available
            if metadata.get('cover_url'):
                thumb = ET.SubElement(root, "thumb")
                thumb.text = metadata['cover_url']
            
            # Save file
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            save_path.write_text(xml_str, encoding='utf-8')
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating song NFO: {str(e)}")
            return False
