"""
MusicBrainz scraper for fetching music metadata
"""
import re
import asyncio
import aiohttp
import logging
from typing import Dict, Optional, List
from pathlib import Path
import musicbrainzngs as mb

logger = logging.getLogger(__name__)

class MusicBrainzScraper:
    """Scraper for MusicBrainz"""
    
    def __init__(self):
        # Set up MusicBrainz client
        mb.set_useragent(
            "Rename-arrr",
            "1.0",
            "https://github.com/yourusername/rename-arrr"
        )
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def _init_session(self):
        """Initialize aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def search_artist(self, artist_name: str) -> List[Dict]:
        """Search for an artist"""
        try:
            result = mb.search_artists(artist_name)
            artists = []
            
            for artist in result['artist-list']:
                artists.append({
                    'id': artist['id'],
                    'name': artist['name'],
                    'type': artist.get('type', ''),
                    'country': artist.get('country', ''),
                    'score': artist.get('ext:score', '0')
                })
            
            return sorted(artists, key=lambda x: int(x['score']), reverse=True)
            
        except Exception as e:
            logger.error(f"Error searching artist: {str(e)}")
            return []
    
    async def search_release(self, album: str, artist: str = None) -> List[Dict]:
        """Search for an album release"""
        try:
            query = f'release:{album}'
            if artist:
                query += f' AND artist:{artist}'
            
            result = mb.search_releases(query)
            releases = []
            
            for release in result['release-list']:
                releases.append({
                    'id': release['id'],
                    'title': release['title'],
                    'artist': release['artist-credit-phrase'],
                    'date': release.get('date', ''),
                    'country': release.get('country', ''),
                    'score': release.get('ext:score', '0')
                })
            
            return sorted(releases, key=lambda x: int(x['score']), reverse=True)
            
        except Exception as e:
            logger.error(f"Error searching release: {str(e)}")
            return []
    
    async def get_release_metadata(self, release_id: str) -> Optional[Dict]:
        """Get detailed metadata for a release"""
        try:
            result = mb.get_release_by_id(
                release_id,
                includes=['recordings', 'artists', 'release-groups']
            )
            release = result['release']
            
            metadata = {
                'title': release['title'],
                'artist': release['artist-credit-phrase'],
                'date': release.get('date', ''),
                'country': release.get('country', ''),
                'type': 'music',
                'tracks': []
            }
            
            # Add track information
            if 'medium-list' in release:
                for medium in release['medium-list']:
                    if 'track-list' in medium:
                        for track in medium['track-list']:
                            metadata['tracks'].append({
                                'number': track['number'],
                                'title': track['recording']['title'],
                                'length': track['recording'].get('length', '')
                            })
            
            # Add release group information
            if 'release-group' in release:
                group = release['release-group']
                metadata['album'] = group['title']
                metadata['type'] = group.get('type', 'Album')
                
            return metadata
            
        except Exception as e:
            logger.error(f"Error getting release metadata: {str(e)}")
            return None
    
    async def get_cover_art(self, release_id: str) -> Optional[str]:
        """Get cover art URL for a release"""
        try:
            result = mb.get_image_list(release_id)
            if result and 'images' in result:
                for image in result['images']:
                    if image.get('front', False):
                        return image.get('image')
            return None
            
        except Exception as e:
            logger.error(f"Error getting cover art: {str(e)}")
            return None
    
    async def download_image(self, url: str, save_path: Path) -> bool:
        """Download image from URL"""
        await self._init_session()
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download image: {response.status}")
                    return False
                
                save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
                return True
                
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            return False
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None
