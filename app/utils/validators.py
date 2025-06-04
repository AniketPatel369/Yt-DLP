"""
URL Validation Utilities
"""
import re
from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """
    Check if the provided string is a valid URL
    
    Args:
        url: URL string to validate
        
    Returns:
        True if URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    try:
        result = urlparse(url.strip())
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def is_youtube_url(url: str) -> bool:
    """
    Check if the URL is a valid YouTube URL
    
    Args:
        url: URL string to validate
        
    Returns:
        True if URL is from YouTube, False otherwise
    """
    if not is_valid_url(url):
        return False
    
    youtube_patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)',
        r'youtube\.com/.*[?&]v=',
    ]
    
    for pattern in youtube_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    
    return False

def sanitize_url(url: str) -> str:
    """
    Sanitize and clean the URL
    
    Args:
        url: URL string to sanitize
        
    Returns:
        Cleaned URL string
    """
    if not url:
        return ""
    
    # Strip whitespace
    url = url.strip()
    
    # Add https if no protocol specified
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url
