"""
Multi-Platform yt-dlp Service
Supports YouTube, Instagram, Facebook with platform-specific configurations
"""
import subprocess
import json
import logging
import sys
import re
from typing import Dict, Any, Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class MultiPlatformYtDlpService:
    """Multi-platform service with different configurations per platform"""
    
    def __init__(self):
        self.timeout = 90
        self.max_retries = 3
        self.ytdlp_available = self._check_ytdlp_installation()
        
        # ✅ Platform-specific configurations
        self.platform_configs = {
            'youtube': {
                'cookies': './www.youtube.com_cookies.txt',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'sleep_interval': '2',
                'extra_args': ['--extractor-args', 'youtube:player_client=android']
            },
            'instagram': {
                'cookies': './www.instagram.com_cookies.txt',
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                'sleep_interval': '3',
                'extra_args': ['--extractor-args', 'instagram:api_type=graphql']
            },
            'facebook': {
                'cookies': './www.facebook.com_cookies.txt',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'sleep_interval': '4',
                'extra_args': []
            }
        }
        
        if not self.ytdlp_available:
            raise RuntimeError("yt-dlp is not available")
    
    def _check_ytdlp_installation(self) -> bool:
        """Check if yt-dlp is properly installed"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'yt_dlp', '--version'], 
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                logger.info(f"yt-dlp found: {result.stdout.strip()}")
                return True
            return False
        except Exception as e:
            logger.error(f"yt-dlp check failed: {e}")
            return False
    
    def detect_platform(self, url: str) -> str:
        """
        Detect which platform the URL belongs to
        
        Args:
            url: The video URL
            
        Returns:
            Platform name: 'youtube', 'instagram', 'facebook', or 'unknown'
        """
        try:
            parsed_url = urlparse(url.lower())
            domain = parsed_url.netloc
            
            # ✅ YouTube detection
            youtube_domains = [
                'youtube.com', 'www.youtube.com', 'm.youtube.com',
                'youtu.be', 'www.youtu.be',
                'youtube-nocookie.com', 'www.youtube-nocookie.com'
            ]
            
            # ✅ Instagram detection
            instagram_domains = [
                'instagram.com', 'www.instagram.com', 'm.instagram.com',
                'instagr.am', 'www.instagr.am'
            ]
            
            # ✅ Facebook detection
            facebook_domains = [
                'facebook.com', 'www.facebook.com', 'm.facebook.com',
                'fb.com', 'www.fb.com', 'fb.watch'
            ]
            
            if any(d in domain for d in youtube_domains):
                return 'youtube'
            elif any(d in domain for d in instagram_domains):
                return 'instagram'
            elif any(d in domain for d in facebook_domains):
                return 'facebook'
            else:
                return 'unknown'
                
        except Exception as e:
            logger.error(f"Error detecting platform: {e}")
            return 'unknown'
    
    def extract_metadata_raw(self, url: str) -> Tuple[bool, Optional[Dict[Any, Any]], Optional[str]]:
        """
        Extract metadata using platform-specific configuration
        """
        if not url:
            return False, None, "No URL provided"
        
        # ✅ Detect platform
        platform = self.detect_platform(url)
        logger.info(f"Detected platform: {platform} for URL: {url}")
        
        if platform == 'unknown':
            return False, None, f"Unsupported platform. URL: {url}"
        
        # ✅ Get platform-specific configuration
        config = self.platform_configs.get(platform)
        if not config:
            return False, None, f"No configuration found for platform: {platform}"
        
        # ✅ Route to platform-specific extraction
        if platform == 'youtube':
            return self._extract_youtube(url, config)
        elif platform == 'instagram':
            return self._extract_instagram(url, config)
        elif platform == 'facebook':
            return self._extract_facebook(url, config)
        else:
            return False, None, f"Platform {platform} not implemented yet"
    
    def _extract_youtube(self, url: str, config: Dict) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Extract from YouTube with YouTube-specific settings"""
        logger.info("🎥 Extracting from YouTube")
        
        for attempt in range(self.max_retries):
            try:
                cmd = [
                    sys.executable, '-m', 'yt_dlp',
                    '--dump-json',
                    '--no-warnings',
                    '--no-playlist',
                    '--no-check-certificate',
                    '--skip-download',
                    '--cookies', config['cookies'],
                    '--user-agent', config['user_agent'],
                    '--sleep-interval', config['sleep_interval'],
                ] + config['extra_args'] + [url]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
                
                if result.returncode == 0:
                    metadata = json.loads(result.stdout)
                    logger.info(f"✅ YouTube extraction successful: {metadata.get('title', 'Unknown')}")
                    return True, metadata, None
                else:
                    error_msg = result.stderr.strip()
                    logger.warning(f"❌ YouTube attempt {attempt + 1} failed: {error_msg}")
                    
            except Exception as e:
                logger.error(f"Exception in YouTube extraction: {e}")
        
        return False, None, "YouTube extraction failed after all retries"
    
    def _extract_instagram(self, url: str, config: Dict) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Extract from Instagram with Instagram-specific settings"""
        logger.info("📷 Extracting from Instagram")
        
        for attempt in range(self.max_retries):
            try:
                # ✅ Instagram-specific command
                cmd = [
                    sys.executable, '-m', 'yt_dlp',
                    '--dump-json',
                    '--no-warnings',
                    '--no-playlist',
                    '--no-check-certificate',
                    '--skip-download',
                    '--cookies', config['cookies'],
                    '--user-agent', config['user_agent'],
                    '--sleep-interval', config['sleep_interval'],
                    '--referer', 'https://www.instagram.com/',  # Instagram-specific
                ] + config['extra_args'] + [url]
                
                logger.info(f"Instagram extraction attempt {attempt + 1}")
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
                
                if result.returncode == 0:
                    try:
                        metadata = json.loads(result.stdout)
                        logger.info(f"✅ Instagram extraction successful: {metadata.get('title', 'Unknown')}")
                        
                        # ✅ Add Instagram-specific metadata
                        metadata['platform'] = 'instagram'
                        metadata['extracted_from'] = 'instagram_service'
                        
                        return True, metadata, None
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decode error: {e}")
                        continue
                else:
                    error_msg = result.stderr.strip()
                    logger.warning(f"❌ Instagram attempt {attempt + 1} failed: {error_msg}")
                    
                    # ✅ Try fallback method for Instagram
                    if attempt == self.max_retries - 1:
                        return self._instagram_fallback_method(url)
                    
            except Exception as e:
                logger.error(f"Exception in Instagram extraction: {e}")
        
        return False, None, "Instagram extraction failed after all retries"
    
    def _instagram_fallback_method(self, url: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Fallback method for Instagram when cookies fail"""
        logger.info("🔄 Trying Instagram fallback method")
        
        try:
            # ✅ Try without cookies but with mobile user agent
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--dump-json',
                '--no-warnings',
                '--user-agent', 'Instagram 219.0.0.12.117 Android',
                '--sleep-interval', '4',
                '--referer', 'https://www.instagram.com/',
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
            
            if result.returncode == 0:
                metadata = json.loads(result.stdout)
                logger.info("✅ Instagram fallback method successful")
                metadata['platform'] = 'instagram'
                metadata['extraction_method'] = 'fallback'
                return True, metadata, None
            else:
                return False, None, f"Instagram fallback failed: {result.stderr.strip()}"
                
        except Exception as e:
            return False, None, f"Instagram fallback error: {e}"
    
    def _extract_facebook(self, url: str, config: Dict) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Extract from Facebook with Facebook-specific settings"""
        logger.info("📘 Extracting from Facebook")
        
        # ✅ Placeholder for Facebook implementation
        return False, None, "Facebook extraction not implemented yet"
    
    def get_platform_info(self, url: str) -> Dict[str, Any]:
        """Get information about the detected platform"""
        platform = self.detect_platform(url)
        config = self.platform_configs.get(platform, {})
        
        return {
            'platform': platform,
            'supported': platform in self.platform_configs,
            'cookies_file': config.get('cookies', 'Not configured'),
            'user_agent': config.get('user_agent', 'Default'),
            'configuration': config
        }

# Create service instance
multi_platform_service = MultiPlatformYtDlpService()
