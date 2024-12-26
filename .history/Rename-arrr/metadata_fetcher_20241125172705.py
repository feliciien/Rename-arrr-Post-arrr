# Rename-arrr/metadata_fetcher.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie/{}"

def fetch_movie_metadata(title, year=None):
    """
    Fetches movie metadata from TheMovieDB API based on the title and optional year.
    
    :param title: Title of the movie.
    :param year: Release year of the movie (optional).
    :return: Dictionary containing movie title and release year.
    :raises ValueError: If no metadata is found.
    :raises ConnectionError: If API request fails.
    """
    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'include_adult': False
    }
    if year:
        params['year'] = year

    response = requests.get(TMDB_SEARCH_URL, params=params)
    
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch metadata: {response.status_code} - {response.text}")

    data = response.json()
    results = data.get('results')
    
    if not results:
        raise ValueError("No metadata found for the given title.")

    # Assume the first result is the correct one
    movie = results[0]
    movie_id = movie['id']

    # Fetch detailed information
    details_response = requests.get(TMDB_MOVIE_DETAILS_URL.format(movie_id), params={'api_key': TMDB_API_KEY})
    if details_response.status_code != 200:
        raise ConnectionError(f"Failed to fetch movie details: {details_response.status_code} - {details_response.text}")

    details = details_response.json()
    official_title = details.get('title')
    release_date = details.get('release_date', '')
    release_year = release_date.split('-')[0] if release_date else 'Unknown'

    return {
        'title': official_title,
        'year': release_year
    }