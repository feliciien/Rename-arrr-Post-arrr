"""
AniDB scraper for anime metadata
"""
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class AniDBScraper:
    def __init__(self):
        self.base_url = "https://anidb.net"
        self.search_url = f"{self.base_url}/perl-bin/animedb.pl"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def search_anime(self, title: str) -> Optional[Dict]:
        """Search for anime on AniDB"""
        if not self.session:
            return None
            
        try:
            params = {
                'show': 'animelist',
                'adb.search': title,
                'do.search': 1
            }
            
            async with self.session.get(self.search_url, params=params) as response:
                if response.status != 200:
                    return None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                # Find the first anime result
                anime_link = soup.find('td', class_='name').find('a')
                if not anime_link:
                    return None
                    
                anime_id = re.search(r'aid=(\d+)', anime_link['href']).group(1)
                
                # Get detailed info
                return await self._get_anime_details(anime_id)
                
        except Exception as e:
            logger.error(f"Error searching AniDB: {str(e)}")
            return None
            
    async def _get_anime_details(self, anime_id: str) -> Optional[Dict]:
        """Get detailed anime information"""
        try:
            url = f"{self.base_url}/anime/{anime_id}"
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    return None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                # Extract information
                title_tag = soup.find('h1', class_='anime')
                year_tag = soup.find('span', class_='year')
                
                if not title_tag:
                    return None
                    
                return {
                    'title': title_tag.text.strip(),
                    'year': year_tag.text.strip() if year_tag else None,
                    'type': 'anime',
                    'source': 'anidb',
                    'id': anime_id,
                    'url': url
                }
                
        except Exception as e:
            logger.error(f"Error getting anime details: {str(e)}")
            return None
