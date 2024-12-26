"""
Music metadata scraper using MusicBrainz and AcoustID
"""
import musicbrainzngs as mb
import acoustid
import os

class MusicScraper:
    def __init__(self, acoustid_api_key):
        self.acoustid_api_key = acoustid_api_key
        mb.set_useragent("Rename-arrr", "1.0")
        
    def get_acoustid_fingerprint(self, file_path):
        """Get audio fingerprint using AcoustID"""
        try:
            duration, fingerprint = acoustid.fingerprint_file(file_path)
            return fingerprint, duration
        except Exception as e:
            return None, None
            
    async def search_by_fingerprint(self, file_path):
        """Search music metadata using audio fingerprint"""
        fingerprint, duration = self.get_acoustid_fingerprint(file_path)
        if not fingerprint:
            return None
            
        try:
            results = acoustid.lookup(self.acoustid_api_key, fingerprint, duration)
            if results:
                recording = results[0]
                return {
                    'title': recording.get('title'),
                    'artist': recording.get('artist'),
                    'album': recording.get('album'),
                    'year': recording.get('year'),
                    'source': 'acoustid'
                }
        except Exception as e:
            return None
            
    def search_musicbrainz(self, title, artist=None):
        """Search music metadata on MusicBrainz"""
        try:
            query = f'recording:"{title}"'
            if artist:
                query += f' AND artist:"{artist}"'
                
            result = mb.search_recordings(query=query, limit=1)
            if result['recording-list']:
                recording = result['recording-list'][0]
                return {
                    'title': recording['title'],
                    'artist': recording['artist-credit'][0]['name'],
                    'album': recording.get('release-list', [{}])[0].get('title'),
                    'year': recording.get('release-list', [{}])[0].get('date', '')[:4],
                    'source': 'musicbrainz'
                }
        except Exception as e:
            return None
