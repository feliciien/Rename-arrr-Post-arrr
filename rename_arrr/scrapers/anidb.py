"""
AniDB Scraper for fetching anime metadata
"""
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import Dict, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class AniDBScraper:
    """Scraper for AniDB website"""
    BASE_URL = "https://anidb.net"
    SEARCH_URL = f"{BASE_URL}/perl-bin/animedb.pl"
    
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
        """Search for anime"""
        await self._init_session()
        
        try:
            params = {
                'show': 'search',
                'do.search': 1,
                'adb.search': title
            }
            
            async with self.session.get(self.SEARCH_URL, params=params) as response:
                if response.status != 200:
                    logger.error(f"Failed to search AniDB: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                results = []
                for item in soup.select('tr.anime'):
                    title_elem = item.select_one('td.name')
                    if not title_elem:
                        continue
                        
                    anime_id = item.get('id', '').replace('aid', '')
                    if not anime_id:
                        continue
                    
                    year_elem = item.select_one('td.year')
                    year = year_elem.text.strip() if year_elem else None
                    
                    results.append({
                        'title': title_elem.text.strip(),
                        'year': year,
                        'url': f"{self.BASE_URL}/anime/{anime_id}",
                        'source': 'anidb'
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Error searching AniDB: {str(e)}")
            return []
    
    async def get_metadata(self, url: str) -> Optional[Dict]:
        """Get detailed metadata for an anime"""
        await self._init_session()
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"Failed to get AniDB metadata: {response.status}")
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract basic info
                title = soup.select_one('h1.anime')
                if not title:
                    return None
                
                # Get poster URL
                poster = soup.select_one('img.image')
                poster_url = poster.get('src') if poster else None
                if poster_url and not poster_url.startswith('http'):
                    poster_url = f"https:{poster_url}"
                
                # Get description
                description = soup.select_one('div.desc')
                overview = description.text.strip() if description else None
                
                # Get year
                year_elem = soup.select_one('span.year')
                year = year_elem.text.strip() if year_elem else None
                
                # Get genres
                genres = [g.text.strip() for g in soup.select('span.tag')]
                
                # Get rating
                rating = soup.select_one('span.rating')
                rating = rating.text.strip() if rating else None
                
                # Get episode count
                episodes = soup.select_one('span.episodes')
                episode_count = episodes.text.strip() if episodes else None
                
                return {
                    'title': title.text.strip(),
                    'year': year,
                    'overview': overview,
                    'poster_url': poster_url,
                    'genres': genres,
                    'rating': rating,
                    'episodes': episode_count,
                    'source': 'anidb'
                }
                
        except Exception as e:
            logger.error(f"Error getting AniDB metadata: {str(e)}")
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
