''' 
Utility functions (can be in a separate module)

    Helpers like:

        is_youtube_url(url)

        format_size(bytes)

        validate_url(url) 
'''

import os
import mimetypes

def is_youtube_url(url): 
    return 'youtube.com' in url or 'youtu.be' in url

def format_size(bytes):
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 * 1024:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1024 * 1024 * 1024:
        return f"{bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes / (1024 * 1024 * 1024):.2f} GB"

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL: must start with http:// or https://")
    if not url:
        raise ValueError("URL cannot be empty")
    return True

def get_file_type_from_url(url):
    filename = os.path.basename(url)
    ext = os.path.splitext(filename)[1].lower()
    extension_map = {
            '.mp3': 'audio',
            '.wav': 'audio',
            '.aac': 'audio',
            '.flac': 'audio',

            '.mp4': 'video',
            '.mkv': 'video',
            '.webm': 'video',
            '.avi': 'video',

            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.bmp': 'image',
            '.svg': 'image',

            '.pdf': 'pdf',
            '.doc': 'document',
            '.docx': 'document',
            '.txt': 'document',
            '.ppt': 'document',
            '.pptx': 'document',
            '.xls': 'document',
            '.xlsx': 'document',
    }
    if ext in extension_map:
        return extension_map[ext]
    
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type:
        if mime_type.startswith('audio/'):
            return 'audio'
        elif mime_type.startswith('video/'):
            return 'video'
        elif mime_type.startswith('image/'):
            return 'image'
        elif mime_type == 'application/pdf':
            return 'pdf'
        elif mime_type.startswith('application/') or mime_type.startswith('text/'):
            return 'document'
    return 'other'
