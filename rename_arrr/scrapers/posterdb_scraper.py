"""
ThePosterDB scraper for movie and TV show posters
"""
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
import os
from typing import Dict, List, Optional
import aiofiles

logger = logging.getLogger(__name__)

class PosterDBScraper:
    def __init__(self):
        self.base_url = "https://theposterdb.com"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def search_posters(self, title: str) -> Optional[List[Dict]]:
        """Search for posters on ThePosterDB"""
        if not self.session:
            return None
            
        try:
            search_url = f"{self.base_url}/search"
            params = {'q': title}
            
            async with self.session.get(search_url, params=params) as response:
                if response.status != 200:
                    return None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                posters = []
                poster_items = soup.find_all('div', class_='poster-item')
                
                for item in poster_items[:5]:  # Limit to first 5 posters
                    poster_link = item.find('a')
                    if not poster_link:
                        continue
                        
                    poster_url = self.base_url + poster_link['href']
                    poster_info = await self._get_poster_details(poster_url)
                    
                    if poster_info:
                        posters.append(poster_info)
                        
                return posters
                
        except Exception as e:
            logger.error(f"Error searching PosterDB: {str(e)}")
            return None
            
    async def _get_poster_details(self, poster_url: str) -> Optional[Dict]:
        """Get detailed poster information"""
        try:
            async with self.session.get(poster_url) as response:
                if response.status != 200:
                    return None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                title_tag = soup.find('h1')
                image_tag = soup.find('img', class_='poster')
                
                if not title_tag or not image_tag:
                    return None
                    
                return {
                    'title': title_tag.text.strip(),
                    'image_url': image_tag['src'],
                    'page_url': poster_url
                }
                
        except Exception as e:
            logger.error(f"Error getting poster details: {str(e)}")
            return None
            
    async def download_poster(self, image_url: str, save_path: str) -> bool:
        """Download poster image"""
        if not self.session:
            return False
            
        try:
            async with self.session.get(image_url) as response:
                if response.status != 200:
                    return False
                    
                # Ensure directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # Save image
                async with aiofiles.open(save_path, 'wb') as f:
                    await f.write(await response.read())
                    
                return True
                
        except Exception as e:
            logger.error(f"Error downloading poster: {str(e)}")
            return False
