#!/usr/bin/env python3
"""
yt-dlp JSON Extractor - Main Application Entry Point
A Flask-based web application for extracting YouTube video metadata using yt-dlp
"""
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Development server configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🚀 Starting yt-dlp JSON Extractor on port {port}")
    print(f"📱 Access the application at: http://localhost:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )
