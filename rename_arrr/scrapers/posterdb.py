"""
PosterDB scraper implementation
"""
import logging
from typing import Dict, Optional
import aiohttp

from .base import BaseScraper

logger = logging.getLogger(__name__)

class PosterDBScraper(BaseScraper):
    """Scraper for ThePosterDB"""
    
    def __init__(self):
        self.base_url = "https://api.theposterdb.com/v1"
        
    async def fetch_metadata(self, info: Dict) -> Optional[Dict]:
        """Fetch metadata for posters"""
        try:
            # For now, just return None since we mainly use this for images
            return None
        except Exception as e:
            logger.error(f"Error fetching metadata from PosterDB: {str(e)}")
            return None
            
    async def search(self, query: str) -> Optional[Dict]:
        """Search for posters"""
        # Implement when we have API access
        return None
        
    async def get_images(self, media_id: str) -> Optional[Dict]:
        """Get posters for a media item"""
        # Implement when we have API access
        return None
