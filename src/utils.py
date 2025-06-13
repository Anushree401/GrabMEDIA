''' 
Utility functions (can be in a separate module)

    Helpers like:

        is_youtube_url(url)

        format_size(bytes)

        validate_url(url) 
'''

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
