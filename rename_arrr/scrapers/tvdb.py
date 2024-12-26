"""
TVDB scraper implementation
"""
import logging
from typing import Dict, Optional
import aiohttp

from .base import BaseScraper

logger = logging.getLogger(__name__)

class TVDBScraper(BaseScraper):
    """Scraper for TVDB"""
    
    def __init__(self):
        self.base_url = "https://api.thetvdb.com/v4"
        
    async def fetch_metadata(self, info: Dict) -> Optional[Dict]:
        """Fetch metadata for a TV show"""
        try:
            # For now, just return the basic info since we don't have API access
            return {
                'title': info['title'],
                'year': info['year'],
                'type': 'series',
                'season': info.get('season'),
                'episode': info.get('episode')
            }
        except Exception as e:
            logger.error(f"Error fetching metadata from TVDB: {str(e)}")
            return None
            
    async def search(self, query: str) -> Optional[Dict]:
        """Search for a TV show"""
        # Implement when we have API access
        return None
        
    async def get_images(self, media_id: str) -> Optional[Dict]:
        """Get images for a TV show"""
        # Implement when we have API access
        return None
