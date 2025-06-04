"""
Application Configuration Settings
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # yt-dlp settings
    YTDLP_TIMEOUT = int(os.environ.get('YTDLP_TIMEOUT', 60))  # seconds
    MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT', 10))
    
    # Security settings
    SESSION_COOKIE_SECURE = not DEBUG
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

# Export the configuration
config = Config()
