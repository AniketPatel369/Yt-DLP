"""
API Routes for Multi-Platform yt-dlp JSON Extractor
"""
from flask import Blueprint, request, jsonify
from app.services.multi_platform_service import multi_platform_service
from app.utils.validators import is_valid_url, sanitize_url
import logging
from datetime import datetime

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Multi-Platform yt-dlp JSON Extractor',
        'supported_platforms': ['youtube', 'instagram', 'facebook']
    })

@api_bp.route('/', methods=['GET'])
def extract_from_url_param():
    """
    Extract metadata from URL with automatic platform detection
    
    Usage: 
    - YouTube: /?url=https://www.youtube.com/watch?v=VIDEO_ID
    - Instagram: /?url=https://www.instagram.com/p/POST_ID/
    - Facebook: /?url=https://www.facebook.com/watch?v=VIDEO_ID
    """
    try:
        raw_url = request.args.get('url', '').strip().strip('"\'')
        
        if not raw_url:
            return jsonify({
                'error': 'URL parameter required',
                'usage': '/?url=https://platform.com/video',
                'supported_platforms': ['YouTube', 'Instagram', 'Facebook'],
                'examples': {
                    'youtube': f'{request.host_url}?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                    'instagram': f'{request.host_url}?url=https://www.instagram.com/p/ABC123/',
                    'facebook': f'{request.host_url}?url=https://www.facebook.com/watch?v=123456'
                }
            }), 400
        
        url = sanitize_url(raw_url)
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # ✅ Detect platform
        platform_info = multi_platform_service.get_platform_info(url)
        logger.info(f"Processing {platform_info['platform']} URL: {url}")
        
        if not platform_info['supported']:
            return jsonify({
                'error': f"Unsupported platform: {platform_info['platform']}",
                'supported_platforms': ['youtube', 'instagram', 'facebook'],
                'detected_platform': platform_info['platform']
            }), 400
        
        # ✅ Extract with platform-specific service
        success, raw_metadata, error = multi_platform_service.extract_metadata_raw(url)
        
        if success:
            # ✅ Add platform info to response
            raw_metadata['platform_info'] = {
                'detected_platform': platform_info['platform'],
                'extraction_service': 'multi_platform_ytdlp'
            }
            return jsonify(raw_metadata)
        else:
            return jsonify({
                'error': error or 'Extraction failed',
                'platform': platform_info['platform'],
                'url': url,
                'platform_info': platform_info
            }), 422
            
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/platform-info', methods=['GET'])
def get_platform_info():
    """Get platform detection info for a URL"""
    url = request.args.get('url', '').strip().strip('"\'')
    
    if not url:
        return jsonify({'error': 'URL parameter required'}), 400
    
    url = sanitize_url(url)
    platform_info = multi_platform_service.get_platform_info(url)
    
    return jsonify(platform_info)

@api_bp.route('/supported-platforms', methods=['GET'])
def get_supported_platforms():
    """Get list of supported platforms and their configurations"""
    platforms = {}
    
    for platform, config in multi_platform_service.platform_configs.items():
        platforms[platform] = {
            'cookies_file': config['cookies'],
            'user_agent': config['user_agent'][:50] + '...',  # Truncate for readability
            'sleep_interval': config['sleep_interval'],
            'has_extra_args': len(config['extra_args']) > 0
        }
    
    return jsonify({
        'supported_platforms': list(platforms.keys()),
        'configurations': platforms,
        'total_platforms': len(platforms)
    })
