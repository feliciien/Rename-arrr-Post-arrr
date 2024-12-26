"""
Media scrapers package
"""
from .base import BaseScraper
from .anidb import AniDBScraper
from .tvdb import TVDBScraper
from .posterdb import PosterDBScraper

__all__ = ['BaseScraper', 'AniDBScraper', 'TVDBScraper', 'PosterDBScraper']
