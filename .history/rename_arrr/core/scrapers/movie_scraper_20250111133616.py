"""
Movie and TV Show metadata scraper
"""
from tmdbv3api import TMDb, Movie, TV
import requests
import imdb
import os
import requests
from datetime import datetime

def download_image(url, save_path):
    """Download an image from a URL and save it to a specified path"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Failed to download image: {e}")

class MovieTVScraper:
    def __init__(self, tmdb_api_key):
        self.tmdb = TMDb()
        self.tmdb.api_key = tmdb_api_key
        self.movie = Movie()
        self.tv = TV()
        # self.tvmaze = tvmaze.TVMaze()  # Commented out as tvmaze-py is unavailable
        self.imdb = imdb.IMDb()
        
    def search_movie(self, title):
        """Search for movie metadata"""
        try:
            results = self.movie.search(title)
            if results:
                movie = results[0]
                metadata = {
                    'title': movie.title,
                    'year': movie.release_date[:4] if movie.release_date else None,
                    'tmdb_id': movie.id,
                    'type': 'movie',
                    'genres': [genre.name for genre in movie.genres],
                    'poster_path': movie.poster_path,
                }
                # Download poster
                if movie.poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{movie.poster_path}"
                    download_image(poster_url, os.path.join('posters', f"{movie.title}.jpg"))
                return metadata
        except Exception as e:
            return None
            
    def search_tv_show(self, title):
        """Search for TV show metadata"""
        try:
            # Try TMDb first
            results = self.tv.search(title)
            if results:
                show = results[0]
                metadata = {
                    'title': show.name,
                    'year': show.first_air_date[:4] if show.first_air_date else None,
                    'tmdb_id': show.id,
                    'type': 'tv',
                    'genres': [genre.name for genre in show.genres],
                    'poster_path': show.poster_path,
                }
                # Download poster
                if show.poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{show.poster_path}"
                    download_image(poster_url, os.path.join('posters', f"{show.name}.jpg"))
                return metadata
                
            # Fallback to TVMaze
            # Fallback to TVMaze API directly
            tvmaze_url = f"https://api.tvmaze.com/search/shows?q={title}"
            response = requests.get(tvmaze_url)
            if response.status_code == 200:
                tvmaze_results = response.json()
                if tvmaze_results:
                    show = tvmaze_results[0]['show']
                    return {
                        'title': show['name'],
        except Exception as e:
            return None
            
    def get_episode_info(self, show_id, season, episode, source='tmdb'):
        """Get specific episode information"""
        try:
            if source == 'tmdb':
                episode_info = self.tv.episode(show_id, season, episode)
                return {
                    'name': episode_info.name,
                    'overview': episode_info.overview,
                    'air_date': episode_info.air_date
                }
            elif source == 'tvmaze':
                show = self.tvmaze.get_show(show_id)
                episode_info = show.get_episode(season=season, number=episode)
                return {
                    'name': episode_info.name,
                    'overview': episode_info.summary,
                    'air_date': str(episode_info.airdate)
                }
        except Exception as e:
            return None
