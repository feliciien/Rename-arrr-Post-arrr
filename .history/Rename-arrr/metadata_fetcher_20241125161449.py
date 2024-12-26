# Rename-arrr/metadata_fetcher.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

TMDB_API_KEY = os.getenv('TMDB_API_KEY')  # Ensure you've set this in your .env file

def fetch_movie_metadata(title):
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': title
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch metadata: {response.status_code}")
    
    data = response.json()
    if data['results']:
        first_result = data['results'][0]
        return {
            'title': first_result['title'],
            'release_date': first_result.get('release_date', 'Unknown')
        }
    else:
        raise ValueError('No metadata found for the given title.')