"""
TVDB Scraper for fetching TV show metadata
"""
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class TVDBScraper:
    """Scraper for TVDB website"""
    BASE_URL = "https://thetvdb.com"
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
        """Search for TV shows"""
        await self._init_session()
        
        try:
            params = {'query': title}
            async with self.session.get(self.SEARCH_URL, params=params) as response:
                if response.status != 200:
                    logger.error(f"Failed to search TVDB: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                results = []
                for item in soup.select('.list-group-item'):
                    title_elem = item.select_one('.media-heading')
                    if not title_elem:
                        continue
                        
                    show_url = item.get('href')
                    if not show_url:
                        continue
                    
                    year_match = re.search(r'\((\d{4})\)', title_elem.text)
                    year = year_match.group(1) if year_match else None
                    
                    results.append({
                        'title': re.sub(r'\(\d{4}\)', '', title_elem.text).strip(),
                        'year': year,
                        'url': self.BASE_URL + show_url,
                        'source': 'tvdb'
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Error searching TVDB: {str(e)}")
            return []
    
    async def get_metadata(self, url: str) -> Optional[Dict]:
        """Get detailed metadata for a TV show"""
        await self._init_session()
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to get TVDB metadata: {response.status}")
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract basic info
                title = soup.select_one('h1')
                if not title:
                    return None
                
                # Get poster URL
                poster = soup.select_one('img.img-responsive')
                poster_url = poster.get('src') if poster else None
                
                # Get description
                description = soup.select_one('.show-overview')
                overview = description.text.strip() if description else None
                
                # Get year
                year_match = re.search(r'\((\d{4})\)', title.text)
                year = year_match.group(1) if year_match else None
                
                # Get genres
                genres = [g.text.strip() for g in soup.select('.genre-list li')]
                
                # Get rating
                rating = soup.select_one('.rating-value')
                rating = rating.text.strip() if rating else None
                
                return {
                    'title': re.sub(r'\(\d{4}\)', '', title.text).strip(),
                    'year': year,
                    'overview': overview,
                    'poster_url': poster_url,
                    'genres': genres,
                    'rating': rating,
                    'source': 'tvdb'
                }
                
        except Exception as e:
            logger.error(f"Error getting TVDB metadata: {str(e)}")
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
