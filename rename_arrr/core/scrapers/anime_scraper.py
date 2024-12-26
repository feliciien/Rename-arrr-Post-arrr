"""
Anime metadata scraper for various anime databases
"""
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

class AnimeScraper:
    def __init__(self):
        self.session = None
        self.sources = {
            'kitsu': 'https://kitsu.io/api/edge',
            'myanimelist': 'https://api.myanimelist.net/v2',
            'anilist': 'https://graphql.anilist.co',
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def search_kitsu(self, title):
        """Search anime on Kitsu.io"""
        if not self.session:
            return None
            
        try:
            url = f"{self.sources['kitsu']}/anime"
            params = {'filter[text]': title}
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['data']:
                        return {
                            'title': data['data'][0]['attributes']['canonicalTitle'],
                            'year': data['data'][0]['attributes']['startDate'][:4],
                            'source': 'kitsu'
                        }
        except Exception as e:
            return None
            
    async def search_all(self, title):
        """Search across all anime sources"""
        results = []
        search_tasks = [
            self.search_kitsu(title),
            # Add other source searches here
        ]
        
        completed = await asyncio.gather(*search_tasks, return_exceptions=True)
        return [r for r in completed if r and not isinstance(r, Exception)]
