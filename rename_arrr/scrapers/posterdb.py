"""
PosterDB Scraper for fetching media posters
"""
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class PosterDBScraper:
    """Scraper for PosterDB website"""
    BASE_URL = "https://theposterdb.com"
    SEARCH_URL = f"{BASE_URL}/search"
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def _init_session(self):
        """Initialize aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
    
    async def search(self, title: str) -> List[Dict]:
        """Search for posters"""
        await self._init_session()
        
        try:
            params = {'q': title}
            async with self.session.get(self.SEARCH_URL, params=params) as response:
                if response.status != 200:
                    logger.error(f"Failed to search PosterDB: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                results = []
                for item in soup.select('.poster-container'):
                    title_elem = item.select_one('.poster-title')
                    if not title_elem:
                        continue
                        
                    poster_url = item.select_one('img.poster')
                    if not poster_url:
                        continue
                    
                    year_match = re.search(r'\((\d{4})\)', title_elem.text)
                    year = year_match.group(1) if year_match else None
                    
                    results.append({
                        'title': re.sub(r'\(\d{4}\)', '', title_elem.text).strip(),
                        'year': year,
                        'url': self.BASE_URL + item.get('href', ''),
                        'poster_url': poster_url.get('src'),
                        'source': 'posterdb'
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Error searching PosterDB: {str(e)}")
            return []
    
    async def get_posters(self, url: str) -> List[Dict]:
        """Get all posters for a media item"""
        await self._init_session()
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to get PosterDB posters: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                posters = []
                for item in soup.select('.poster-container'):
                    poster = item.select_one('img.poster')
                    if not poster:
                        continue
                    
                    author = item.select_one('.poster-author')
                    
                    posters.append({
                        'url': poster.get('src'),
                        'author': author.text.strip() if author else None,
                        'source': 'posterdb'
                    })
                
                return posters
                
        except Exception as e:
            logger.error(f"Error getting PosterDB posters: {str(e)}")
            return []
    
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
