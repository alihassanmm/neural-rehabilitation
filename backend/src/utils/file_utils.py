import re
from typing import Optional

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_google_doc_id(url: str) -> Optional[str]:
    """
    Extract Google Doc ID from various Google Docs URL formats
    """
    if not url:
        return None
    
    # Common Google Docs URL patterns
    patterns = [
        r'https://docs\.google\.com/document/d/([a-zA-Z0-9-_]+)',
        r'https://drive\.google\.com/file/d/([a-zA-Z0-9-_]+)',
        r'https://drive\.google\.com/open\?id=([a-zA-Z0-9-_]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If it's just the ID itself
    if re.match(r'^[a-zA-Z0-9-_]+$', url):
        return url
    
    return None

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    """
    import os
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def is_valid_file_size(file_path: str, max_size_mb: int = 12) -> bool:
    """
    Check if file size is within allowed limits
    """
    return get_file_size_mb(file_path) <= max_size_mb

