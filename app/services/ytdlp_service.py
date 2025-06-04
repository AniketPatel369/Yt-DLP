"""
yt-dlp Service Layer
Handles all yt-dlp related operations using Python module syntax
"""
import subprocess
import json
import logging
import sys
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class YtDlpService:
    """Service class for yt-dlp operations"""
    
    def __init__(self):
        """Initialize the service"""
        self.timeout = 60
        self.max_retries = 3
        self.ytdlp_available = self._check_ytdlp_installation()
        
        if not self.ytdlp_available:
            raise RuntimeError("yt-dlp is not available via Python module")
    
    def _check_ytdlp_installation(self) -> bool:
        """Check if yt-dlp is properly installed"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'yt_dlp', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"yt-dlp found via Python module: {result.stdout.strip()}")
                return True
            else:
                logger.error(f"yt-dlp module check failed: {result.stderr}")
                return False
                
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            logger.error(f"yt-dlp check failed: {e}")
            return False
    
    def extract_metadata_raw(self, url: str) -> Tuple[bool, Optional[Dict[Any, Any]], Optional[str]]:
        """
        Extract RAW metadata from a video URL using yt-dlp Python module
        Returns the complete, unmodified response from yt-dlp
        """
        if not url:
            return False, None, "No URL provided"
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Extracting RAW metadata for URL: {url} (attempt {attempt + 1})")
                
                cmd = [
                    sys.executable, '-m', 'yt_dlp',
                    '--dump-json',
                    '--no-warnings',
                    '--no-playlist',
                    '--no-check-certificate',
                    '--skip-download',
                    '--cookies', './www.youtube.com_cookies.txt',  # ✅ Use cookies
                    '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    '--sleep-interval', '2',  # Add delay
                    url
                ]
                
                logger.info(f"Running command: {' '.join(cmd[:3])} ... {url}")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False
                )
                
                if result.returncode != 0:
                    error_msg = result.stderr.strip() or "yt-dlp command failed"
                    logger.error(f"yt-dlp failed (attempt {attempt + 1}): {error_msg}")
                    
                    if attempt == self.max_retries - 1:
                        return False, None, f"yt-dlp error: {error_msg}"
                    continue
                
                # Parse JSON output and return AS-IS
                try:
                    raw_metadata = json.loads(result.stdout)
                    
                    logger.info(f"Successfully extracted RAW metadata for: {raw_metadata.get('title', 'Unknown')}")
                    # ✅ Return the complete, unmodified response from yt-dlp
                    return True, raw_metadata, None
                    
                except json.JSONDecodeError as e:
                    error_msg = f"Failed to parse JSON output: {str(e)}"
                    logger.error(error_msg)
                    return False, None, error_msg
                    
            except subprocess.TimeoutExpired:
                error_msg = f"Request timeout after {self.timeout} seconds"
                logger.error(error_msg)
                if attempt == self.max_retries - 1:
                    return False, None, error_msg
                
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                logger.error(error_msg)
                if attempt == self.max_retries - 1:
                    return False, None, error_msg
        
        return False, None, "Maximum retries exceeded"
    
    # Keep the old method for the web interface
    def extract_metadata(self, url: str) -> Tuple[bool, Optional[Dict[Any, Any]], Optional[str]]:
        """Extract cleaned metadata (for web interface)"""
        success, raw_data, error = self.extract_metadata_raw(url)
        if success:
            cleaned_data = self._clean_metadata(raw_data)
            return True, cleaned_data, None
        return success, raw_data, error
    
    def _clean_metadata(self, metadata: Dict[Any, Any]) -> Dict[Any, Any]:
        """Clean metadata for web interface"""
        important_fields = [
            'id', 'title', 'description', 'uploader', 'uploader_id',
            'upload_date', 'duration', 'view_count', 'like_count',
            'comment_count', 'thumbnail', 'webpage_url', 'formats',
            'extractor'
        ]
        
        cleaned = {}
        for field in important_fields:
            if field in metadata:
                cleaned[field] = metadata[field]
        
        from datetime import datetime
        cleaned['extracted_at'] = datetime.utcnow().isoformat() + 'Z'
        
        return cleaned

# Create service instance
ytdlp_service = YtDlpService()
