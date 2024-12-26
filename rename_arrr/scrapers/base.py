"""
Base scraper class for all media scrapers
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseScraper(ABC):
    """Base class for all media scrapers"""
    
    @abstractmethod
    async def fetch_metadata(self, info: Dict) -> Optional[Dict]:
        """Fetch metadata for a media item"""
        pass
        
    @abstractmethod
    async def search(self, query: str) -> Optional[Dict]:
        """Search for a media item"""
        pass
        
    @abstractmethod
    async def get_images(self, media_id: str) -> Optional[Dict]:
        """Get images for a media item"""
        pass
