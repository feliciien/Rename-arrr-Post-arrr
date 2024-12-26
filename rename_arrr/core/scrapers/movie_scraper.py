"""
Movie and TV Show metadata scraper
"""
from tmdbv3api import TMDb, Movie, TV
import tvmaze
import imdb
from datetime import datetime

class MovieTVScraper:
    def __init__(self, tmdb_api_key):
        self.tmdb = TMDb()
        self.tmdb.api_key = tmdb_api_key
        self.movie = Movie()
        self.tv = TV()
        self.tvmaze = tvmaze.TVMaze()
        self.imdb = imdb.IMDb()
        
    def search_movie(self, title):
        """Search for movie metadata"""
        try:
            results = self.movie.search(title)
            if results:
                movie = results[0]
                return {
                    'title': movie.title,
                    'year': movie.release_date[:4] if movie.release_date else None,
                    'tmdb_id': movie.id,
                    'type': 'movie'
                }
        except Exception as e:
            return None
            
    def search_tv_show(self, title):
        """Search for TV show metadata"""
        try:
            # Try TMDb first
            results = self.tv.search(title)
            if results:
                show = results[0]
                return {
                    'title': show.name,
                    'year': show.first_air_date[:4] if show.first_air_date else None,
                    'tmdb_id': show.id,
                    'type': 'tv'
                }
                
            # Fallback to TVMaze
            tvmaze_results = self.tvmaze.get_show_list(title)
            if tvmaze_results:
                show = tvmaze_results[0]
                return {
                    'title': show.name,
                    'year': str(show.premiered.year) if show.premiered else None,
                    'tvmaze_id': show.id,
                    'type': 'tv'
                }
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
