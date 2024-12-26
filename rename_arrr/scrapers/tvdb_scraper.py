"""
TVDB scraper for TV series metadata
"""
import os
from tvdb_v4_official import TVDB
import logging
from typing import Dict, Optional
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class TVDBScraper:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('TVDB_API_KEY')
        self.base_url = "https://thetvdb.com"
        self.client = None
        self.session = None
        
        if self.api_key:
            try:
                self.client = TVDB(apikey=self.api_key)
                self.client.login()
            except Exception as e:
                logger.error(f"Failed to initialize TVDB client: {str(e)}")
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def search_series(self, title: str) -> Optional[Dict]:
        """Search for TV series on TVDB"""
        try:
            if self.client:
                # Try API first
                results = self.client.search(query=title, type='series')
                if results and results.get('data'):
                    series = results['data'][0]
                    return {
                        'title': series.get('name'),
                        'year': series.get('firstAired', '').split('-')[0] if series.get('firstAired') else None,
                        'type': 'series',
                        'source': 'tvdb',
                        'id': series.get('tvdb_id'),
                        'url': f"{self.base_url}/series/{series.get('tvdb_id')}"
                    }
            
            # Fallback to web scraping
            return await self._search_web(title)
            
        except Exception as e:
            logger.error(f"Error searching TVDB: {str(e)}")
            return None
            
    async def _search_web(self, title: str) -> Optional[Dict]:
        """Fallback to web scraping when API is not available"""
        if not self.session:
            return None
            
        try:
            search_url = f"{self.base_url}/search"
            params = {'query': title, 'type': 'series'}
            
            async with self.session.get(search_url, params=params) as response:
                if response.status != 200:
                    return None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                # Find the first search result
                result = soup.find('div', class_='search-result')
                if not result:
                    return None
                    
                # Extract title and year
                title_elem = result.find('h3', class_='title')
                if not title_elem:
                    return None
                    
                title = title_elem.text.strip()
                year = None
                
                # Try to extract year from title or additional info
                year_elem = result.find('span', class_='year')
                if year_elem:
                    year = year_elem.text.strip()
                    
                # Get series ID from URL
                link = result.find('a', href=True)
                if not link:
                    return None
                    
                series_id = link['href'].split('/')[-1]
                
                return {
                    'title': title,
                    'year': year,
                    'type': 'series',
                    'source': 'tvdb',
                    'id': series_id,
                    'url': f"{self.base_url}/series/{series_id}"
                }
                
        except Exception as e:
            logger.error(f"Error scraping TVDB: {str(e)}")
            return None
