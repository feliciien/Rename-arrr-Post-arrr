"""
MediaInfo wrapper for extracting media metadata
"""
from mediainfo import MediaInfo
import os

class MediaInfoExtractor:
    def __init__(self):
        self.media_info = MediaInfo()
    
    def get_media_info(self, file_path):
        """Extract media information from file"""
        if not os.path.exists(file_path):
            return None
            
        try:
            info = self.media_info.get_media_info(file_path)
            return {
                'duration': info.get('duration'),
                'video_codec': info.get('video_codec'),
                'audio_codec': info.get('audio_codec'),
                'resolution': f"{info.get('width')}x{info.get('height')}",
                'file_size': info.get('file_size'),
                'container': info.get('container')
            }
        except Exception as e:
            return None
