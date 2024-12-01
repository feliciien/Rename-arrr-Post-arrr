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
    """
    if not TMDB_API_KEY:
        raise EnvironmentError("TMDB_API_KEY is not set. Please set it in your .env file.")

    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'include_adult': False
    }
    if year:
        params['year'] = year

    try:
        # Search for the movie
        response = requests.get(TMDB_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = data.get('results', [])
        if not results:
            raise ValueError(f"No metadata found for the title '{title}' with year '{year or 'N/A'}'.")

        # Assume the first result is the correct one
        movie = results[0]
        movie_id = movie['id']

        # Fetch detailed movie information
        details_response = requests.get(
            TMDB_MOVIE_DETAILS_URL.format(movie_id), 
            params={'api_key': TMDB_API_KEY}
        )
        details_response.raise_for_status()
        details = details_response.json()

        official_title = details.get('title', title)
        release_date = details.get('release_date', '')
        release_year = release_date.split('-')[0] if release_date else 'Unknown'

        return {
            'title': official_title,
            'year': release_year
        }

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to fetch metadata due to a connection error: {e}")
    except ValueError as ve:
        raise ValueError(str(ve))
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

# TEST BLOCK
if __name__ == "__main__":
    try:
        # Example 1: Valid title and year
        metadata = fetch_movie_metadata("Inception", 2010)
        print(f"Metadata for 'Inception (2010)': {metadata}")

        # Example 2: Valid title without year
        metadata = fetch_movie_metadata("Avatar")
        print(f"Metadata for 'Avatar': {metadata}")

        # Example 3: Non-existent movie
        metadata = fetch_movie_metadata("SomeNonExistentMovieTitle")
        print(f"Metadata for 'SomeNonExistentMovieTitle': {metadata}")
    except Exception as e:
        print(f"Error: {e}")